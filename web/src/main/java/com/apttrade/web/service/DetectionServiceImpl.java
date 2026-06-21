package com.apttrade.web.service;

import com.apttrade.web.mapper.DetectionMapper;
import com.apttrade.web.vo.DetectionSearchCondition;
import com.apttrade.web.vo.NewHighLowVO;
import com.apttrade.web.vo.OutlierTradeVO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class DetectionServiceImpl implements DetectionService {

	@Autowired
	private DetectionMapper detectionMapper;

	@Override
	public Map<String, Object> getNewHighLowList(DetectionSearchCondition condition) {
		List<NewHighLowVO> list = detectionMapper.selectNewHighLowList(condition);
		int totalCount = detectionMapper.countNewHighLowList(condition);
		return buildPagedResult(list, totalCount, condition);
	}

	@Override
	public Map<String, Object> getOutlierList(DetectionSearchCondition condition) {
		List<OutlierTradeVO> list = detectionMapper.selectOutlierList(condition);
		int totalCount = detectionMapper.countOutlierList(condition);
		return buildPagedResult(list, totalCount, condition);
	}

	private Map<String, Object> buildPagedResult(List<?> list, int totalCount, DetectionSearchCondition condition) {
		int totalPages = (int) Math.ceil((double) totalCount / condition.getPageSize());

		Map<String, Object> result = new HashMap<>();
		result.put("list", list);
		result.put("totalCount", totalCount);
		result.put("totalPages", totalPages);
		result.put("currentPage", condition.getPage());
		return result;
	}
}