var csrftoken = getCookie("csrftoken");

$(function () {
	$(".audio").click(function () {
		var self = $(this);
		var id_audio = self.attr("id_audio");

		$.ajax({
			type: "POST",
			beforeSend: function (request) {
				request.setRequestHeader("X-CSRFToken", csrftoken);
			},
			url: "/websecurity/playaudio/",
			data: {
				"id_audio": id_audio
			},
			success: function (json) {
				Msg.success("Audio started playing =)", 2000);
			},
			error: function (json) {
				var jsonResp = json.responseJSON;
				Msg.error(jsonResp['msg'], 2000);
			}
		})
	})
})