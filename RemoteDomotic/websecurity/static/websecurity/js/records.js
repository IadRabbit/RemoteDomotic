var csrftoken = getCookie("csrftoken");
const record = document.querySelector(".record");
const stop = document.querySelector(".stop");
const soundClips = document.querySelector("#sound-clips");
const canvas = document.querySelector(".visualizer");
const mainSection = document.querySelector(".main-controls");

stop.disabled = true;

const constraints = {
	audio: true
};

let audioCtx;
const canvasCtx = canvas.getContext("2d");
var rec;
var gumStream;
var source;

if (navigator.mediaDevices.getUserMedia) {
	console.log("getUserMedia supported.");

	let onSuccess = function (stream) {
		visualize(stream);

		record.onclick = function () {
			rec = new Recorder(source, {
				numChannels: 1
			})

			rec.record();
			gumStream = stream
			console.log("recorder started");
			record.style.background = "red";
			stop.disabled = false;
			record.disabled = true;
		}

		stop.onclick = function () {
			rec.stop();
			console.log("recorder stopped");
			record.style.background = "";
			record.style.color = "";
			stop.disabled = true;
			record.disabled = false;
			gumStream.getAudioTracks()[0];
			rec.exportWAV(createDownloadLink);
		}

		function createDownloadLink(blob) {
			const clipName = new Date().toISOString() + ".wav";
			const clipContainer = document.createElement("article");
			const clipLabel = document.createElement("p");
			const audio = document.createElement("audio");
			const deleteButton = document.createElement("button");
			const saveButton = document.createElement("button");
			clipContainer.classList.add("clip");
			audio.setAttribute("controls", "");
			deleteButton.textContent = "Delete";
			deleteButton.className = "btn btn-danger";
			saveButton.textContent = "Save";
			saveButton.className = "btn btn-success";
			clipLabel.textContent = clipName;
			clipContainer.appendChild(audio);
			clipContainer.appendChild(clipLabel);
			clipContainer.appendChild(deleteButton);
			clipContainer.appendChild(saveButton);
			soundClips.appendChild(clipContainer);
			audio.controls = true;
			const audioURL = window.URL.createObjectURL(blob);
			audio.src = audioURL;
			console.log("recorder stopped");

			saveButton.addEventListener("click", function (event) {
				var description = $("#audio_description").val();
				var command = $("#audio_command").val();
				var fd = new FormData();
				fd.append("audio", blob, clipName);
				fd.append("description", description);
				fd.append("command", command);

				$.ajax({
					type: "POST",
					beforeSend: function (request) {
						request.setRequestHeader("X-CSRFToken", csrftoken);
					},
					url: "/websecurity/upload_audio_command/",
					data: fd,
					contentType: false,
					processData: false,
					success: function (json) {
						Msg.success("AUDIO UPLOADED", 2000);
					},
					error: function (json) {
						var jsonResp = json.responseJSON;
						Msg.error(jsonResp["msg"], 3000);
					}
				})
			})

			deleteButton.onclick = function (e) {
				let evtTgt = e.target;
				evtTgt.parentNode.parentNode.removeChild(evtTgt.parentNode);
			}
		}
	}

	let onError = function (err) {
		console.log("The following error occured: " + err);
	}

	navigator.mediaDevices.getUserMedia(constraints).then(onSuccess, onError);

} else {
	console.log("getUserMedia not supported on your browser!");
}

function visualize(stream) {
	audioCtx = new AudioContext();
	source = audioCtx.createMediaStreamSource(stream);
	const analyser = audioCtx.createAnalyser();
	analyser.fftSize = 2048;
	const bufferLength = analyser.frequencyBinCount;
	const dataArray = new Uint8Array(bufferLength);
	source.connect(analyser);
	draw()

	function draw() {
		const WIDTH = canvas.width
		const HEIGHT = canvas.height;

		requestAnimationFrame(draw);

		analyser.getByteTimeDomainData(dataArray);

		canvasCtx.fillStyle = "rgb(200, 200, 200)";
		canvasCtx.fillRect(0, 0, WIDTH, HEIGHT);

		canvasCtx.lineWidth = 2;
		canvasCtx.strokeStyle = "rgb(0, 0, 0)";

		canvasCtx.beginPath();

		let sliceWidth = WIDTH * 1.0 / bufferLength;
		let x = 0;


		for (let i = 0; i < bufferLength; i++) {

			let v = dataArray[i] / 128.0;
			let y = v * HEIGHT / 2;

			if (i === 0) {
				canvasCtx.moveTo(x, y);
			} else {
				canvasCtx.lineTo(x, y);
			}

			x += sliceWidth;
		}

		canvasCtx.lineTo(canvas.width, canvas.height / 2);
		canvasCtx.stroke();
	}
}

window.onresize = function () {
	canvas.width = mainSection.offsetWidth;
}

window.onresize();