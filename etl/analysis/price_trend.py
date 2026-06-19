"""
지역별 월별 가격 추이 집계
- apt_trade 원본 데이터를 sgg_cd + 연/월 기준으로 GROUP BY
- monthly_price_summary 테이블에 집계 결과 저장 (UPSERT)
- 전월 대비 변동률(price_change_rate)도 함께 계산

실행: python -m analysis.price_trend
"""

from db.connection import get_connection
from collector.region_codes import SEOUL_DISTRICTS


SELECT_MONTHLY_AGG_SQL = """
SELECT
    sgg_cd,
    deal_year,
    deal_month,
    COUNT(*) AS trade_count,
    ROUND(AVG(deal_amount)) AS avg_price,
    ROUND(AVG(price_per_pyeong), 2) AS avg_price_per_pyeong
FROM apt_trade
WHERE price_per_pyeong IS NOT NULL
GROUP BY sgg_cd, deal_year, deal_month
ORDER BY sgg_cd, deal_year, deal_month
"""

UPSERT_SQL = """
INSERT INTO monthly_price_summary (
    sgg_cd, sgg_nm, deal_year, deal_month,
    trade_count, avg_price, avg_price_per_pyeong, price_change_rate
) VALUES (
    %(sgg_cd)s, %(sgg_nm)s, %(deal_year)s, %(deal_month)s,
    %(trade_count)s, %(avg_price)s, %(avg_price_per_pyeong)s, %(price_change_rate)s
)
ON DUPLICATE KEY UPDATE
    trade_count = VALUES(trade_count),
    avg_price = VALUES(avg_price),
    avg_price_per_pyeong = VALUES(avg_price_per_pyeong),
    price_change_rate = VALUES(price_change_rate)
"""


def calc_price_trend():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(SELECT_MONTHLY_AGG_SQL)
            rows = cursor.fetchall()

        # 지역별로 시간순 정렬된 리스트를 만들어 전월대비 변동률 계산
        by_region = {}
        for row in rows:
            by_region.setdefault(row["sgg_cd"], []).append(row)

        upsert_records = []
        for sgg_cd, region_rows in by_region.items():
            # 이미 deal_year, deal_month 순으로 정렬되어 들어옴
            prev_price = None
            for row in region_rows:
                avg_ppp = float(row["avg_price_per_pyeong"]) if row["avg_price_per_pyeong"] else None

                change_rate = None
                if prev_price and avg_ppp:
                    change_rate = round((avg_ppp - prev_price) / prev_price * 100, 2)

                upsert_records.append({
                    "sgg_cd": sgg_cd,
                    "sgg_nm": SEOUL_DISTRICTS.get(sgg_cd, ""),
                    "deal_year": row["deal_year"],
                    "deal_month": row["deal_month"],
                    "trade_count": row["trade_count"],
                    "avg_price": row["avg_price"],
                    "avg_price_per_pyeong": avg_ppp,
                    "price_change_rate": change_rate,
                })

                if avg_ppp:
                    prev_price = avg_ppp

        with conn.cursor() as cursor:
            cursor.executemany(UPSERT_SQL, upsert_records)
        conn.commit()

        print(f"[가격추이 집계 완료] 총 {len(upsert_records)}개 (지역 x 월) 레코드 갱신")

    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    calc_price_trend()