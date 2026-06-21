package com.apttrade.web.mapper;

import com.apttrade.web.vo.DetectionSearchCondition;
import com.apttrade.web.vo.NewHighLowVO;
import com.apttrade.web.vo.OutlierTradeVO;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;

@Mapper
public interface DetectionMapper {

	List<NewHighLowVO> selectNewHighLowList(DetectionSearchCondition condition);

	int countNewHighLowList(DetectionSearchCondition condition);

	List<OutlierTradeVO> selectOutlierList(DetectionSearchCondition condition);

	int countOutlierList(DetectionSearchCondition condition);
}