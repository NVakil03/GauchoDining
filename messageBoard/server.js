// server.js
const express = require('express');
const app = express();
const http = require('http').createServer(app);
const io = require('socket.io')(http);

app.use(express.static('public'));

io.on('connection', socket => {
    console.log('a user connected');
    socket.on('message', msg => {
        io.emit('message', msg); // broadcast to everyone
    });
});

http.listen(3000, () => {
    console.log('Listening on http://localhost:3000');
});
