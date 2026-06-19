"""
서울 25개구 x 2023.01 ~ 2025.06 (30개월) 전체 백필
- 중간에 끊겨도 backfill_progress.json 기준으로 이어서 실행 가능
- 호출 사이 짧은 지연을 둬서 API 서버 부담/요청제한 방지

실행: python backfill.py
"""

import time
import sys
from datetime import date

from collector.api_client import fetch_apt_trade
from collector.parser import parse_items, normalize_items_with_dedup_seq
from collector.region_codes import SEOUL_DISTRICTS
from db.repository import insert_trades_incremental
from backfill_progress import load_progress, mark_done

# ===== 설정 =====
START_YEAR_MONTH = (2023, 1)
END_YEAR_MONTH = (2025, 6)
REQUEST_DELAY_SEC = 0.3   # 호출 사이 대기시간 (요청제한 방지)
MAX_RETRY = 3


def generate_year_months(start: tuple, end: tuple) -> list:
    """(2023,1) ~ (2025,6) 사이의 모든 (year, month) 리스트 생성"""
    result = []
    y, m = start
    while (y, m) <= end:
        result.append((y, m))
        m += 1
        if m > 12:
            m = 1
            y += 1
    return result


def fetch_with_retry(lawd_cd: str, deal_ymd: str, max_retry: int = MAX_RETRY) -> dict:
    """일시적 오류 대비 재시도 로직"""
    last_error = None
    for attempt in range(1, max_retry + 1):
        try:
            return fetch_apt_trade(lawd_cd, deal_ymd)
        except Exception as e:
            last_error = e
            print(f"    ⚠️ 시도 {attempt}/{max_retry} 실패: {e}")
            time.sleep(1.5 * attempt)  # 점점 길게 대기 후 재시도
    raise last_error


def main():
    year_months = generate_year_months(START_YEAR_MONTH, END_YEAR_MONTH)
    done = load_progress()

    total_tasks = len(SEOUL_DISTRICTS) * len(year_months)
    task_idx = 0

    total_inserted = 0
    total_skipped = 0
    failed_tasks = []

    print(f"[백필 시작] 서울 25개구 x {len(year_months)}개월 = 총 {total_tasks}건 작업")
    print(f"[이미 완료됨] {len(done)}건 (이어서 진행)\n")

    start_time = time.time()

    for lawd_cd, district_name in SEOUL_DISTRICTS.items():
        for (y, m) in year_months:
            task_idx += 1
            deal_ymd = f"{y}{m:02d}"
            key = (lawd_cd, deal_ymd)

            if key in done:
                continue  # 이미 처리됨 -> 스킵

            progress_label = f"[{task_idx}/{total_tasks}] {district_name}({lawd_cd}) {deal_ymd}"

            try:
                raw_data = fetch_with_retry(lawd_cd, deal_ymd)
                items = parse_items(raw_data)
                records = normalize_items_with_dedup_seq(items)
                result = insert_trades_incremental(records)

                total_inserted += result["inserted"]
                total_skipped += result["skipped"]

                print(f"{progress_label} -> {len(items)}건 수신 / 신규 {result['inserted']} / 중복 {result['skipped']}")

                mark_done(done, lawd_cd, deal_ymd)
                time.sleep(REQUEST_DELAY_SEC)

            except Exception as e:
                print(f"{progress_label} -> ❌ 최종 실패: {e}")
                failed_tasks.append(key)
                # 실패해도 계속 진행 (done에는 추가 안 함 -> 재실행 시 다시 시도됨)

    elapsed = time.time() - start_time

    print("\n" + "=" * 50)
    print("[백필 완료]")
    print(f"총 신규 적재: {total_inserted}건")
    print(f"총 중복 skip: {total_skipped}건")
    print(f"실패 건수: {len(failed_tasks)}건")
    print(f"소요 시간: {elapsed/60:.1f}분")

    if failed_tasks:
        print("\n실패한 작업 목록 (재실행하면 자동으로 다시 시도됩니다):")
        for lawd_cd, deal_ymd in failed_tasks:
            print(f"  - {SEOUL_DISTRICTS.get(lawd_cd)}({lawd_cd}) {deal_ymd}")
        sys.exit(1)


if __name__ == "__main__":
    main()