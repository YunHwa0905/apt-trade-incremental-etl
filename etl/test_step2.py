"""
2단계 테스트: 종로구 한 달치 데이터를 실제로 DB에 증분 적재
실행: python test_step2.py
같은 명령을 두 번 실행해도 두 번째는 전부 skipped로 나와야 증분 적재가 정상 동작하는 것
"""

from collector.api_client import fetch_apt_trade
from collector.parser import parse_items, normalize_items_with_dedup_seq
from db.repository import insert_trades_incremental


def main():
    lawd_cd = "11110"  # 종로구
    deal_ymd = "202506"

    print(f"[1] API 호출: 종로구(11110) {deal_ymd}")
    raw_data = fetch_apt_trade(lawd_cd, deal_ymd)
    items = parse_items(raw_data)
    print(f"    -> {len(items)}건 수신")

    print("[2] 정규화 중... (동일 키 중복 시 일련번호 부여)")
    records = normalize_items_with_dedup_seq(items)

    print("[3] DB 증분 적재 중...")
    result = insert_trades_incremental(records)

    print("\n=== 적재 결과 ===")
    print(f"시도   : {result['attempted']}건")
    print(f"신규   : {result['inserted']}건")
    print(f"중복(skip): {result['skipped']}건")


if __name__ == "__main__":
    main()