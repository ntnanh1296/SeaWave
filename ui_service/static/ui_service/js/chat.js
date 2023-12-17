// ui_service/static/ui_service/js/script.js

document.addEventListener('DOMContentLoaded', function () {
    // Get the recipient ID and recipient username from the template context
    const recipientId = parseInt('{{ recipient_id }}');
    const recipientUsername = '{{ recipient_username }}';

    const chatContainer = document.getElementById('chatContainer');
    const messageArea = document.getElementById('messageArea');
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');

    // Simulate a WebSocket connection
    const socket = new WebSocket(`ws://${window.location.host}/ws/chat/${recipientId}/`);

    // WebSocket event listeners
    socket.onopen = function (event) {
        console.log('WebSocket connection opened:', event);
    };

    socket.onmessage = function (event) {
        // Handle incoming messages
        const message = JSON.parse(event.data);
        appendMessage(message.sender, message.text, message.sender === recipientUsername);
    };

    socket.onclose = function (event) {
        console.log('WebSocket connection closed:', event);
    };

    // Event listener for the Send button
    sendButton.addEventListener('click', function () {
        const messageText = messageInput.value;

        if (messageText.trim() !== '') {
            // Send the message to the WebSocket server
            const message = {
                sender: '{{ user.username }}',  // Sender's username
                recipient: recipientId,
                text: messageText,
            };

            socket.send(JSON.stringify(message));

            // Append the sent message to the chat area
            appendMessage(message.sender, message.text, true);

            // Clear the input field
            messageInput.value = '';
        }
    });

    // Function to append messages to the message area
    function appendMessage(sender, text, isSentByRecipient) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');

        if (isSentByRecipient) {
            messageElement.classList.add('received');
            messageElement.innerHTML = `<strong>${sender} (Recipient):</strong> ${text}`;
        } else {
            messageElement.classList.add('sent');
            messageElement.innerHTML = `<strong>${sender} (Sender):</strong> ${text}`;
        }

        messageArea.appendChild(messageElement);

        // Scroll to the bottom to show the latest messages
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
});
