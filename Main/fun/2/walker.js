    function Walker(x, y, quaded, l) {
        this.x = x;
        this.y = y;
        this.l = l;
        this.quaded = quaded

        this.move = function() {
            var np = floor(random(4));
            if (np == 0) {
                this.x += this.l;
                if (this.x > w) {
                    this.x = 0;
                }
            }
            if (np == 1) {
                this.x -= this.l;
                if (this.x < 0) {
                    this.x = w;
                }
            }
            if (np == 2) {
                this.y += this.l;
                if (this.y > h) {
                    this.y = 0;
                }
            }
            if (np == 3) {
                this.y -= this.l;
                if (this.y < 0) {
                    this.y = h;
                }
            }
            addL(this.x, this.y);
            if (this.quaded) {
                addL(this.x + w / 2, this.y);
                addL(this.x,         this.y + h / 2);
                addL(this.x + w / 2, this.y + h / 2);
            }
        }
    }
