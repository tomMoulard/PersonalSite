var h,w;
var images = []
var pos = 0;
var hBox, wBox;
var nbBoxX, nbBoxY;
function setup() {
	h = windowHeight - 50;
	w = windowWidth;
	hBox = 25;
	wBox = 25;
	nbBoxX = floor(w / wBox);
	nbBoxY = floor(h / hBox);
	createCanvas(w,h);
	background(0);
}

function draw() {
	for(var j = 0; j < nbBoxY; j += 1){
		for(var i = 0; i < nbBoxX; i += 1){
			drawRect(i, j, images[pos][i][j]);
		}
	}
}

function drawRect(x, y, color){
	noStroke();
	fill(color);
	rectangle()
}