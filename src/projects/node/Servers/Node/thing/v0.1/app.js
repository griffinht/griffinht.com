console.log('Server starting...');
var express = require('express');
var app = express();
var serv = require('http').Server(app);
app.get('/',function(req, res){res.sendFile(__dirname+'/client/index.html');});
app.use('/',express.static(__dirname+'/client'));
serv.listen(2000);
console.log('Server started');
var targetFPS = 60;

var padding = 5;
var fontSize = 12;
var fontUnit = 'pt';
var fontColor = 'black';
var fontFamily = 'arial';
var backgroundColor = 'red';

var defaultWidth = 100;
var defaultHeight = 100;

var io = require('socket.io')(serv,{});
io.sockets.on('connection',function(socket){
  socket.id = Math.random();
  socket.emit('info',{targetFPS:targetFPS, padding:padding, fontSize:fontSize, fontColor:fontColor, fontFamily:fontFamily, defaultWidth:defaultWidth, defaultHeight:defaultHeight, backgroundColor:backgroundColor, fontUnit:fontUnit});
});