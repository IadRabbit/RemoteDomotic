var csrftoken = getCookie("csrftoken");

$(function () {
	$(".switchh").click(function () {
		const self = $(this);
		var id_device = self.attr("id_device");

		$.ajax({
			type: "POST",
			beforeSend: function (request) {
				request.setRequestHeader("X-CSRFToken", csrftoken);
			},
			url: "/websecurity/turn_lamp/",
			data: {
				"id_device": id_device
			},
			success: function (json) {
				var status = json['status'];
				Msg.success(json['msg'], 2000);
			},
			error: function (json) {
				var jsonResp = json.responseJSON;
				Msg.error(jsonResp['msg'], 2000);
			}
		})
	})
})