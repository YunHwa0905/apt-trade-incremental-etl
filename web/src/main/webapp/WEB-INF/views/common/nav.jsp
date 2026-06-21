<%@ page contentType="text/html; charset=UTF-8" language="java"%>
<style>
.nav-bar {
	background-color: #2c3e50;
	padding: 14px 24px;
	margin: -40px -40px 30px -40px;
}

.nav-bar a {
	color: #ecf0f1;
	text-decoration: none;
	margin-right: 24px;
	font-size: 15px;
	font-weight: 500;
}

.nav-bar a:hover {
	color: #3498db;
}

.nav-bar .brand {
	color: #fff;
	font-weight: bold;
	margin-right: 36px;
}
</style>
<div class="nav-bar">
	<span class="brand">🏠 서울 아파트 실거래가</span> <a
		href="${pageContext.request.contextPath}/trade/list">실거래 목록</a> <a
		href="${pageContext.request.contextPath}/price-trend">가격 추이</a> <a
		href="${pageContext.request.contextPath}/detection/high-low">신고가/신저가</a>
	<a href="${pageContext.request.contextPath}/detection/outlier">이상거래</a>
</div>