package com.apttrade.web.vo;

import lombok.Data;

@Data
public class OutlierTradeVO {
	private Long id;
	private Long aptTradeId;
	private String sggCd;
	private String sggNm;
	private String aptNm;
	private Double dealPricePerPyeong;
	private Double regionAvgPricePerPyeong; // 실제로는 "단지 평균" 값이 들어있음
	private Double deviationRate;

	// apt_trade 조인으로 채워지는 부가 정보 (화면 표시용)
	private String dealingGbn;
	private String slerGbn;
	private String buyerGbn;
	private java.time.LocalDate dealDate;
}