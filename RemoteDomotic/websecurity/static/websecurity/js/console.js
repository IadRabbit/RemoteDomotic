var csrftoken = getCookie("csrftoken");
var helpKeyWords = [];

function getCommands() {
	$.ajax({
		type: "GET",
		beforeSend: function (request) {
			request.setRequestHeader("X-CSRFToken", csrftoken);
		},
		url: "/APIwebsecurity/get_audios/",
		success: function (json) {
			var commands = json['results']['commands'];

			for (a = 0; a < commands.length; a++) {
				c = commands[a];

				if (c.command) {
					text = "'" + c.command + "', " + c.description;
					helpKeyWords.push(text);
				}
			}

			helpKeyWords = helpKeyWords.join('<br>');
		},
		error: function (json) {
			Msg.error("WHAT ARE YOU TRYING TO DO?", 4000);
		}
	})
}

getCommands();

document.addEventListener('DOMContentLoaded', function () {

	document.getElementsByTagName('form')[0].onsubmit = function (evt) {
		evt.preventDefault(); // Preventing the form from submitting
		checkWord(); // Do your magic and check the entered word/sentence
		window.scrollTo(0, 150);
	}

	// Get the focus to the text input to enter a word right away.
	document.getElementById('terminalTextInput').focus();

	// Getting the text from the input
	var textInputValue = document.getElementById('terminalTextInput').value.trim();

	// Clear text input
	var clearInput = function () {
		document.getElementById('terminalTextInput').value = "";
	}

	// Scrtoll to the bottom of the results div
	var scrollToBottomOfResults = function () {
		var terminalResultsDiv = document.getElementById('terminalReslutsCont');
		terminalResultsDiv.scrollTop = terminalResultsDiv.scrollHeight;
	}

	// Scroll to the bottom of the results
	scrollToBottomOfResults();

	// Add text to the results div
	var addTextToResults = function (textToAdd) {
		document.getElementById('terminalReslutsCont').innerHTML += "<p>" + textToAdd + "</p>";
		scrollToBottomOfResults();
	}

	// Getting the list of keywords for help & posting it to the screen
	var postHelpList = function () {
		// Array of all the help keywords
		addTextToResults(helpKeyWords);
	}

	// Having a specific text reply to specific strings
	var textReplies = function () {
		if (helpKeyWords.includes(textInputValueLowerCase)) {
			clearInput();
			var command = textInputValueLowerCase;

			$.ajax({
				type: "POST",
				beforeSend: function (request) {
					request.setRequestHeader("X-CSRFToken", csrftoken);
				},
				url: "/APIwebsecurity/play_command/",
				data: {
					"command": command
				},
				success: function (json) {
					addTextToResults("<p>DONE =)</p>");
				},
				error: function (json) {
					var resp = json.responseJSON;
					addTextToResults("<p>" + resp['msg'] + "</p>");
				}
			})
		} else {
			switch (textInputValueLowerCase) {
				case "clear":
				case "cls":
					clearInput();
					break;

				case "help":
				case "?":
					clearInput();
					postHelpList();
					break;

				default:
					clearInput();
					addTextToResults("<p><i>The command " + "<b>" + textInputValue + "</b>" + " was not found. Type <b>Help</b> to see all commands.</i></p>");
					break;
			}
		}
	}

	// Main function to check the entered text and assign it to the correct function
	var checkWord = function () {
		textInputValue = document.getElementById('terminalTextInput').value.trim(); //get the text from the text input to a variable
		textInputValueLowerCase = textInputValue.toLowerCase(); //get the lower case of the string

		if (textInputValue != "") { //checking if text was entered
			addTextToResults("<p class='userEnteredText'>> " + textInputValue + "</p>");
			textReplies();
		}
	};

});