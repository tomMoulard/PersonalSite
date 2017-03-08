var h, w;
var walkers = [];
var points = [];
var checkSym4;
function setup() {
	h = windowHeight - 20;
	w = windowWidth;
	createCanvas(w, h);
	stroke(0,255,0);
	strokeWeight(4);
	checkSym4 = createCheckbox();
}

function draw() {
	background(0);
	for(var i = 0; i < walkers.length; i++){
		walkers[i].move();
	}
	for(var j = 0; j < points.length; j++){
		print(points[j].x);
		point(points[j].x, points[j].y);
	}
}

function mousePressed(){
		add(mouseX, mouseY);
}
function mouseDragged(){
	add(mouseX, mouseY);	
}

function add(x, y){
	var newwalker = new Walker(x, y, checkSym4.checked());
	append(walkers, newwalker);
}

function addL(x, y){
	var here = new P(x,y);
	append(points, here);
}

function P(x,y) {
	this.x = x;
	this.y = y;
}