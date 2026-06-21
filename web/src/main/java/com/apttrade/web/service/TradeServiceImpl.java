package com.apttrade.web.service;

import com.apttrade.web.mapper.TradeMapper;
import com.apttrade.web.vo.AptTradeVO;
import com.apttrade.web.vo.TradeSearchCondition;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class TradeServiceImpl implements TradeService {

	@Autowired
	private TradeMapper tradeMapper;

	@Override
	public Map<String, Object> getTradeList(TradeSearchCondition condition) {
		List<AptTradeVO> list = tradeMapper.selectTradeList(condition);
		int totalCount = tradeMapper.countTradeList(condition);
		int totalPages = (int) Math.ceil((double) totalCount / condition.getPageSize());

		Map<String, Object> result = new HashMap<>();
		result.put("list", list);
		result.put("totalCount", totalCount);
		result.put("totalPages", totalPages);
		result.put("currentPage", condition.getPage());

		return result;
	}

	@Override
	public AptTradeVO getTradeDetail(Long id) {
		return tradeMapper.selectTradeById(id);
	}
}