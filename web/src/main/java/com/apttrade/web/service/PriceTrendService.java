package com.apttrade.web.service;

import com.apttrade.web.vo.MonthlyPriceSummaryVO;

import java.util.List;

public interface PriceTrendService {

	List<MonthlyPriceSummaryVO> getMonthlyTrend(String sggCd);

	List<MonthlyPriceSummaryVO> getRegionList();
}