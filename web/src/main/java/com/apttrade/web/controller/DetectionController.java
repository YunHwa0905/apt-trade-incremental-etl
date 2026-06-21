package com.apttrade.web.controller;

import com.apttrade.web.service.DetectionService;
import com.apttrade.web.vo.DetectionSearchCondition;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import java.util.Map;

@Controller
@RequestMapping("/detection")
public class DetectionController {

	@Autowired
	private DetectionService detectionService;

	private static final int PAGE_BLOCK = 5;

	/**
	 * 신고가/신저가 목록 화면 예: /detection/high-low?sggCd=11680&recordType=HIGH&page=1
	 */
	@RequestMapping(value = "/high-low", method = RequestMethod.GET)
	public String highLow(@ModelAttribute DetectionSearchCondition condition, Model model) {
		Map<String, Object> result = detectionService.getNewHighLowList(condition);
		addPagingAttributes(model, result, condition);
		return "high_low"; // -> /WEB-INF/views/high_low.jsp
	}

	/**
	 * 이상거래 목록 화면 예: /detection/outlier?sggCd=11680&page=1
	 */
	@RequestMapping(value = "/outlier", method = RequestMethod.GET)
	public String outlier(@ModelAttribute DetectionSearchCondition condition, Model model) {
		Map<String, Object> result = detectionService.getOutlierList(condition);
		addPagingAttributes(model, result, condition);
		return "outlier"; // -> /WEB-INF/views/outlier.jsp
	}

	private void addPagingAttributes(Model model, Map<String, Object> result, DetectionSearchCondition condition) {
		int currentPage = condition.getPage();
		int totalPages = (int) result.get("totalPages");

		int blockIndex = (currentPage - 1) / PAGE_BLOCK;
		int startPage = blockIndex * PAGE_BLOCK + 1;
		int endPage = Math.min(startPage + PAGE_BLOCK - 1, totalPages);

		model.addAttribute("list", result.get("list"));
		model.addAttribute("totalCount", result.get("totalCount"));
		model.addAttribute("totalPages", totalPages);
		model.addAttribute("currentPage", currentPage);
		model.addAttribute("startPage", startPage);
		model.addAttribute("endPage", endPage);
		model.addAttribute("condition", condition);
	}
}