var h,w;
var file;
function setup() {
    h = windowHeight;
    w = windowWidth;
    createCanvas(w,h);
    background(0);
    file = FileReader(../../date.txt);
    console.log(file);
}

function draw() {
    
}