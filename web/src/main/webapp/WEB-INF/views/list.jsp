<%@ page contentType="text/html; charset=UTF-8" language="java"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>서울 아파트 실거래가 목록</title>
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

.outlier {
	color: #e74c3c;
	font-weight: bold;
}

.search-form {
	margin-bottom: 20px;
}

.search-form input, .search-form select {
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
</style>
</head>
<body>
	<h1>🏠 서울 아파트 실거래가 목록</h1>

	<form class="search-form"
		action="${pageContext.request.contextPath}/trade/list" method="get">
		<select name="sggCd">
			<option value="">전체 구</option>
			<option value="11680" ${condition.sggCd == '11680' ? 'selected' : ''}>강남구</option>
			<option value="11710" ${condition.sggCd == '11710' ? 'selected' : ''}>송파구</option>
			<option value="11350" ${condition.sggCd == '11350' ? 'selected' : ''}>노원구</option>
			<option value="11170" ${condition.sggCd == '11170' ? 'selected' : ''}>용산구</option>
		</select> <input type="text" name="aptNm" placeholder="단지명 검색"
			value="${condition.aptNm}" /> <input type="number" name="dealYear"
			placeholder="연도 (예: 2025)" value="${condition.dealYear}"
			style="width: 100px;" /> <input type="number" name="dealMonth"
			placeholder="월 (예: 6)" value="${condition.dealMonth}"
			style="width: 80px;" />
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
				<th>전용면적(㎡)</th>
				<th>층</th>
				<th>거래금액(만원)</th>
				<th>평당가</th>
				<th>거래유형</th>
				<th>이상거래</th>
			</tr>
		</thead>
		<tbody>
			<c:forEach var="trade" items="${tradeList}">
				<tr>
					<td>${trade.dealDate}</td>
					<td>${trade.umdNm}</td>
					<td>${trade.aptNm}</td>
					<td>${trade.excluUseAr}</td>
					<td>${trade.floor}</td>
					<td><fmt:formatNumber value="${trade.dealAmount}"
							pattern="#,###" /></td>
					<td><fmt:formatNumber value="${trade.pricePerPyeong}"
							pattern="#,###" /></td>
					<td>${trade.dealingGbn}</td>
					<td><c:if test="${trade.isOutlier}">
							<span class="outlier">⚠ 이상거래</span>
						</c:if></td>
				</tr>
			</c:forEach>
			<c:if test="${empty tradeList}">
				<tr>
					<td colspan="9">조회된 거래가 없습니다.</td>
				</tr>
			</c:if>
		</tbody>
	</table>

	<div class="pagination">
		<c:if test="${currentPage > 1}">
			<a
				href="${pageContext.request.contextPath}/trade/list?page=1&sggCd=${condition.sggCd}&aptNm=${condition.aptNm}&dealYear=${condition.dealYear}&dealMonth=${condition.dealMonth}">&laquo;</a>
			<a
				href="${pageContext.request.contextPath}/trade/list?page=${currentPage - 1}&sggCd=${condition.sggCd}&aptNm=${condition.aptNm}&dealYear=${condition.dealYear}&dealMonth=${condition.dealMonth}">&lsaquo;</a>
		</c:if>

		<c:forEach var="p" begin="${startPage}" end="${endPage}">
			<c:choose>
				<c:when test="${p == currentPage}">
					<span class="current">${p}</span>
				</c:when>
				<c:otherwise>
					<a
						href="${pageContext.request.contextPath}/trade/list?page=${p}&sggCd=${condition.sggCd}&aptNm=${condition.aptNm}&dealYear=${condition.dealYear}&dealMonth=${condition.dealMonth}">${p}</a>
				</c:otherwise>
			</c:choose>
		</c:forEach>

		<c:if test="${currentPage < totalPages}">
			<a
				href="${pageContext.request.contextPath}/trade/list?page=${currentPage + 1}&sggCd=${condition.sggCd}&aptNm=${condition.aptNm}&dealYear=${condition.dealYear}&dealMonth=${condition.dealMonth}">&rsaquo;</a>
			<a
				href="${pageContext.request.contextPath}/trade/list?page=${totalPages}&sggCd=${condition.sggCd}&aptNm=${condition.aptNm}&dealYear=${condition.dealYear}&dealMonth=${condition.dealMonth}">&raquo;</a>
		</c:if>
	</div>

</body>
</html>