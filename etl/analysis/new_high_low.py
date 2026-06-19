"""
단지별 신고가/신저가 탐지
- 같은 단지(apt_nm + sgg_cd) 내에서 거래일 순으로 평당가를 비교
- 직전까지의 최고가를 넘으면 HIGH, 최저가보다 낮으면 LOW로 기록
- new_high_low_history 테이블에 기록 (이미 기록된 apt_trade_id는 재기록하지 않음)

실행: python -m analysis.new_high_low
"""

from db.connection import get_connection


SELECT_TRADES_SQL = """
SELECT id, apt_nm, sgg_cd, price_per_pyeong, deal_date
FROM apt_trade
WHERE price_per_pyeong IS NOT NULL
ORDER BY apt_nm, sgg_cd, deal_date ASC, id ASC
"""

SELECT_ALREADY_RECORDED_SQL = """
SELECT apt_trade_id FROM new_high_low_history
"""

INSERT_SQL = """
INSERT INTO new_high_low_history (
    apt_trade_id, apt_nm, sgg_cd, record_type, price_per_pyeong, deal_date
) VALUES (
    %(apt_trade_id)s, %(apt_nm)s, %(sgg_cd)s, %(record_type)s, %(price_per_pyeong)s, %(deal_date)s
)
"""


def detect_new_high_low():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(SELECT_TRADES_SQL)
            trades = cursor.fetchall()

            cursor.execute(SELECT_ALREADY_RECORDED_SQL)
            already_recorded = {row["apt_trade_id"] for row in cursor.fetchall()}

        # 단지(apt_nm + sgg_cd) 별로 그룹화하면서 거래일 순으로 최고/최저가 추적
        tracker = {}  # (apt_nm, sgg_cd) -> {"max": float, "min": float}
        new_records = []

        for trade in trades:
            if trade["id"] in already_recorded:
                # 이미 신고가/신저가 판정이 끝난 거래는 추적용 최대/최소값만 갱신하고 스킵
                key = (trade["apt_nm"], trade["sgg_cd"])
                price = float(trade["price_per_pyeong"])
                state = tracker.setdefault(key, {"max": price, "min": price})
                state["max"] = max(state["max"], price)
                state["min"] = min(state["min"], price)
                continue

            key = (trade["apt_nm"], trade["sgg_cd"])
            price = float(trade["price_per_pyeong"])
            state = tracker.get(key)

            if state is None:
                # 해당 단지 첫 거래 -> 기준값만 설정, 기록은 안 함
                tracker[key] = {"max": price, "min": price}
                continue

            if price > state["max"]:
                new_records.append({
                    "apt_trade_id": trade["id"],
                    "apt_nm": trade["apt_nm"],
                    "sgg_cd": trade["sgg_cd"],
                    "record_type": "HIGH",
                    "price_per_pyeong": price,
                    "deal_date": trade["deal_date"],
                })
                state["max"] = price

            elif price < state["min"]:
                new_records.append({
                    "apt_trade_id": trade["id"],
                    "apt_nm": trade["apt_nm"],
                    "sgg_cd": trade["sgg_cd"],
                    "record_type": "LOW",
                    "price_per_pyeong": price,
                    "deal_date": trade["deal_date"],
                })
                state["min"] = price

        if new_records:
            with conn.cursor() as cursor:
                cursor.executemany(INSERT_SQL, new_records)
            conn.commit()

        high_count = sum(1 for r in new_records if r["record_type"] == "HIGH")
        low_count = sum(1 for r in new_records if r["record_type"] == "LOW")
        print(f"[신고가/신저가 탐지 완료] 신고가 {high_count}건 / 신저가 {low_count}건 신규 기록")

    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    detect_new_high_low()