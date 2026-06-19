"""
국토부 아파트 매매 API 응답 파싱
- item이 dict(단건) 또는 list(여러건)로 오는 경우 둘 다 처리
- 증분 적재용 dedup_key 생성
- deal_date(DATE), price_per_pyeong(평당가) 파생 필드 계산
"""

from datetime import date
from typing import List, Dict, Optional


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


def make_dedup_key(item: Dict) -> str:
    """
    증분 적재용 중복판별 키 생성
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


def _safe_int(value, default: int = 0) -> int:
    try:
        return int(str(value).replace(",", "").strip())
    except (ValueError, TypeError):
        return default


def _safe_float(value, default: float = 0.0) -> float:
    try:
        return float(str(value).strip())
    except (ValueError, TypeError):
        return default


def _build_deal_date(year: int, month: int, day: int) -> Optional[date]:
    try:
        return date(year, month, day)
    except (ValueError, TypeError):
        return None


def _calc_price_per_pyeong(deal_amount: int, exclu_use_ar: float) -> Optional[float]:
    """평당가 = 거래금액(만원) / (전용면적(㎡) / 3.3058)"""
    if not exclu_use_ar:
        return None
    pyeong = exclu_use_ar / 3.3058
    if pyeong == 0:
        return None
    return round(deal_amount / pyeong, 2)


def normalize_items_with_dedup_seq(raw_items: List[Dict]) -> List[Dict]:
    """
    한 번에 수집된 item 리스트를 정규화하면서,
    동일 dedup_key가 여러 번 나오면 끝에 일련번호를 붙여 구분한다.

    국토부 API는 호수(몇 호)를 제공하지 않기 때문에 같은 단지/동/층/면적/계약일/
    금액 조합이 실제로 다른 두 세대의 거래일 수 있다. 이를 단순 중복(skip)으로
    잘못 처리하지 않기 위해 같은 키가 N번째로 나오면 "_dupN"을 붙여 별개 거래로
    적재되도록 한다.
    """
    normalized = [normalize_item(item) for item in raw_items]

    seen_counts: Dict[str, int] = {}
    for record in normalized:
        base_key = record["dedup_key"]
        seen_counts[base_key] = seen_counts.get(base_key, 0) + 1
        seq = seen_counts[base_key]
        if seq > 1:
            record["dedup_key"] = f"{base_key}_dup{seq}"

    return normalized


def normalize_item(item: Dict) -> Dict:
    """문자열 필드를 적절한 타입으로 변환 + dedup_key, deal_date, price_per_pyeong 계산"""
    deal_year = _safe_int(item.get("dealYear"))
    deal_month = _safe_int(item.get("dealMonth"))
    deal_day = _safe_int(item.get("dealDay"))
    deal_amount = _safe_int(item.get("dealAmount"))
    exclu_use_ar = _safe_float(item.get("excluUseAr"))

    return {
        "dedup_key": make_dedup_key(item),
        "sgg_cd": item.get("sggCd"),
        "umd_nm": item.get("umdNm"),
        "apt_nm": item.get("aptNm"),
        "apt_dong": item.get("aptDong"),
        "jibun": item.get("jibun"),
        "exclu_use_ar": exclu_use_ar,
        "deal_year": deal_year,
        "deal_month": deal_month,
        "deal_day": deal_day,
        "deal_date": _build_deal_date(deal_year, deal_month, deal_day),
        "deal_amount": deal_amount,
        "price_per_pyeong": _calc_price_per_pyeong(deal_amount, exclu_use_ar),
        "floor": _safe_int(item.get("floor")),
        "build_year": _safe_int(item.get("buildYear")),
        "dealing_gbn": item.get("dealingGbn"),
        "sler_gbn": item.get("slerGbn"),
        "buyer_gbn": item.get("buyerGbn"),
        "cdeal_type": item.get("cdealType") or None,
        "cdeal_day": item.get("cdealDay") or None,
        "estate_agent_sgg_nm": item.get("estateAgentSggNm"),
        "land_leasehold_gbn": item.get("landLeaseholdGbn"),
    }