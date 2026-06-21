package com.apttrade.web.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.ui.Model;

import java.time.LocalDateTime;

/**
 * 환경 구동 확인용 테스트 컨트롤러. Spring MVC + Tomcat 연동이 정상인지 확인하는 용도. (실제 기능 완성 후 삭제하거나
 * /health 체크용으로 남겨도 됨)
 */
@Controller
public class HomeController {

	@RequestMapping(value = "/", method = RequestMethod.GET)
	public String home(Model model) {
		model.addAttribute("serverTime", LocalDateTime.now().toString());
		model.addAttribute("message", "Spring Legacy + MyBatis 환경 정상 구동 확인");
		return "home"; // -> /WEB-INF/views/home.jsp
	}
}