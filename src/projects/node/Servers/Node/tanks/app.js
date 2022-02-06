console.log('Server starting...');
var express = require('express');
var app = express();
var serv = require('http').Server(app);
app.get('/',function(req, res){res.sendFile(__dirname+'/client/index.html');});
app.use('/',express.static(__dirname+'/client'));
serv.listen(2000);
console.log('Server started');
var io = require('socket.io')(serv,{});
var change = 3;
var tanks = {};
var font = '12pt Arial';
var tank = {height:66,width:66};
function Tank(id, name){
  this.id = id;
  this.name = name;
  this.x = 50;
  this.y = 50;
  this.degrees = 0;
  this.barrel = 45;
  this.keysPressed = [];
  this.move = function(){//add compensation for change to not go over
    /*if(this.keysPressed[87] && this.y >= 0){//w
      this.y -= change;
    }
    if(this.keysPressed[65] && this.x >= 0){//a
      this.x -= change;
    }
    if(this.keysPressed[83] && this.y <= 500-tank.height){//s
      this.y += change;
    }
    if(this.keysPressed[68] && this.x <= 500-tank.width){//d
      this.x += change;
    }*/
    if(this.keysPressed[87] && this.keysPressed[68]){
      this.degrees = -45;
      this.y -= change;
      this.x += change;
    }else if(this.keysPressed[87] && this.keysPressed[65]){
      this.degrees = -135;
      this.y -= change;
      this.x -= change;
    }else if(this.keysPressed[83] && this.keysPressed[68]){
      this.degrees = 45;
      this.y += change;
      this.x += change;
    }else if(this.keysPressed[83] && this.keysPressed[65]){
      this.degrees = 135
      this.y += change;
      this.x -= change;
    }else if(this.keysPressed[87]){
      this.degrees = 90;
      this.y -= change;
    }else if(this.keysPressed[83]){
      this.degrees = 90;
      this.y += change;
    }else if(this.keysPressed[68]){
      this.degrees = 0;
      this.x += change;
    }else if(this.keysPressed[65]){
      this.degrees = 0;
      this.x -= change;
    }
    
    if(this.x < 0){
      this.x = 0;
    }
    if(this.x > 434){
      this.x = 434;
    }
    if(this.y < 0){
      this.y = 0;
    }
    if(this.y > 434){
      this.y = 434;
    }
  }
  this.bullets = {};
  this.Bullet = function Bullet(parentId, xDir, yDir){
    
  }
  tanks[this.id] = this;
}
io.sockets.on('connection',function(socket){
  socket.id = Math.random();
  socket.on('newClient',function(data){
    new Tank(socket.id, data.name);
    console.log('Tank connected with id ' + socket.id);
    socket.on('keyUpdate',function(data){
      tanks[socket.id].keysPressed = data;
    });
    socket.on('disconnect',function(data){
      delete tanks[socket.id];
      console.log('Tank disconnected with id '+socket.id);
    });
    socket.emit('newClient',{id:socket.id,font:font})
  });
});
setInterval(function(){
  for(var id in tanks){
    tanks[id].move();
  }
  io.sockets.emit('move',tanks);
},1000/60);