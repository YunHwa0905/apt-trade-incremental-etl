<%@ page contentType="text/html; charset=UTF-8" language="java"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>신고가 / 신저가 히스토리</title>
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

.high {
	color: #e74c3c;
	font-weight: bold;
}

.low {
	color: #2980b9;
	font-weight: bold;
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
</style>
</head>
<body>
	<jsp:include page="/WEB-INF/views/common/nav.jsp" />
	<h1>📊 신고가 / 신저가 히스토리</h1>

	<form class="search-form"
		action="${pageContext.request.contextPath}/detection/high-low"
		method="get">
		<select name="sggCd">
			<option value="">전체 구</option>
			<option value="11680" ${condition.sggCd == '11680' ? 'selected' : ''}>강남구</option>
			<option value="11710" ${condition.sggCd == '11710' ? 'selected' : ''}>송파구</option>
			<option value="11350" ${condition.sggCd == '11350' ? 'selected' : ''}>노원구</option>
			<option value="11170" ${condition.sggCd == '11170' ? 'selected' : ''}>용산구</option>
		</select> <select name="recordType">
			<option value="">전체</option>
			<option value="HIGH"
				${condition.recordType == 'HIGH' ? 'selected' : ''}>신고가만</option>
			<option value="LOW"
				${condition.recordType == 'LOW' ? 'selected' : ''}>신저가만</option>
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
				<th>구분</th>
				<th>평당가(만원)</th>
			</tr>
		</thead>
		<tbody>
			<c:forEach var="row" items="${list}">
				<tr>
					<td>${row.dealDate}</td>
					<td>${row.sggCd}</td>
					<td>${row.aptNm}</td>
					<td><c:choose>
							<c:when test="${row.recordType == 'HIGH'}">
								<span class="high">▲ 신고가</span>
							</c:when>
							<c:otherwise>
								<span class="low">▼ 신저가</span>
							</c:otherwise>
						</c:choose></td>
					<td><fmt:formatNumber value="${row.pricePerPyeong}"
							pattern="#,###" /></td>
				</tr>
			</c:forEach>
			<c:if test="${empty list}">
				<tr>
					<td colspan="5">조회된 데이터가 없습니다.</td>
				</tr>
			</c:if>
		</tbody>
	</table>

	<div class="pagination">
		<c:if test="${currentPage > 1}">
			<a
				href="${pageContext.request.contextPath}/detection/high-low?page=1&sggCd=${condition.sggCd}&recordType=${condition.recordType}">&laquo;</a>
			<a
				href="${pageContext.request.contextPath}/detection/high-low?page=${currentPage - 1}&sggCd=${condition.sggCd}&recordType=${condition.recordType}">&lsaquo;</a>
		</c:if>
		<c:forEach var="p" begin="${startPage}" end="${endPage}">
			<c:choose>
				<c:when test="${p == currentPage}">
					<span class="current">${p}</span>
				</c:when>
				<c:otherwise>
					<a
						href="${pageContext.request.contextPath}/detection/high-low?page=${p}&sggCd=${condition.sggCd}&recordType=${condition.recordType}">${p}</a>
				</c:otherwise>
			</c:choose>
		</c:forEach>
		<c:if test="${currentPage < totalPages}">
			<a
				href="${pageContext.request.contextPath}/detection/high-low?page=${currentPage + 1}&sggCd=${condition.sggCd}&recordType=${condition.recordType}">&rsaquo;</a>
			<a
				href="${pageContext.request.contextPath}/detection/high-low?page=${totalPages}&sggCd=${condition.sggCd}&recordType=${condition.recordType}">&raquo;</a>
		</c:if>
	</div>
</body>
</html>