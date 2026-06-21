package com.apttrade.web.service;

import com.apttrade.web.vo.AptTradeVO;
import com.apttrade.web.vo.TradeSearchCondition;

import java.util.List;
import java.util.Map;

public interface TradeService {

	/**
	 * 검색조건에 맞는 거래 목록 + 페이징 정보를 함께 반환
	 * 
	 * @return {"list": List<AptTradeVO>, "totalCount": int, "totalPages": int}
	 */
	Map<String, Object> getTradeList(TradeSearchCondition condition);

	AptTradeVO getTradeDetail(Long id);
}