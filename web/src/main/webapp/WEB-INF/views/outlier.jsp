<%@ page contentType="text/html; charset=UTF-8" language="java"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>이상거래 탐지</title>
<style>
body {
	font-family: 'Malgun Gothic', sans-serif;
	margin: 40px;
}

table {
	border-collapse: collapse;
	width: 100%;
	margin-top: 20px;
}

th, td {
	border: 1px solid #ddd;
	padding: 8px;
	text-align: center;
	font-size: 14px;
}

th {
	background-color: #2c3e50;
	color: white;
}

tr:nth-child(even) {
	background-color: #f9f9f9;
}

.plus {
	color: #e74c3c;
	font-weight: bold;
}

.minus {
	color: #2980b9;
	font-weight: bold;
}

.direct {
	background-color: #fff3cd;
}

.search-form {
	margin-bottom: 20px;
}

.search-form select {
	padding: 5px;
	margin-right: 8px;
}

.pagination {
	margin-top: 24px;
	text-align: center;
}

.pagination a, .pagination span {
	display: inline-block;
	min-width: 28px;
	padding: 6px 10px;
	margin: 0 2px;
	border-radius: 4px;
	text-decoration: none;
	color: #2c3e50;
}

.pagination a:hover {
	background-color: #ecf0f1;
}

.pagination .current {
	font-weight: bold;
	color: #fff;
	background-color: #2c3e50;
}

.legend {
	font-size: 13px;
	color: #666;
	margin-top: 8px;
}
</style>
</head>
<body>
	<h1>⚠ 이상거래 탐지</h1>
	<p class="legend">같은 단지·같은 월 평균 평당가 대비 ±30% 이상 벗어난 거래입니다. 직거래는 음영으로
		표시됩니다.</p>

	<form class="search-form"
		action="${pageContext.request.contextPath}/detection/outlier"
		method="get">
		<select name="sggCd">
			<option value="">전체 구</option>
			<option value="11680" ${condition.sggCd == '11680' ? 'selected' : ''}>강남구</option>
			<option value="11710" ${condition.sggCd == '11710' ? 'selected' : ''}>송파구</option>
			<option value="11350" ${condition.sggCd == '11350' ? 'selected' : ''}>노원구</option>
			<option value="11170" ${condition.sggCd == '11170' ? 'selected' : ''}>용산구</option>
		</select>
		<button type="submit">검색</button>
	</form>

	<p>
		총 <strong>${totalCount}</strong>건 (${currentPage} / ${totalPages} 페이지)
	</p>

	<table>
		<thead>
			<tr>
				<th>거래일</th>
				<th>구</th>
				<th>단지명</th>
				<th>거래 평당가</th>
				<th>단지 평균 평당가</th>
				<th>편차율</th>
				<th>거래유형</th>
				<th>매도/매수</th>
			</tr>
		</thead>
		<tbody>
			<c:forEach var="row" items="${list}">
				<tr class="${row.dealingGbn == '직거래' ? 'direct' : ''}">
					<td>${row.dealDate}</td>
					<td>${row.sggCd}</td>
					<td>${row.aptNm}</td>
					<td><fmt:formatNumber value="${row.dealPricePerPyeong}"
							pattern="#,###" /></td>
					<td><fmt:formatNumber value="${row.regionAvgPricePerPyeong}"
							pattern="#,###" /></td>
					<td><c:choose>
							<c:when test="${row.deviationRate > 0}">
								<span class="plus">+${row.deviationRate}%</span>
							</c:when>
							<c:otherwise>
								<span class="minus">${row.deviationRate}%</span>
							</c:otherwise>
						</c:choose></td>
					<td>${row.dealingGbn}</td>
					<td>${row.slerGbn}→ ${row.buyerGbn}</td>
				</tr>
			</c:forEach>
			<c:if test="${empty list}">
				<tr>
					<td colspan="8">조회된 이상거래가 없습니다.</td>
				</tr>
			</c:if>
		</tbody>
	</table>

	<div class="pagination">
		<c:if test="${currentPage > 1}">
			<a
				href="${pageContext.request.contextPath}/detection/outlier?page=1&sggCd=${condition.sggCd}">&laquo;</a>
			<a
				href="${pageContext.request.contextPath}/detection/outlier?page=${currentPage - 1}&sggCd=${condition.sggCd}">&lsaquo;</a>
		</c:if>
		<c:forEach var="p" begin="${startPage}" end="${endPage}">
			<c:choose>
				<c:when test="${p == currentPage}">
					<span class="current">${p}</span>
				</c:when>
				<c:otherwise>
					<a
						href="${pageContext.request.contextPath}/detection/outlier?page=${p}&sggCd=${condition.sggCd}">${p}</a>
				</c:otherwise>
			</c:choose>
		</c:forEach>
		<c:if test="${currentPage < totalPages}">
			<a
				href="${pageContext.request.contextPath}/detection/outlier?page=${currentPage + 1}&sggCd=${condition.sggCd}">&rsaquo;</a>
			<a
				href="${pageContext.request.contextPath}/detection/outlier?page=${totalPages}&sggCd=${condition.sggCd}">&raquo;</a>
		</c:if>
	</div>
</body>
</html>