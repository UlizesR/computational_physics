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

class Vector {
    constructor(effect, x, y) {
        this.effect = effect;
        this.x = x;
        this.y = y;
        this.angle = 0;
        this.red = 255;
        this.green = 255;
        this.blue = 255;
    }
    draw(context) {
        context.beginPath();
        context.moveTo(this.x, this.y);
        context.lineTo(this.x + Math.cos(this.angle) * 10, this.y + Math.sin(this.angle) * 10);
        ctx.strokeStyle = `rgb(${this.red}, ${this.green}, ${this.blue})`;
        context.stroke();
        context.closePath();
    }
    m_update() {
        // Calculate the angle between the Vector and the Celestial objects.
        const dx1 = this.effect.celestial1.x - this.x;
        const dy1 = this.effect.celestial1.y - this.y;
        const dx2 = this.effect.celestial2.x - this.x;
        const dy2 = this.effect.celestial2.y - this.y;
        const distance1 = Math.sqrt(dx1 * dx1 + dy1 * dy1);
        const distance2 = Math.sqrt(dx2 * dx2 + dy2 * dy2);
        const angle1 = Math.atan2(dy1, dx1);
        const angle2 = Math.atan2(dy2, dx2);
        const g1 = this.effect.celestial1.g;
        const g2 = this.effect.celestial2.g;

        // Calculate the angle of the vector based on the distance to both Celestial objects and their g properties.
        const angle = Math.atan2(
            g1 * distance1 * Math.sin(angle1) + g2 * distance2 * Math.sin(angle2) * 100,
            g1 * distance1 * Math.cos(angle1) + g2 * distance2 * Math.cos(angle2) * 100
        );
        this.angle = angle;

        // Calculate the color of the vector based on its distance to the Celestial objects.
        const maxDistance = 500; // maximum distance for full blue color
        const minDistance = 50; // minimum distance for full red color
        const distanceRange = maxDistance - minDistance;
        const distanceRatio = (distance1 + distance2 - 2 * minDistance) / distanceRange;
        this.red = 255 * (1 - distanceRatio);
        this.green = 255 * distanceRatio * (1 - distanceRatio);
        this.blue = 255 * distanceRatio;
    }
}

class Celestial {
    constructor(effect, x, y, mass, radius, velocityX, velocityY, color) {
        this.effect = effect;
        this.x = x;
        this.y = y;
        this.mass = (mass * SCALE).toFixed(6);
        if (radius < 10000000)
            this.radius = (radius * SCALE / 25).toFixed(6);
        else
            this.radius = (radius * SCALE / 1000).toFixed(6);
        this.velocityX = velocityX;
        this.velocityY = velocityY;
        this.g = (G_CONST * mass) / (radius * radius);
        this.g = this.g.toFixed(6);
        this.color = color;

        console.log("mass: " + this.mass);
        console.log("radius: " + this.radius);
        console.log("g: " + this.g);
    }
    draw(context) {
        context.beginPath();
        context.arc(this.x, this.y, this.radius, 0, 2 * Math.PI);
        context.fillStyle = this.color;
        context.fill();
        context.closePath();
    }
    m_update(obj) {
        // calculate the distance between the celestial object and the other celestial object.
        const dx = obj.x - this.x;
        const dy = obj.y - this.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        const inv_distance = 1 / distance;
        const inv_distance_squared = inv_distance * inv_distance;

        const normalized_x = dx * inv_distance;
        const normalized_y = dy * inv_distance;

        // calculate the acceleration of the celestial object.
        const acceleration_x =  normalized_x * obj.g * inv_distance_squared;
        const acceleration_y =  normalized_y * obj.g * inv_distance_squared;

        // calculate the velocity of the celestial object.
        this.velocityX += acceleration_x;
        this.velocityY += acceleration_y;

        // Update the position of the celestial object based on its velocity.
        this.x += this.velocityX;
        this.y += this.velocityY;
    }
}

class Effect {
    constructor(width, height) {
        this.width = width;
        this.height = height;
        this.vectors = [];
        this.celestial1 = new Celestial(this, 500, 300, 1.989e30, 696e6, 0.1, 0, 'yellow');
        this.celestial2 = new Celestial(this, 800, 500, 5.972e24, 6378e3, 0.1, -0.2, 'blue');
        // this.init();

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

        this.vectors = positions.map(([x, y]) => new Vector(this, x, y));
    }
    update() {

        // this.vectors.forEach(vector => {
        //     vector.m_update();
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

        // this.vectors.forEach(vector => {
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