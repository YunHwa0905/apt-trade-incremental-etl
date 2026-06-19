"""
국토교통부 아파트 매매 실거래가 상세 자료 API 클라이언트
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERVICE_KEY = os.environ.get("SERVICE_KEY")
BASE_URL = "http://apis.data.go.kr/1613000/RTMSDataSvcAptTrade/getRTMSDataSvcAptTrade"


def fetch_apt_trade(lawd_cd: str, deal_ymd: str, num_of_rows: int = 1000, page_no: int = 1) -> dict:
    """
    아파트 매매 실거래가 상세 자료 조회

    :param lawd_cd: 법정동 코드 앞 5자리 (예: 종로구 11110)
    :param deal_ymd: 계약년월 6자리 (예: 202506)
    :param num_of_rows: 한 페이지 결과 수 (최대치로 설정해 페이지네이션 최소화)
    :param page_no: 페이지 번호
    :return: 응답 JSON (dict)
    """
    if not SERVICE_KEY:
        raise ValueError("SERVICE_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")

    params = {
        "serviceKey": SERVICE_KEY,
        "LAWD_CD": lawd_cd,
        "DEAL_YMD": deal_ymd,
        "numOfRows": num_of_rows,
        "pageNo": page_no,
        "_type": "json",
    }

    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()

    try:
        return response.json()
    except ValueError:
        raise ValueError(f"JSON 파싱 실패. 응답 내용: {response.text[:500]}")


if __name__ == "__main__":
    # 단독 실행 시 테스트
    data = fetch_apt_trade("11110", "202506")
    header = data.get("response", {}).get("header", {})
    body = data.get("response", {}).get("body", {})

    print(f"resultCode: {header.get('resultCode')}")
    print(f"resultMsg: {header.get('resultMsg')}")
    print(f"totalCount: {body.get('totalCount')}")