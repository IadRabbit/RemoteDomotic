var ball = document.getElementById("ball");

document.onmousemove = function (event) {
	var x = event.clientX * 80 / window.innerWidth + "%";
	var y = event.clientY * 80 / window.innerHeight + "%";

	ball.style.left = x;
	ball.style.top = y;
	ball.style.transform = "translate(-" + x + ",-" + y + ")";
}

var csrftoken = getCookie("csrftoken");

$(function () {
	$("#login").submit(function (event) {
		event.preventDefault();
		var username = $("#username").val();
		var password = $("#password").val();
		var redirect = $("#redirect").val();

		$.ajax({
			type: "POST",
			beforeSend: function (request) {
				request.setRequestHeader("X-CSRFToken", csrftoken);
			},
			url: "/websecurity/auth/",
			data: {
				"username": username,
				"password": password,
				"next": redirect
			},
			success: function (json) {
				location.href = json["redirect"];
			},
			error: function (json) {
				Msg.error("CANNOT LOGIN =)???", 4000);
			}
		})
	})
})