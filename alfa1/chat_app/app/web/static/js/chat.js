let ws;
document.addEventListener("DOMContentLoaded", () => {
    const sendButton = document.getElementById("send_button");
    const messageInput = document.getElementById("message_input");
    const usernameInput = document.getElementById("username");
    const messagesDiv = document.getElementById("messages");

    ws = new WebSocket("ws://" + window.location.host + "/ws");

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if(data.type === "message") {
            const msg = data.data;
            const div = document.createElement("div");
            div.innerText = msg.username + ": " + msg.content;
            messagesDiv.appendChild(div);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        } else if(data.type === "error") {
            alert("Error: " + data.error);
        }
    };

    sendButton.addEventListener("click", () => {
        const content = messageInput.value;
        const username = usernameInput.value || "Anonymous";
        const msg = {type: "message", username: username, content: content};
        ws.send(JSON.stringify(msg));
        messageInput.value = "";
    });
});
