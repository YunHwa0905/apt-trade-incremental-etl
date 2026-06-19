"""
국토부 아파트 매매 API 응답 파싱
- item이 dict(단건) 또는 list(여러건)로 오는 경우 둘 다 처리
- 증분 적재용 unique_key 생성
"""

from typing import List, Dict


def parse_items(raw_data: dict) -> List[Dict]:
    """API 응답에서 item 리스트만 추출"""
    body = raw_data.get("response", {}).get("body", {})
    items = body.get("items", {})

    if not items:
        return []

    item_list = items.get("item", [])

    # 결과가 1건일 때 dict로 오는 경우 보정
    if isinstance(item_list, dict):
        item_list = [item_list]

    return item_list


def make_unique_key(item: Dict) -> str:
    """
    증분 적재용 유니크 키 생성
    같은 (법정동+지번+단지명+동+층+면적+계약일+거래금액) 조합이면 동일 거래로 간주
    """
    parts = [
        item.get("sggCd", ""),
        item.get("umdNm", ""),
        item.get("jibun", ""),
        item.get("aptNm", ""),
        item.get("aptDong", ""),
        item.get("floor", ""),
        item.get("excluUseAr", ""),
        item.get("dealYear", ""),
        item.get("dealMonth", ""),
        item.get("dealDay", ""),
        item.get("dealAmount", ""),
    ]
    return "_".join(str(p).strip() for p in parts)


def normalize_item(item: Dict) -> Dict:
    """문자열 필드를 적절한 타입으로 변환 + unique_key 추가"""
    return {
        "unique_key": make_unique_key(item),
        "sgg_cd": item.get("sggCd"),
        "umd_nm": item.get("umdNm"),
        "apt_nm": item.get("aptNm"),
        "apt_dong": item.get("aptDong"),
        "jibun": item.get("jibun"),
        "exclu_use_ar": float(item.get("excluUseAr", 0) or 0),
        "deal_year": int(item.get("dealYear", 0) or 0),
        "deal_month": int(item.get("dealMonth", 0) or 0),
        "deal_day": int(item.get("dealDay", 0) or 0),
        "deal_amount": int(str(item.get("dealAmount", "0")).replace(",", "").strip() or 0),
        "floor": int(item.get("floor", 0) or 0),
        "build_year": int(item.get("buildYear", 0) or 0),
        "dealing_gbn": item.get("dealingGbn"),
        "sler_gbn": item.get("slerGbn"),
        "buyer_gbn": item.get("buyerGbn"),
        "cdeal_type": item.get("cdealType"),
        "cdeal_day": item.get("cdealDay"),
        "estate_agent_sgg_nm": item.get("estateAgentSggNm"),
        "land_leasehold_gbn": item.get("landLeaseholdGbn"),
    }