"""
백필 진행 상태 관리
- 이미 처리 완료한 (지역코드, 계약년월) 조합을 파일에 기록
- 중간에 스크립트가 끊겨도 재실행 시 처리된 부분은 건너뜀
"""

import json
import os

PROGRESS_FILE = os.path.join(os.path.dirname(__file__), "backfill_progress.json")


def load_progress() -> set:
    """완료된 (lawd_cd, deal_ymd) 조합 집합 로드"""
    if not os.path.exists(PROGRESS_FILE):
        return set()
    with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return set(tuple(item) for item in data)


def save_progress(done_set: set):
    """완료된 조합 집합을 파일로 저장"""
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(done_set), f, ensure_ascii=False)


def mark_done(done_set: set, lawd_cd: str, deal_ymd: str):
    """한 건 완료 표시 + 즉시 파일에 반영 (중간에 끊겨도 안전하게)"""
    done_set.add((lawd_cd, deal_ymd))
    save_progress(done_set)