const express = require('express');
const fs = require('fs');
const path = require('path');
const WebSocket = require('ws');

const app = express();
const PORT = process.env.PORT || 3000;
const messagesFilePath = path.join(__dirname, 'messages.json');
const metaFilePath = path.join(__dirname, 'meta.json');

// Ensure daily reset
const today = new Date().toISOString().split('T')[0];
let lastResetDate = '';
let messages = [];

try {
    const meta = JSON.parse(fs.readFileSync(metaFilePath, 'utf8'));
    lastResetDate = meta.date;
} catch {
    lastResetDate = '';
}

if (lastResetDate !== today) {
    console.log('🔁 Resetting messages for a new day!');
    messages = [];
    fs.writeFileSync(messagesFilePath, JSON.stringify(messages, null, 2));
    fs.writeFileSync(metaFilePath, JSON.stringify({ date: today }, null, 2));
} else {
    try {
        messages = JSON.parse(fs.readFileSync(messagesFilePath, 'utf8'));
    } catch {
        messages = [];
    }
}

app.use(express.static('public'));
app.use(express.json());

// HTTP POST message
app.post('/messages', (req, res) => {
    const { username, message } = req.body;
    if (!username || !message) return res.status(400).json({ error: 'Missing username or message' });

    const newMessage = { username, message, timestamp: new Date().toISOString() };
    messages.push(newMessage);
    fs.writeFileSync(messagesFilePath, JSON.stringify(messages, null, 2));

    broadcastMessage(newMessage);
    res.status(201).json(newMessage);
});

// HTTP GET messages
app.get('/messages', (req, res) => {
    res.json(messages);
});

// Start server
const server = app.listen(PORT, '0.0.0.0', () => {
    console.log(`✅ Server running at http://localhost:${PORT}`);
});

// WebSocket setup
const wss = new WebSocket.Server({ server });

wss.on('connection', ws => {
    console.log('🟢 WebSocket client connected');
    ws.send(JSON.stringify({ type: 'init', messages }));

    ws.on('message', data => {
        const { username, message } = JSON.parse(data);
        const newMessage = { username, message, timestamp: new Date().toISOString() };
        messages.push(newMessage);
        fs.writeFileSync(messagesFilePath, JSON.stringify(messages, null, 2));
        broadcastMessage(newMessage);
    });
});

function broadcastMessage(msg) {
    wss.clients.forEach(client => {
        if (client.readyState === WebSocket.OPEN) {
            client.send(JSON.stringify({ type: 'new', message: msg }));
        }
    });
}