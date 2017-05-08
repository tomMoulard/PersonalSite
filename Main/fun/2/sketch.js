var h, w;
var walkers = [];
var points = [];
var checkSym4;
var strokeW;

function setup() {
    h = windowHeight - 44;
    w = windowWidth;
    createCanvas(w, h);
    stroke(0, 255, 0);
    strokeWeight(3);
    checkSym4 = createCheckbox();
    strokeW = createSlider(0, 20, 3);
}

function draw() {
    strokeWeight(strokeW.value());
    background(0);
    for (var i = 0; i < walkers.length; i++) {
        walkers[i].move();
    }
    for (var j = 0; j < points.length; j++) {
        //print(points[j].x);
        point(points[j].x, points[j].y);
    }
}

function mousePressed() {
    if (mouseX < w && mouseY < h) {
        add(mouseX, mouseY);
    }
}

function mouseDragged() {
    if (mouseX < w && mouseY < h) {
        add(mouseX, mouseY);
    }
}

function add(x, y) {
    var newwalker = new Walker(x, y, checkSym4.checked());
    append(walkers, newwalker);
}

function addL(x, y) {
    var here = new P(x, y);
    append(points, here);
}

function P(x, y) {
    this.x = x;
    this.y = y;
}
