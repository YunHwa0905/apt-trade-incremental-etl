"""
분석 배치 통합 실행기
- 가격추이 -> 신고가/신저가 -> 이상거래 탐지 순서로 실행
  (이상거래 탐지가 monthly_price_summary 결과를 참조하므로 순서 중요)

실행: python run_analysis.py
"""

from analysis.price_trend import calc_price_trend
from analysis.new_high_low import detect_new_high_low
from analysis.outlier_detect import detect_outliers


def main():
    print("===== 분석 배치 시작 =====")

    print("\n[1/3] 지역별 월별 가격 추이 집계")
    calc_price_trend()

    print("\n[2/3] 단지별 신고가/신저가 탐지")
    detect_new_high_low()

    print("\n[3/3] 이상거래 탐지")
    detect_outliers()

    print("\n===== 분석 배치 완료 =====")


if __name__ == "__main__":
    main()