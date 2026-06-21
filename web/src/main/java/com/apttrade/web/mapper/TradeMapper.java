package com.apttrade.web.mapper;

import com.apttrade.web.vo.AptTradeVO;
import com.apttrade.web.vo.TradeSearchCondition;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;

@Mapper
public interface TradeMapper {

	/**
	 * 검색 조건에 맞는 거래 목록 조회 (페이징 적용)
	 */
	List<AptTradeVO> selectTradeList(TradeSearchCondition condition);

	/**
	 * 검색 조건에 맞는 전체 건수 조회 (페이징 처리용)
	 */
	int countTradeList(TradeSearchCondition condition);

	/**
	 * 단건 상세 조회
	 */
	AptTradeVO selectTradeById(Long id);
}