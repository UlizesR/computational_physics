// const { Vector } = require('./vector.js');
// const { Celestial } = require('./celestial.js');

const canvas = document.querySelector('canvas');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// canvas settings
ctx.fillStyle = 'white';
ctx.strokeStyle = 'white';
ctx.lineWidth = 1;

G_CONST = 6.67408e-11;
SCREEN_RATIO = canvas.width / canvas.height;
//  1 px = 100 000 km
SCALE = 1e-5;
AU = 149597870.7; // 1 AU = 149 597 870.7 km
AU_SCALE = AU * SCALE;
console.log(AU_SCALE);

G_CONST_S = G_CONST / SCALE;
console.log(G_CONST);




class Effect {
    constructor(width, height) {
        this.width = width;
        this.height = height;
        this.vectors1 = [];
        this.vectors2 = [];
        this.vectors3 = [];
        this.celestial1 = new Celestial(this, 500, 300, 1.989e30, 696e6, 0.1, 0, 'yellow');
        this.celestial2 = new Celestial(this, 500, 300 + AU_SCALE, 5.972e24, 6378e3, 0.1, -1.07, 'blue');
        this.init();

        // Add event listener for mousemove event.
        canvas.addEventListener('mousemove', (event) => {
            this.mouseX = event.clientX;
            this.mouseY = event.clientY;
        });
    }
    init() {
        const px_space = 20;
        const px2 = 2 * px_space;
        const positions = Array.from(
            { length: (this.width - px2) / px_space * (this.height - px2) / px_space },
            (_, i) => [
                px_space + (i % ((this.width - px2) / px_space)) * px_space,
                px_space + Math.floor(i / ((this.width - px2) / px_space)) * px_space
            ]
        );

        this.vectors1 = positions.map(([x, y]) => new Vector(this, x, y));
        this.vectors2 = positions.map(([x, y]) => new Vector(this, x, y));
        this.vectors3 = positions.map(([x, y]) => new Vector(this, x, y));
    }
    update() {

        this.vectors1.forEach(vector => {
            vector.m_update(this.celestial1);
        });
        // this.vectors2.forEach(vector => {
        //     vector.m_update(this.celestial2);
        // });
        // this.vectors3.forEach(vector => {
        //     vector.v_update(this.vectors1[this.vectors1.length - 1], this.vectors2[this.vectors2.length - 1]);
        // });
        this.celestial1.m_update(this.celestial2);
        this.celestial2.m_update(this.celestial1);

    }
    render(context) {
        // Clear the canvas.
        context.clearRect(0, 0, this.width, this.height);

        // Render the celestial objects.
        this.celestial1.draw(context);
        this.celestial2.draw(context);

        this.vectors1.forEach(vector => {
            vector.draw(context);
        });
        // this.vectors2.forEach(vector => {
        //     vector.draw(context);
        // });
        // this.vectors3.forEach(vector => {
        //     vector.draw(context);
        // });
    }
}

const effect = new Effect(canvas.width, canvas.height);

function animate() {
    requestAnimationFrame(() => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        effect.update();
        effect.render(ctx);
        animate();
    });
}

animate();