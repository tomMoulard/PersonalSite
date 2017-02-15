// BUTTON PARTICLE
(function() {
    var lastTime = 0;
    var vendors = ['ms', 'moz', 'webkit', 'o'];
    for(var x = 0; x < vendors.length && !window.requestAnimationFrame; ++x) {
        window.requestAnimationFrame = window[vendors[x]+'RequestAnimationFrame'];
        window.cancelAnimationFrame = window[vendors[x]+'CancelAnimationFrame'] 
                                   || window[vendors[x]+'CancelRequestAnimationFrame'];
    }
 
    if (!window.requestAnimationFrame)
        window.requestAnimationFrame = function(callback, element) {
            var currTime = new Date().getTime();
            var timeToCall = Math.max(0, 16 - (currTime - lastTime));
            var id = window.setTimeout(function() { callback(currTime + timeToCall); }, 
              timeToCall);
            lastTime = currTime + timeToCall;
            return id;
        };
 
    if (!window.cancelAnimationFrame)
        window.cancelAnimationFrame = function(id) {
            clearTimeout(id);
        };
}());

(function() {

	var startBtn = document.getElementById('button');
	var requestID;
	var canvas = document.getElementById('canvas');
	var ctx = canvas.getContext('2d');

	var posX = 0;
	var W = 246;
  var H = 60;
  var circles = []; 
  
  canvas.width = 246;
  canvas.height = 60; 

	function animate() {
		requestID = requestAnimationFrame(animate);

    ctx.fillStyle = "rgba(0,70,117,0.15)";
    ctx.fillRect(0, 0, W, H);

    for(var j = 0; j < circles.length; j++){
      var c = circles[j];

      ctx.beginPath();
      ctx.arc(c.x, c.y, c.radius, 0, Math.PI*2, false);
          ctx.fillStyle = "rgba("+c.r+", "+c.g+", "+c.b+", 0.5)";
      ctx.fill();

      c.x += c.vx;
      c.y += c.vy;
      c.radius -= .02;

      if(c.radius < 0)
        circles[j] = new create();
    }  
     
		
	}
  
      function create() {

        this.x = W/2;
        this.y = H/2;

        this.radius = 2 + Math.random()*3; 

        this.vx = -5 + Math.random()*10;
        this.vy = -5 + Math.random()*10;

        this.r = Math.round(Math.random())*255;
        this.g = Math.round(Math.random())*255;
        this.b = Math.round(Math.random())*255;
      }

      for (var i = 0; i < 500; i++) {
        circles.push(new create());
	 }
	
	startBtn.addEventListener('mouseover', function(e) {
		e.preventDefault();
		
		requestID = requestAnimationFrame(animate);
	});

	startBtn.addEventListener('mouseout', function(e) {
		e.preventDefault();

		cancelAnimationFrame(requestID);
    
    e.preventDefault();

		// Reset the X position to 0.
		posX = 0;

		// Clear the canvas.
		ctx.clearRect(0, 0, canvas.width, canvas.height);

		// Draw the initial box on the canvas.
		ctx.fillRect(posX, 0, boxWidth, canvas.height);
    
	});

}());