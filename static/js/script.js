var context = [];
var timeout;
window.onload = function () {
    document.getElementById("textInput").addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            getBotResponse();
        }
    });
}

function getBotResponse() {
    var userText = document.getElementById("textInput").value;
    userText = userText.replace(/</g, "&lt;").replace(/>/g, "&gt;");

    var chatbox = $('#chatbox');
    chatbox.append('<div class="userText"><div class=userIcon ><img src="/static/fry.png" alt="fry" width="40"></div><span>' + userText + '</span></div>');
    //// Clear the text input field
    $('#textInput').val('');
    // Cancel the previous timeout if it exists
    if (timeout) {
        clearTimeout(timeout);
    }
    // Set a new timeout to submit the form in 1 second
    timeout = setTimeout(function () {
        // Get the user's input text and sanitize it to prevent XSS attacks
        // Send an AJAX request to the server to get the bot's response
        $.ajax({
            url: '/get',
            type: 'GET',
            data: {
                msg: userText,
                context: context.join("\n")
            },
            success: function (response) {
                // Sanitize the bot's response to prevent XSS attacks
                response = response.replace(/</g, "<").replace(/>/g, ">");
                // Append the bot's response to the chatbox
                chatbox.append('<span><img src="/static/pixel_bender.png" alt="Hello" width="25"></span><div class="botText"><span>' + response + '</span></div>');
                // Update the context to include the user's input and the bot's response
                context.push(("User:", userText));
                context.push(("Bot:", response));
                // scroll to the bottom of the chatbox after appending the bot's response
                chatbox.scrollTop(chatbox.prop("scrollHeight"));
            }
        });
    }, 1000);
}

function clearConversation() {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/clear_conversation");
    xhr.onload = function () {
        if (this.status == 200) {
            context = xhr.responseText;
            // reload the page after the clear conversation request is completed
            location.reload();
        }
    };
    xhr.send();
}

function downloadConversation() {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/save_conversation");
    xhr.responseType = "blob";
    xhr.onload = function () {
        if (this.status == 200) {
            var blob = new Blob([xhr.response], {
                type: "application/octet-stream"
            });
            var link = document.createElement("a");
            link.href = window.URL.createObjectURL(blob);
            link.download = "conversation.txt";
            link.click();
        }
    };
    xhr.send();
};
