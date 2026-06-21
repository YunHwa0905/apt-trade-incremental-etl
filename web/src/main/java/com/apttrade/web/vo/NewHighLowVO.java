package com.apttrade.web.vo;

import lombok.Data;
import java.time.LocalDate;

@Data
public class NewHighLowVO {
	private Long id;
	private Long aptTradeId;
	private String aptNm;
	private String sggCd;
	private String sggNm; // join으로 채워질 수 있음 (없으면 null)
	private String recordType; // HIGH / LOW
	private Double pricePerPyeong;
	private LocalDate dealDate;
}