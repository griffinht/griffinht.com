console.log('Server starting...');
var express = require('express');
var app = express();
var serv = require('http').Server(app);
app.get('/', function(req, res){res.sendFile(__dirname+'/client/index.html');});
app.use('/', express.static(__dirname+'/client'));
serv.listen(2000);
console.log('Server started');
var fps = 60;
var speedUp = .25; //How much the ball should speed up
var slowDown = .25; //How much the ball should slow down
var balls = {};
var iimage = {width:110,height:110}
var canvas = {width:500,height:500}
function Ball(id, name, color, x, y){
  if(!id){id = Math.random();}
  if(!color){color = 'red';}
  if(!x){x = 1;}
  if(!y){y = 1;}
  if(!name){name = '';}
  this.keysPressed = [];
  this.id = id;
  this.name = name;
  this.color = color;
  this.x = x;
  this.y = y;
  this.xVel = 10;
  this.yVel = 10;
  this.move = function(){
    var collision = false;
    var slowX = true;
    var slowY = true;
    if(this.keys){slowX = false; slowY = false;}
    if(this.x<0 || this.x+iimage.width>canvas.width){
      this.xVel = -this.xVel;
      collision = true;
    }
    if(this.y<0 || this.y+iimage.height>canvas.height){
      this.yVel = -this.yVel;
      collision = true;
    }
    if(collision){io.sockets.emit('bump', Math.floor(Math.random()*2));}
    if(!collision){
      if(this.keysPressed.indexOf('w')!=-1){
        this.yVel = this.yVel-speedUp;
        slowY = false;
      }
      if(this.keysPressed.indexOf('s')!=-1){
        this.yVel = this.yVel+speedUp;
        slowY = false;
      }
      if(this.keysPressed.indexOf('d')!=-1){
        this.xVel = this.xVel+speedUp;
        slowX = false;
      }
      if(this.keysPressed.indexOf('a')!=-1){
        this.xVel = this.xVel-speedUp;
        slowX = false;
      }
      if(slowX){
        if(Math.sign(this.xVel)==1){
          this.xVel = this.xVel-slowDown;
        }else if(Math.sign(this.xVel)==-1){
          this.xVel = this.xVel+slowDown;
        }
      }
      if(slowY){
        if(Math.sign(this.yVel)==1){
          this.yVel = this.yVel-slowDown;
        }else if(Math.sign(this.yVel)==-1){
          this.yVel = this.yVel+slowDown;
        }
      }
    }
    var a = 60/fps;
    var b = this.xVel*a;
    var c = this.yVel*a;
    this.x = this.x+b;
    this.y = this.y+c;
  }
  balls[id] = this;
}
var io = require('socket.io')(serv,{});
io.sockets.on('connection', function(socket){
  socket.id = Math.random();
  console.log('Socket connected with server ID '+socket.id);
  socket.on('newClient', function(data){
    data[0] = socket.id;
    new Ball(data[0], data[1], data[2]);
    socket.emit('newClient',balls[socket.id]);
  });
  socket.on('disconnect', function(){
    console.log('Socket disconnected with ID '+socket.id);
    io.sockets.emit('adelete',socket.id);
    delete balls[socket.id];
  });
  socket.on('keyUpdate', function(data){
    if(balls[socket.id]){
      balls[socket.id].keysPressed = data;
    }
  });
  socket.on('aping', function(){socket.emit('apong');});
});
setInterval(function(){
  for(var id in balls){balls[id].move();}
  io.sockets.emit('move',balls);
},1000/fps);