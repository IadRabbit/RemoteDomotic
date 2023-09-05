var csrftoken = getCookie("csrftoken");
const updated_success = getCookie("updated_success");

if (updated_success == "True") {
	Msg.success("AUDIO DELETED", 2000);
	document.cookie = "updated_success=False";
}

$(function () {
	$(".del_audio").click(function () {
		var self = $(this);
		var id_audio = self.attr("id_audio");

		$.ajax({
			type: "POST",
			beforeSend: function (request) {
				request.setRequestHeader("X-CSRFToken", csrftoken);
			},
			url: "/websecurity/del_audio/",
			data: {
				"id_audio": id_audio
			},
			success: function (json) {
				document.cookie = "updated_success=True";
				location.reload();
			},
			error: function (json) {
				var jsonResp = json.responseJSON;
				Msg.error(jsonResp['msg'], 2000);
			}
		})
	})
})