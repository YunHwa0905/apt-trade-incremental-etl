package com.apttrade.web.mapper;

import com.apttrade.web.vo.MonthlyPriceSummaryVO;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

@Mapper
public interface PriceTrendMapper {

	/**
	 * 특정 지역(sggCd)의 월별 가격추이 전체 조회 (시간순 정렬) sggCd가 null이면 서울 전체(구 구분 없이) 합산 추이 조회용으로
	 * 사용 가능
	 */
	List<MonthlyPriceSummaryVO> selectMonthlyTrendByRegion(@Param("sggCd") String sggCd);

	/**
	 * 구별 드롭다운/필터용 - 데이터가 존재하는 구 목록만 조회
	 */
	List<MonthlyPriceSummaryVO> selectDistinctRegions();
}