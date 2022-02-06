console.log('Server starting...');
var express = require('express');
var app = express();
var serv = require('http').Server(app);
app.get('/',function(req, res){res.sendFile(__dirname+'/client/index.html');});
app.use('/',express.static(__dirname+'/client'));
serv.listen(2000);
console.log('Server started');
var targetFPS = 60;
var clients = {};
function Client(args){
  if(typeof args === 'object'){
    if(typeof args.id === 'number'){
      this.id = args.id
    }
    clients[this.id] = this;
  }
}
var io = require('socket.io')(serv,{});
io.sockets.on('connection',function(socket){
  socket.id = Math.random();
  new Client({id:socket.id});
});