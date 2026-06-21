package com.apttrade.web.controller;

import com.apttrade.web.service.PriceTrendService;
import com.apttrade.web.vo.MonthlyPriceSummaryVO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.List;

@Controller
@RequestMapping("/price-trend")
public class PriceTrendController {

	@Autowired
	private PriceTrendService priceTrendService;

	/**
	 * 가격추이 화면 (최초 진입, 구 목록 드롭다운 채우기용)
	 */
	@RequestMapping(value = "", method = RequestMethod.GET)
	public String page(Model model) {
		List<MonthlyPriceSummaryVO> regions = priceTrendService.getRegionList();
		model.addAttribute("regions", regions);
		return "price_trend"; // -> /WEB-INF/views/price_trend.jsp
	}

	/**
	 * 차트용 데이터 API (Ajax) 예: /price-trend/data?sggCd=11680
	 */
	@RequestMapping(value = "/data", method = RequestMethod.GET)
	@ResponseBody
	public List<MonthlyPriceSummaryVO> data(@RequestParam(required = false) String sggCd) {
		return priceTrendService.getMonthlyTrend(sggCd);
	}
}