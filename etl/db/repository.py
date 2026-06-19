"""
apt_trade 테이블 증분 적재 로직
- dedup_key가 이미 존재하면 INSERT 무시 (INSERT IGNORE)
- 한 번에 여러 row를 executemany로 적재 (성능 + 코드 단순화)
"""

from typing import List, Dict
from db.connection import get_connection


INSERT_SQL = """
INSERT IGNORE INTO apt_trade (
    dedup_key, sgg_cd, umd_nm, apt_nm, apt_dong, jibun,
    exclu_use_ar, deal_year, deal_month, deal_day, deal_date,
    deal_amount, price_per_pyeong, floor, build_year,
    dealing_gbn, sler_gbn, buyer_gbn,
    cdeal_type, cdeal_day, estate_agent_sgg_nm, land_leasehold_gbn
) VALUES (
    %(dedup_key)s, %(sgg_cd)s, %(umd_nm)s, %(apt_nm)s, %(apt_dong)s, %(jibun)s,
    %(exclu_use_ar)s, %(deal_year)s, %(deal_month)s, %(deal_day)s, %(deal_date)s,
    %(deal_amount)s, %(price_per_pyeong)s, %(floor)s, %(build_year)s,
    %(dealing_gbn)s, %(sler_gbn)s, %(buyer_gbn)s,
    %(cdeal_type)s, %(cdeal_day)s, %(estate_agent_sgg_nm)s, %(land_leasehold_gbn)s
)
"""


def insert_trades_incremental(records: List[Dict]) -> Dict[str, int]:
    """
    여러 거래 레코드를 증분 적재.

    :param records: normalize_item()을 통과한 dict 리스트
    :return: {"attempted": N, "inserted": M, "skipped": N-M}
    """
    if not records:
        return {"attempted": 0, "inserted": 0, "skipped": 0}

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # executemany는 INSERT IGNORE의 실제 삽입 건수를 정확히 반환하지 않을 수 있어
            # 건별로 처리해 정확한 신규/중복 카운트를 잡는다.
            inserted = 0
            for record in records:
                cursor.execute(INSERT_SQL, record)
                inserted += cursor.rowcount  # 1이면 신규삽입, 0이면 중복(skip)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    attempted = len(records)
    return {
        "attempted": attempted,
        "inserted": inserted,
        "skipped": attempted - inserted,
    }