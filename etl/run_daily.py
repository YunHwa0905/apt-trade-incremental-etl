"""
일별 증분 수집 스케줄러
- 매일 실행되어 "이번달 + 저번달" 데이터를 재조회
  (국토부 신고는 계약 후 30일 이내이므로, 신고가 늦게 들어온 건도 놓치지 않기 위함)
- dedup_key 기반 증분 적재라서 이미 적재된 건은 자동으로 skip됨
- 실행 결과를 로그 파일에 기록

crontab 등록 예시 (매일 오전 9시 실행):
    0 9 * * * cd /home/smt21/apt-trade-incremental-etl/etl && /usr/bin/python3 run_daily.py >> logs/cron.log 2>&1
"""

import os
import sys
import time
import logging
from datetime import date

from collector.api_client import fetch_apt_trade
from collector.parser import parse_items, normalize_items_with_dedup_seq
from collector.region_codes import SEOUL_DISTRICTS
from db.repository import insert_trades_incremental

REQUEST_DELAY_SEC = 0.3
MAX_RETRY = 3

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# 날짜별 로그 파일 (예: logs/2025-06-19.log)
log_filename = os.path.join(LOG_DIR, f"{date.today().isoformat()}.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_filename, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


def get_target_year_months() -> list:
    """오늘 기준 이번달 + 저번달 (year, month) 튜플 리스트"""
    today = date.today()
    y, m = today.year, today.month

    prev_m = m - 1
    prev_y = y
    if prev_m == 0:
        prev_m = 12
        prev_y -= 1

    return [(prev_y, prev_m), (y, m)]


def fetch_with_retry(lawd_cd: str, deal_ymd: str, max_retry: int = MAX_RETRY) -> dict:
    last_error = None
    for attempt in range(1, max_retry + 1):
        try:
            return fetch_apt_trade(lawd_cd, deal_ymd)
        except Exception as e:
            last_error = e
            logger.warning(f"    재시도 {attempt}/{max_retry} 실패: {e}")
            time.sleep(1.5 * attempt)
    raise last_error


def main():
    year_months = get_target_year_months()
    deal_ymds = [f"{y}{m:02d}" for (y, m) in year_months]

    logger.info(f"===== 일별 증분 수집 시작 (대상 월: {', '.join(deal_ymds)}) =====")

    total_received = 0
    total_inserted = 0
    total_skipped = 0
    failed = []

    for lawd_cd, district_name in SEOUL_DISTRICTS.items():
        for deal_ymd in deal_ymds:
            try:
                raw_data = fetch_with_retry(lawd_cd, deal_ymd)
                items = parse_items(raw_data)
                records = normalize_items_with_dedup_seq(items)
                result = insert_trades_incremental(records)

                total_received += len(items)
                total_inserted += result["inserted"]
                total_skipped += result["skipped"]

                if result["inserted"] > 0:
                    logger.info(
                        f"{district_name}({lawd_cd}) {deal_ymd} "
                        f"-> 수신 {len(items)} / 신규 {result['inserted']} / 중복 {result['skipped']}"
                    )

                time.sleep(REQUEST_DELAY_SEC)

            except Exception as e:
                logger.error(f"{district_name}({lawd_cd}) {deal_ymd} -> 실패: {e}")
                failed.append((lawd_cd, deal_ymd))

    logger.info("=" * 50)
    logger.info(f"[일별 수집 완료] 수신 {total_received} / 신규 {total_inserted} / 중복 {total_skipped} / 실패 {len(failed)}")

    if failed:
        logger.error(f"실패 목록: {failed}")
        sys.exit(1)


if __name__ == "__main__":
    main()