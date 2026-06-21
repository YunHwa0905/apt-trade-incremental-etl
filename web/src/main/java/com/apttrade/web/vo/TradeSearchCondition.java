package com.apttrade.web.vo;

import lombok.Data;

/**
 * 실거래 목록 검색 조건
 */
@Data
public class TradeSearchCondition {

	private String sggCd; // 법정동코드 (구 단위), null이면 전체
	private String aptNm; // 단지명 검색 (LIKE), null이면 전체
	private Integer dealYear; // 거래연도, null이면 전체
	private Integer dealMonth; // 거래월, null이면 전체

	// 페이징
	private Integer page = 1;
	private Integer pageSize = 20;

	public int getOffset() {
		return (page - 1) * pageSize;
	}
}