package com.apttrade.web.vo;

import lombok.Data;

@Data
public class DetectionSearchCondition {

	private String sggCd; // 구 필터, null이면 전체
	private String recordType; // HIGH / LOW / null(전체) - 신고가/신저가 화면에서만 사용

	private Integer page = 1;
	private Integer pageSize = 20;

	public int getOffset() {
		return (page - 1) * pageSize;
	}
}