function Walker(x, y, quaded) {
	this.x = x;
	this.y = y;
	this.l = 3;
	this.quaded = quaded

	this.move = function() {
		var np = floor(random(4));
		if (np == 0){
			this.x += this.l;
			if(this.x > w){
				this.x = 0;
			}
			if(this.quaded){		
				addL(this.x - this.l + w / 2, this.y)
			}
		}
		if (np == 1){
			this.x -= this.l;	
			if(this.x < 0){
				this.x = w;
			}
			if(this.quaded){	
				addL(this.x + this.l + w / 2, this.y)	
			}
		}
		if (np == 2){
			this.y += this.l;
			if(this.y > h){
				this.y = 0;
			}
			if(this.quaded){
				addL(this.x, this.y + this.l + h / 2)		
			}
		}
		if (np == 3){
			this.y -= this.l;
			if(this.y < 0){
				this.y = h;
			}
			if(this.quaded){
				addL(this.x, this.y - this.l + h / 2)			
			}			
		}
		addL(this.x, this.y);
	}
}