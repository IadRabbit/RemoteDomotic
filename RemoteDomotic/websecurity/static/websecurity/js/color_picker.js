var csrftoken = getCookie("csrftoken");
const root = $(document.documentElement);

function req(id_device, c_hue, brightness) {
	$.ajax({
		type: "POST",
		beforeSend: function (request) {
			request.setRequestHeader("X-CSRFToken", csrftoken);
		},
		url: "/websecurity/color_lamp/",
		data: {
			"id_device": id_device,
			"hue": c_hue,
			"brightness": brightness
		},
		success: function (json) {
			Msg.success(json['msg'], 2000);
		},
		error: function (json) {
			var jsonResp = json.responseJSON;
			Msg.error(jsonResp['msg'], 2000);
		}
	})
}

function change_lamp(self) {
	var self = $(self);
	var id_device = self.attr("id_device");
	var parent = self.parent();
	var parent1 = parent.parent();
	var parent2 = parent1.parent();
	var parent3 = parent2.parent();

	var color_temp = (
		parent3
		.find(".tempp")
		.find(".color_temp")
	);

	var c_hue = (
		parent3
		.find(".huee")
		.find(".hue")
	);

	var brightness = (
		parent3
		.find(".brightnesss")
		.find(".brightness")
		.val()
	);

	var val_to_use;

	if (
		color_temp.attr("checked")
	) {
		val_to_use = color_temp.val();
	} else {
		val_to_use = c_hue.val();
	}

	req(id_device, val_to_use, brightness);
}

function setHue(self) {
	var self = $(self);
	var parent = self.parent();
	var parent1 = parent.parent();
	var parent2 = parent1.parent();
	var parent3 = parent2.parent();

	var color_temp = (
		parent3
		.find(".tempp")
		.find(".color_temp")
		.removeAttr("checked")
	);

	self.attr("checked", "checked");
	var hue = self.val();

	var some_class = {
		"background": "hsl(" + hue + ", 100%, 50%)"
	}

	var parent = self.parent();
	var parent1 = parent.parent();
	parent1.css(some_class);
	var output = parent.find("output");
	output.val(hue + "°");
	root.css("--hue", hue);
}

function setColorTemp(self) {
	var self = $(self);
	var parent = self.parent();
	var parent1 = parent.parent();
	var parent2 = parent1.parent();
	var parent3 = parent2.parent();

	var hue = (
		parent3
		.find(".huee")
		.find(".hue")
		.removeAttr("checked")
	);

	self.attr("checked", "checked");
	var color_temp = self.val();
	var parent = self.parent();
	var output = parent.find("output");
	output.val(color_temp + "K");
	root.css("--color_temp", color_temp);
}

function setBrightness(self) {
	var self = $(self);
	var brightness = self.val();
	var parent = self.parent();
	var output = parent.find("output");
	output.val(brightness + "%");
	root.css("--brightness", brightness);
}

function setDefaultState() {
	$(".hue").each(function () {
		setHue(this);
	})

	$(".color_temp").each(function () {
		setColorTemp(this);
	})

	$(".brightness").each(function () {
		setBrightness(this);
	})
}

$(".hue").on("input", function () {
	setHue(this);
})

$(".color_temp").on("input", function () {
	setColorTemp(this);
})

$(".brightness").on("input", function () {
	setBrightness(this);
})

$(".hue").change(function () {
	change_lamp(this);
})

$(".color_temp").change(function () {
	change_lamp(this);
})

$(".brightness").change(function () {
	change_lamp(this);
})

setDefaultState();