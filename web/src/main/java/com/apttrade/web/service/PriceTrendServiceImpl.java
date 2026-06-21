package com.apttrade.web.service;

import com.apttrade.web.mapper.PriceTrendMapper;
import com.apttrade.web.vo.MonthlyPriceSummaryVO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class PriceTrendServiceImpl implements PriceTrendService {

	@Autowired
	private PriceTrendMapper priceTrendMapper;

	@Override
	public List<MonthlyPriceSummaryVO> getMonthlyTrend(String sggCd) {
		return priceTrendMapper.selectMonthlyTrendByRegion(sggCd);
	}

	@Override
	public List<MonthlyPriceSummaryVO> getRegionList() {
		return priceTrendMapper.selectDistinctRegions();
	}
}