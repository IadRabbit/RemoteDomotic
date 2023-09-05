var csrftoken = getCookie("csrftoken");

const fields = [
	"audio_description2", "audio_lang",
	"audio_text", "audio_command2"
]

const audio_gtts = $("#sound-clips2");

$(function () {
	$("#save_gtts").click(function () {
		for (a = 0; a < fields.length; a++) {
			var c = $("#" + fields[a]);

			if (c.val() === "") {
				c.focus();
				Msg.error("One field is empty :(", 2000);
				return;
			}
		}

		var audio_description = $("#audio_description2").val();
		var audio_lang = $("#audio_lang").val();
		var audio_text = $("#audio_text").val();
		var audio_command = $("#audio_command2").val();

		$.ajax({
			type: "POST",
			beforeSend: function (request) {
				request.setRequestHeader("X-CSRFToken", csrftoken);
			},
			url: "/websecurity/save_gtts/",
			data: {
				"audio_description": audio_description,
				"audio_lang": audio_lang,
				"audio_text": audio_text,
				"audio_command": audio_command
			},
			success: function (json) {
				var path = json['path'];
				var html = "<li class=\"list-group-item\">";
				html += "<audio src=\"" + path + "\" controls></audio>";
				html += "</li>";
				audio_gtts.append(html);
				Msg.success("Audio created with success =)", 2000);
			},
			error: function (json) {
				var jsonResp = json.responseJSON;
				Msg.error(jsonResp['msg'], 4000);
			}
		})
	})
})