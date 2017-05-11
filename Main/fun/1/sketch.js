var angle;
var slider;
var h, w;
var newLen;
function setup() {
    h      = windowHeight - 50;
    w      = windowWidth;
    newLen = 0.6667;
    createCanvas(w, h);
    slider = createSlider(0, TWO_PI, PI/4, 0.001);
}

function draw() {
    background(51);
    angle = slider.value();
    stroke(255);
    translate(w / 2, height);
    branch(h / 4);
}

function branch(len){
    strokeWeight(len * 0.25);
    line(0, 0, 0, -len);
    translate(0, -len);
    if(len > 2){    
        newbranch(len, angle);
        newbranch(len, -angle);
    }
}

function newbranch(len, angle){
    push();
    rotate(angle);
    branch(len*newLen);
    pop();
}