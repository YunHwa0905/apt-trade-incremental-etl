"""
1단계 테스트: 서울 종로구 한 달치 데이터 호출 + 파싱 결과 확인
실행: python test_step1.py
"""

from collector.api_client import fetch_apt_trade
from collector.parser import parse_items, normalize_item

def main():
    lawd_cd = "11110"  # 종로구
    deal_ymd = "202506"  # 2025년 6월

    print(f"[테스트] 종로구(11110) {deal_ymd} 데이터 조회 중...")
    raw_data = fetch_apt_trade(lawd_cd, deal_ymd)

    header = raw_data.get("response", {}).get("header", {})
    print(f"resultCode: {header.get('resultCode')} / resultMsg: {header.get('resultMsg')}")

    items = parse_items(raw_data)
    print(f"\n총 {len(items)}건 조회됨\n")

    if not items:
        print("⚠️ 조회된 데이터가 없습니다. 해당 월에 거래가 없거나 파라미터를 확인하세요.")
        return

    print("--- 정규화된 데이터 샘플 (앞 3건) ---")
    for raw_item in items[:3]:
        normalized = normalize_item(raw_item)
        for key, value in normalized.items():
            print(f"  {key}: {value}")
        print()


if __name__ == "__main__":
    main()