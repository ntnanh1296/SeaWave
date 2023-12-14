document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const chatMessages = document.getElementById('chat-messages');

    const socket = new WebSocket('ws://' + window.location.host + '/ws/chat/');

    socket.onmessage = function(event) {
        const message = JSON.parse(event.data).message;
        chatMessages.innerHTML += '<p>' + message + '</p>';
    };

    chatForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const message = messageInput.value;
        socket.send(JSON.stringify({'message': message}));
        messageInput.value = '';
    });
});
