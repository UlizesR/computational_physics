G_CONST = 6.67408e-11;

//  1 px = 100 000 km
SCALE = 1e-5;
AU = 149597870.7; // 1 AU = 149 597 870.7 km
AU_SCALE = AU * SCALE;
console.log(AU_SCALE);

G_CONST_S = G_CONST / SCALE;

class Vector {
    constructor(effect, x, y) {
        this.effect = effect;
        this.x = x;
        this.y = y;
        this.angle = 0;
        this.red = 255;
        this.green = 255;
        this.blue = 255;
        this.length = 0;
    }
    draw(context) {
        context.beginPath();
        context.moveTo(this.x, this.y);
        context.lineTo(this.x + Math.cos(this.angle) * this.length, this.y + Math.sin(this.angle) * this.length);
        ctx.strokeStyle = `rgb(${this.red}, ${this.green}, ${this.blue})`;
        context.stroke();
        context.closePath();
    }
    m_update(cest) {
        // Calculate the angle between the Vector and the Celestial objects.
        const dx1 = cest.x - this.x;
        const dy1 = cest.y - this.y;
        const distance1 = Math.sqrt(dx1 * dx1 + dy1 * dy1);
        const angle1 = Math.atan2(dy1, dx1);
        const g1 = Math.min(100000, G_CONST * cest.mass / (distance1 * distance1))
        // console.log("g1: " + g1);

        // Calculate the angle of the vector based on the distance to both Celestial objects and their g properties.
        const angle = Math.atan2(
            g1 * distance1 * Math.sin(angle1) * 100,
            g1 * distance1 * Math.cos(angle1) * 100
        );
        this.angle = angle;
        this.length = Math.min(10, g1/100000);


        // const maxDistance = 25; // maximum distance for full blue color
        // const minDistance = 500; // minimum distance for full red color
        // const distanceRange = maxDistance - minDistance;
        // const distanceRatio = Math.max(0, Math.min(1, (distance1 - minDistance) / distanceRange));

        // if (distanceRatio < 0.5) {
        //     // Interpolate between blue and green in the first half of the range
        //     this.red = 0;
        //     this.green = 255 * 2 * distanceRatio;
        //     this.blue = 255 * (1 - 2 * distanceRatio);
        // } else {
        //     // Interpolate between green and red in the second half of the range
        //     this.red = 255 * 2 * (distanceRatio - 0.5);
        //     this.green = 255 * (1 - 2 * (distanceRatio - 0.5));
        //     this.blue = 0;
        // }
    }
    v_update(vec1, vec2) {
        // Calculate the angle between the two vectors.
        const dx1 = vec1.x - this.x;
        const dy1 = vec1.y - this.y;
        const dx2 = vec2.x - this.x;
        const dy2 = vec2.y - this.y;
        const angle1 = Math.atan2(dy1, dx1);
        const angle2 = Math.atan2(dy2, dx2);

        // Calculate the average angle between the two vectors.
        const angle = (angle1 + angle2) / 2;
        this.angle = angle;
    }
}