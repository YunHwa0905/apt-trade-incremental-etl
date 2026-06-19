"""
이상거래 탐지
- 같은 단지(apt_nm + sgg_cd), 같은 거래월(deal_year, deal_month) 내 평균 평당가를 기준으로
  ±30% 이상 벗어난 거래를 탐지
- 구 단위 평균이 아니라 "단지 단위" 평균을 쓰는 이유:
  같은 구 안에도 평형/연식/단지 등급이 섞여 있어 구 평균과 비교하면
  "이상거래"가 아니라 "단지/평형 차이"를 잡아내는 노이즈가 커짐.
  같은 단지 내 비교라야 직거래 저가 매도, 허위신고 의심 등 의미 있는 이상치를 잡아낼 수 있음.
- outlier_trade 테이블에 기록 (apt_trade.is_outlier 플래그도 함께 갱신)

실행: python -m analysis.outlier_detect
"""

from db.connection import get_connection

OUTLIER_THRESHOLD_RATE = 30.0  # 단지 평균 대비 ±30%
MIN_SAMPLE_SIZE = 3  # 같은 단지+같은 달 거래가 이 건수 미만이면 평균 자체가 불안정하므로 탐지 제외

SELECT_APT_MONTHLY_AVG_SQL = """
SELECT
    apt_nm,
    sgg_cd,
    deal_year,
    deal_month,
    COUNT(*) AS sample_size,
    AVG(price_per_pyeong) AS apt_avg_price_per_pyeong
FROM apt_trade
WHERE price_per_pyeong IS NOT NULL
GROUP BY apt_nm, sgg_cd, deal_year, deal_month
HAVING COUNT(*) >= %(min_sample)s
"""

SELECT_TRADES_SQL = """
SELECT id, sgg_cd, apt_nm, deal_year, deal_month, price_per_pyeong
FROM apt_trade
WHERE price_per_pyeong IS NOT NULL
    AND id NOT IN (SELECT apt_trade_id FROM outlier_trade)
"""

INSERT_OUTLIER_SQL = """
INSERT INTO outlier_trade (
    apt_trade_id, sgg_cd, apt_nm,
    deal_price_per_pyeong, region_avg_price_per_pyeong, deviation_rate
) VALUES (
    %(apt_trade_id)s, %(sgg_cd)s, %(apt_nm)s,
    %(deal_price_per_pyeong)s, %(region_avg_price_per_pyeong)s, %(deviation_rate)s
)
"""

UPDATE_FLAG_SQL = """
UPDATE apt_trade SET is_outlier = TRUE WHERE id IN ({placeholders})
"""


def detect_outliers():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # 1. 단지+월 단위 평균 평당가 계산 (샘플 수가 너무 적은 단지는 제외)
            cursor.execute(SELECT_APT_MONTHLY_AVG_SQL, {"min_sample": MIN_SAMPLE_SIZE})
            avg_rows = cursor.fetchall()

            avg_lookup = {}
            for row in avg_rows:
                key = (row["apt_nm"], row["sgg_cd"], row["deal_year"], row["deal_month"])
                avg_lookup[key] = float(row["apt_avg_price_per_pyeong"])

            # 2. 아직 검사하지 않은 거래 조회
            cursor.execute(SELECT_TRADES_SQL)
            trades = cursor.fetchall()

        outlier_records = []
        outlier_ids = []

        for trade in trades:
            key = (trade["apt_nm"], trade["sgg_cd"], trade["deal_year"], trade["deal_month"])
            apt_avg = avg_lookup.get(key)

            if apt_avg is None or apt_avg == 0:
                # 샘플 수 부족(MIN_SAMPLE_SIZE 미달)으로 평균이 없는 경우 -> 판단 보류
                continue

            price = float(trade["price_per_pyeong"])
            deviation = round((price - apt_avg) / apt_avg * 100, 2)

            if abs(deviation) >= OUTLIER_THRESHOLD_RATE:
                outlier_records.append({
                    "apt_trade_id": trade["id"],
                    "sgg_cd": trade["sgg_cd"],
                    "apt_nm": trade["apt_nm"],
                    "deal_price_per_pyeong": price,
                    "region_avg_price_per_pyeong": apt_avg,
                    "deviation_rate": deviation,
                })
                outlier_ids.append(trade["id"])

        if outlier_records:
            with conn.cursor() as cursor:
                cursor.executemany(INSERT_OUTLIER_SQL, outlier_records)

                placeholders = ", ".join(["%s"] * len(outlier_ids))
                cursor.execute(UPDATE_FLAG_SQL.format(placeholders=placeholders), outlier_ids)

            conn.commit()

        print(
            f"[이상거래 탐지 완료] 단지 평균 대비 ±{OUTLIER_THRESHOLD_RATE}% 이상 거래 "
            f"{len(outlier_records)}건 신규 탐지 (최소 샘플 수 {MIN_SAMPLE_SIZE}건 미달 단지는 제외)"
        )

    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    detect_outliers()