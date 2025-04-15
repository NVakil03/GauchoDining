// Connect to WebSocket server
const socket = new WebSocket('ws://localhost:3000');

// Listen for messages from the server
socket.onmessage = function (event) {
    const newMessage = JSON.parse(event.data);
    const messagesList = document.getElementById('messagesList');

    // Create a new list item for the new message
    const messageElement = document.createElement('li');
    messageElement.textContent = `${newMessage.username}: ${newMessage.message}`;
    messagesList.appendChild(messageElement);
};

// Fetch all messages when the page loads
window.addEventListener('load', function () {
    fetch('/messages')
        .then(response => response.json())
        .then(data => {
            const messagesList = document.getElementById('messagesList');
            data.forEach(msg => {
                const messageElement = document.createElement('li');
                messageElement.textContent = `${msg.username}: ${msg.message}`;
                messagesList.appendChild(messageElement);
            });
        });
});

// Handle form submission
document.getElementById('messageForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const message = document.getElementById('message').value;

    // Send the new message to the server through WebSocket
    socket.send(JSON.stringify({ username, message }));

    // Clear the message input field
    document.getElementById('message').value = '';
});