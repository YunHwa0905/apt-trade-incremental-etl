package com.apttrade.web.service;

import com.apttrade.web.vo.DetectionSearchCondition;

import java.util.Map;

public interface DetectionService {

	Map<String, Object> getNewHighLowList(DetectionSearchCondition condition);

	Map<String, Object> getOutlierList(DetectionSearchCondition condition);
}