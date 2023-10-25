G_CONST = 6.67408e-11;

//  1 px = 100 000 km
SCALE = 1e-5;
AU = 149597870.7; // 1 AU = 149 597 870.7 km
AU_SCALE = AU * SCALE;

G_CONST_S = G_CONST / SCALE;

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
        const acceleration_x = normalized_x * obj.g * inv_distance_squared;
        const acceleration_y = normalized_y * obj.g * inv_distance_squared;

        // calculate the velocity of the celestial object.
        this.velocityX += acceleration_x;
        this.velocityY += acceleration_y;

        // Update the position of the celestial object based on its velocity.
        this.x += this.velocityX;
        this.y += this.velocityY;
    }
}