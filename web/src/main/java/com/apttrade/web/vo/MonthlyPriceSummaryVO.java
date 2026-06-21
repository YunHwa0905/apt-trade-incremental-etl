package com.apttrade.web.vo;

import lombok.Data;

/**
 * monthly_price_summary 테이블 매핑 VO
 */
@Data
public class MonthlyPriceSummaryVO {

	private Long id;
	private String sggCd;
	private String sggNm;
	private Integer dealYear;
	private Integer dealMonth;

	private Integer tradeCount;
	private Long avgPrice;
	private Double avgPricePerPyeong;
	private Double priceChangeRate;
}