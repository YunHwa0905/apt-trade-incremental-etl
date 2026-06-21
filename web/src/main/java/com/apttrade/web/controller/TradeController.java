package com.apttrade.web.controller;

import com.apttrade.web.service.TradeService;
import com.apttrade.web.vo.TradeSearchCondition;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import java.util.Map;

@Controller
@RequestMapping("/trade")
public class TradeController {

	@Autowired
	private TradeService tradeService;

	/**
	 * 실거래 목록 화면 예: /trade/list?sggCd=11680&page=1
	 */
	@RequestMapping(value = "/list", method = RequestMethod.GET)
	public String list(@ModelAttribute TradeSearchCondition condition, Model model) {
		Map<String, Object> result = tradeService.getTradeList(condition);

		int currentPage = condition.getPage();
		int totalPages = (int) result.get("totalPages");

		// 페이지네이션 블록(한 화면에 보여줄 페이지 번호 개수) 계산
		final int pageBlock = 5;
		int blockIndex = (currentPage - 1) / pageBlock; // 정수 나눗셈
		int startPage = blockIndex * pageBlock + 1;
		int endPage = Math.min(startPage + pageBlock - 1, totalPages);

		model.addAttribute("tradeList", result.get("list"));
		model.addAttribute("totalCount", result.get("totalCount"));
		model.addAttribute("totalPages", totalPages);
		model.addAttribute("currentPage", currentPage);
		model.addAttribute("startPage", startPage);
		model.addAttribute("endPage", endPage);
		model.addAttribute("condition", condition);

		return "list"; // -> /WEB-INF/views/list.jsp
	}
}