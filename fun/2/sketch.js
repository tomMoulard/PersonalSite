var h, w;
var walkers = []
var points = []
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

	for(var i = 0; i < points.length; i++){
		point(points[i].x, points[i].y);
	}
}

function mousePressed(){
	if(mouseY < h){
		add(mouseX, mouseY);
	}
}
function mouseDragged(){
	add(mouseX, mouseY);	
}

function add(x, y){
	var newwalker = new Walker(x, y, checkSym4.checked());
	append(walkers, newwalker)
}

function addL(x, y){
	var l = points.length;
	var found = false;
	var pos = 0;
	while (pos < l && ! found){
		if(points[pos].x == x && points[pos].y == y){
			found = true;
		}
		pos += 1;
	}
	if(! found){
		append(points, P(x, y));
	}
}

function P(x,y) {
	this.x = x;
	this.y = y;
	return this;
}