<%@ page contentType="text/html; charset=UTF-8" language="java"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>지역별 가격 추이</title>
<script type="text/javascript"
	src="https://www.gstatic.com/charts/loader.js"></script>
<style>
body {
	font-family: 'Malgun Gothic', sans-serif;
	margin: 40px;
}

select {
	padding: 6px;
	font-size: 14px;
	margin-bottom: 16px;
}

#chart_div {
	width: 100%;
	height: 480px;
}
</style>
</head>
<body>
	<jsp:include page="/WEB-INF/views/common/nav.jsp" />
	<h1>📈 지역별 월별 가격 추이</h1>

	<select id="sggCdSelect">
		<option value="">전체(서울 평균)</option>
		<c:forEach var="region" items="${regions}">
			<option value="${region.sggCd}">${region.sggNm}</option>
		</c:forEach>
	</select>

	<div id="chart_div"></div>

	<script type="text/javascript">
		google.charts.load('current', {
			'packages' : [ 'corechart' ]
		});
		google.charts.setOnLoadCallback(initialDraw);

		function initialDraw() {
			drawChart('');
		}

		function drawChart(sggCd) {
			var url = '${pageContext.request.contextPath}/price-trend/data';
			if (sggCd) {
				url += '?sggCd=' + sggCd;
			}

			fetch(url).then(function(response) {
				return response.json();
			}).then(
					function(data) {
						var chartData = new google.visualization.DataTable();
						chartData.addColumn('string', '연월');
						chartData.addColumn('number', '평균 평당가(만원)');
						chartData.addColumn('number', '거래건수');

						data.forEach(function(row) {
							var label = row.dealYear
									+ '-'
									+ (row.dealMonth < 10 ? '0' + row.dealMonth
											: row.dealMonth);
							chartData.addRow([ label, row.avgPricePerPyeong,
									row.tradeCount ]);
						});

						var options = {
							title : '월별 평균 평당가 추이',
							curveType : 'function',
							legend : {
								position : 'bottom'
							},
							series : {
								0 : {
									targetAxisIndex : 0
								},
								1 : {
									targetAxisIndex : 1,
									type : 'bars',
									color : '#cccccc'
								}
							},
							vAxes : {
								0 : {
									title : '평당가(만원)'
								},
								1 : {
									title : '거래건수'
								}
							},
							seriesType : 'line'
						};

						var chart = new google.visualization.ComboChart(
								document.getElementById('chart_div'));
						chart.draw(chartData, options);
					});
		}

		document.getElementById('sggCdSelect').addEventListener('change',
				function() {
					drawChart(this.value);
				});
	</script>

</body>
</html>