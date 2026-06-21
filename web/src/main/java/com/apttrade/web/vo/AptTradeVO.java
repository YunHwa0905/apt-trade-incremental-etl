package com.apttrade.web.vo;

import lombok.Data;
import java.time.LocalDate;

/**
 * apt_trade 테이블 매핑 VO
 */
@Data
public class AptTradeVO {

	private Long id;
	private String dedupKey;

	private String sggCd;
	private String umdNm;
	private String aptNm;
	private String aptDong;
	private String jibun;

	private Double excluUseAr;

	private Integer dealYear;
	private Integer dealMonth;
	private Integer dealDay;
	private LocalDate dealDate;

	private Long dealAmount;
	private Double pricePerPyeong;

	private Integer floor;
	private Integer buildYear;

	private String dealingGbn;
	private String slerGbn;
	private String buyerGbn;

	private String cdealType;
	private String cdealDay;

	private String estateAgentSggNm;
	private String landLeaseholdGbn;

	private Boolean isOutlier;
}