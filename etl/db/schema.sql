-- ============================================
-- 서울 아파트 실거래가 증분 적재 DB 스키마
-- DB: apt_trade
-- ============================================

CREATE DATABASE IF NOT EXISTS apt_trade
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE apt_trade;

-- ============================================
-- 1. 원본 거래 데이터 적재 테이블
-- ============================================
CREATE TABLE IF NOT EXISTS apt_trade (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,

    -- 증분 적재 핵심: 이 값이 중복이면 INSERT 안 됨
    unique_key VARCHAR(255) NOT NULL,

    sgg_cd VARCHAR(10) NOT NULL COMMENT '법정동코드 앞5자리',
    umd_nm VARCHAR(100) COMMENT '법정동명',
    apt_nm VARCHAR(200) COMMENT '아파트 단지명',
    apt_dong VARCHAR(50) COMMENT '동 정보',
    jibun VARCHAR(50) COMMENT '지번',

    exclu_use_ar DECIMAL(10,2) COMMENT '전용면적(㎡)',

    deal_year SMALLINT,
    deal_month TINYINT,
    deal_day TINYINT,
    deal_date DATE COMMENT '계약일 (계산된 컬럼, 조회 편의용)',

    deal_amount BIGINT COMMENT '거래금액(만원)',
    price_per_pyeong DECIMAL(12,2) COMMENT '평당가(만원) - ETL에서 계산',

    floor SMALLINT,
    build_year SMALLINT,

    dealing_gbn VARCHAR(20) COMMENT '거래유형(중개/직거래)',
    sler_gbn VARCHAR(50) COMMENT '매도자구분',
    buyer_gbn VARCHAR(50) COMMENT '매수자구분',

    cdeal_type VARCHAR(10) COMMENT '해제여부',
    cdeal_day VARCHAR(20) COMMENT '해제사유발생일',

    estate_agent_sgg_nm VARCHAR(100) COMMENT '중개사소재지',
    land_leasehold_gbn VARCHAR(5) COMMENT '대지권여부',

    is_outlier BOOLEAN DEFAULT FALSE COMMENT '이상거래 플래그 (분석 배치에서 갱신)',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE KEY uk_unique_key (unique_key),
    INDEX idx_region_date (sgg_cd, deal_date),
    INDEX idx_apt_nm (apt_nm),
    INDEX idx_deal_date (deal_date)
) ENGINE=InnoDB COMMENT='아파트 매매 실거래 원본 데이터';


-- ============================================
-- 2. 지역별 월별 가격 추이 집계 테이블 (분석 배치 결과 저장용)
-- ============================================
CREATE TABLE IF NOT EXISTS monthly_price_summary (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    sgg_cd VARCHAR(10) NOT NULL,
    sgg_nm VARCHAR(50) COMMENT '구 이름 (조회 편의용)',
    deal_year SMALLINT NOT NULL,
    deal_month TINYINT NOT NULL,

    trade_count INT COMMENT '해당월 거래건수',
    avg_price BIGINT COMMENT '평균 거래금액(만원)',
    avg_price_per_pyeong DECIMAL(12,2) COMMENT '평균 평당가',
    price_change_rate DECIMAL(6,2) COMMENT '전월대비 변동률(%)',

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE KEY uk_region_month (sgg_cd, deal_year, deal_month)
) ENGINE=InnoDB COMMENT='지역별 월별 가격 집계';


-- ============================================
-- 3. 신고가/신저가 히스토리 테이블
-- ============================================
CREATE TABLE IF NOT EXISTS new_high_low_history (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    apt_trade_id BIGINT NOT NULL COMMENT 'apt_trade.id 참조',
    apt_nm VARCHAR(200),
    sgg_cd VARCHAR(10),
    record_type ENUM('HIGH', 'LOW') NOT NULL COMMENT '신고가/신저가 구분',
    price_per_pyeong DECIMAL(12,2),
    deal_date DATE,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (apt_trade_id) REFERENCES apt_trade(id),
    INDEX idx_apt_record (apt_nm, record_type)
) ENGINE=InnoDB COMMENT='단지별 신고가/신저가 경신 기록';


-- ============================================
-- 4. 이상거래 탐지 테이블
-- ============================================
CREATE TABLE IF NOT EXISTS outlier_trade (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    apt_trade_id BIGINT NOT NULL,
    sgg_cd VARCHAR(10),
    apt_nm VARCHAR(200),
    deal_price_per_pyeong DECIMAL(12,2) COMMENT '실제 거래 평당가',
    region_avg_price_per_pyeong DECIMAL(12,2) COMMENT '지역 평균 평당가',
    deviation_rate DECIMAL(6,2) COMMENT '평균 대비 편차율(%)',
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (apt_trade_id) REFERENCES apt_trade(id)
) ENGINE=InnoDB COMMENT='평균 대비 이상 거래 탐지 결과';