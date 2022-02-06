console.log('Server starting...');
var express = require('express');
var app = express();
var serv = require('http').Server(app);
app.get('/',function(req, res){res.sendFile(__dirname+'/client/index.html');});
app.use('/',express.static(__dirname+'/client'));
serv.listen(2000);
console.log('Server started');
var fps = 60;//FPS
var a = 60/fps;
var speedUp = .25; //How much the ball should speed up
var slowDown = .25; //How much the ball should slow down
var bulletSpeed = 10; //How fast the bullets should move
var bulletDamage = 20; //How much damage the bullets should inflict
var bulletHealth = 2; //How many times the bullet can hit a wall before it dies
var health = 100; //How much health the player has
var bulletCollisions = true; //Should the server check if each bullet is hitting each player?
var balls = {};
var bullets = {};
var colors = ['red','blue'];
var ballImage = {width:110,height:110}
var bulletImage = {width:40,height:40}
var canvas = {width:500,height:500}
var frames = 0;
function bump(){io.sockets.emit('bump',Math.floor(Math.random()*2));}
function checkDefined(variable){if(typeof variable!=='undefined'){return true;}else{return false;}}
function Bullet(xDir, yDir, id){
  if(!xDir || !yDir){return false;}
  this.id = Math.random();
  this.parentId = id;
  this.x = balls[id].x+ballImage.width/2-bulletImage.width/2;
  this.y = balls[id].y+ballImage.height/2-bulletImage.height/2;
  this.xVel = xDir*bulletSpeed;
  this.yVel = yDir*bulletSpeed;
  this.bumps = 0;
  this.move = function(){
    var collision = false;
    if(this.x<0 || this.x+bulletImage.width>canvas.width){
      this.xVel = -this.xVel;
      collision = true;
    }
    if(this.y<0 || this.y+bulletImage.height>canvas.height){
      this.yVel = -this.yVel;
      collision = true;
    }
    if(collision){
      bump();
      this.bumps++;
    }
    if(this.bumps>=bulletHealth){
      delete bullets[this.id];
    }
    var b = this.xVel*a;
    var c = this.yVel*a;
    this.x = this.x+b;
    this.y = this.y+c;
  }
  bullets[this.id] = this;
}
function Ball(id, name, color, x, y){
  if(!id){id = Math.random();}
  if(!color){color = 'red';}
  var realColor = false;
  for(var i = 0; i<colors.length; i++){if(colors[i]==color){realColor = true;}}
  if(!realColor){color = 'red';}
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
  this.health = health;
  this.move = function(){
    if(this.health<=0){
      io.sockets.emit('death',this.id);
      delete balls[this.id];
    }
    var collision = false;
    var slowX = true;
    var slowY = true;
    if(this.keys){slowX = false; slowY = false;}
    if(bulletCollisions){
      for(var id in bullets){
        if(bullets[id].parentId!=this.id){
          var distance = Math.hypot((this.x+ballImage.height/2)-(bullets[id].x+bulletImage.height/2),(this.y+ballImage.width/2)-(bullets[id].y+bulletImage.width/2));
          if(distance<=75){
            delete bullets[id];
            this.health -= bulletDamage;
          }
        }
      }
    }
    if(this.x<0 || this.x+ballImage.width>canvas.width){
      this.xVel = -this.xVel;
      collision = true;
    }
    if(this.y<0 || this.y+ballImage.height>canvas.height){
      this.yVel = -this.yVel;
      collision = true;
    }
    if(collision){bump();}
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
    var b = this.xVel*a;
    var c = this.yVel*a;
    this.x = this.x+b;
    this.y = this.y+c;
  }
  balls[this.id] = this;
}
var io = require('socket.io')(serv,{});
io.sockets.on('connection',function(socket){
  socket.id = Math.random();
  console.log('Socket connected with ID '+socket.id);
  socket.on('newClient',function(data){
    if(checkDefined(data)){
      if(checkDefined(data[0]) && checkDefined(data[1])){
        var name = '';
        var color = 'red';
        new Ball(socket.id, data[0], data[1]);
        socket.emit('newClient',balls[socket.id]);
      }
    }
  });
  socket.on('disconnect',function(){
    console.log('Socket disconnected with ID '+socket.id);
    delete balls[socket.id];
  });
  socket.on('newBullet',function(data){
    if(checkDefined(data.xDir) && checkDefined(data.yDir)){new Bullet(data.xDir, data.yDir, socket.id);}
  });
  socket.on('keyUpdate',function(data){
    if(checkDefined(balls[socket.id]) && checkDefined(data)){balls[socket.id].keysPressed = data;}
  });
  socket.on('aping',function(){socket.emit('apong');});
});
setInterval(function(){
  var emit = false;
  for(var id in balls){
    balls[id].move();
    emit = true;
  }
  for(var id in bullets){
    bullets[id].move();
    emit = true;
  }
  if(emit){io.sockets.emit('move',{balls:balls,bullets:bullets});}
  frames++;
},1000/fps);
setInterval(function(){
  if(frames<fps*.90){console.log('Server is lagging - FPS: '+frames+' (Target: '+fps+')');}
  frames = 0;
},1000);