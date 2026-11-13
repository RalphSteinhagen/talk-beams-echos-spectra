// @name    wavepackets
// @uses    background
// @author  R. J. Steinhagen (GSI/FAIR), written with Claude for this deck
// @source  own work; the idea after https://www.shadertoy.com/view/7dBSz3, the author's reference (its code not used)
// @licence the deck's own
// @channel0 chalk-top.jpg wrap=clamp
// @channel1 chalk-middle.jpg wrap=clamp
// @channel2 chalk-bottom.jpg wrap=clamp
// @channel3 fair-gsi-logo.png wrap=clamp
// @param   strength float 1.0 0.0 4.0
// @param   shade    float 1.0 0.0 4.0

// The title master's chalkboard, re-composed from its three strips as make-masters.py does (top 200 px and bottom
// 90 px keep their shape, the middle stretches), distorted by wave packets travelling horizontally: each packet is a
// longitudinal (sound-like) displacement in its own lane, its envelope moving at its own group velocity and its carrier
// at a different phase velocity, so the ripples slide through the packet (dispersion); all travel left to right,
// with carrier wavelengths from ~8 to ~80 px and amplitudes from faint to full; about one packet in five is a big,
// longer and taller swell (2.2-3.5x), the rest stay small. The compression shades the
// chalk a little. The FAIR/GSI logo is drawn back on top at the master's place, undistorted; everything the slide puts
// on the board (the GREMLIN logo, the link) is drawn after the background and is not touched.
// `strength` scales the displacement (1: up to ~6 px at 1600 px width), `shade` the brightness ripple.

const int   N   = 24;
const float TAU = 6.28318530718;

float hash(float n) { return fract(sin(n * 127.1) * 43758.5453123); }

// x displacement (in packet amplitudes) and normalised compression at p (x in slide widths, y from the top in widths)
vec2 packets(vec2 p, float t, float depth) {
    float d = 0.0;
    float c = 0.0;
    for (int i = 0; i < N; ++i) {
        float f   = float(i) + 1.0;
        float y0  = (0.04 + 0.92 * hash(f * 1.31)) * depth;   // its lane
        float sy  = mix(0.012, 0.040, hash(f * 2.17));        // lane half-width
        float sx  = mix(0.035, 0.110, hash(f * 3.71));        // packet length
        float lam = mix(0.005, 0.050, pow(hash(f * 4.93), 1.5)); // carrier wavelength: from fine ripples to long swells
        float vg  = mix(0.020, 0.100, hash(f * 5.59));        // all travel left to right, each at its own speed
        float vp  = vg * mix(0.55, 1.8, hash(f * 7.43));      // phase velocity != group velocity
        float amp = mix(0.15, 1.0, pow(hash(f * 8.27), 0.7)); // from faint to strong ...
        if (hash(f * 11.3) < 0.22) {                           // ... and about one in five a big, pronounced swell
            amp *= mix(2.2, 3.5, hash(f * 12.1));
            sx  *= 1.4;
            sy  *= 1.6;
        }
        float L   = 1.0 + 6.0 * sx;                           // enters and leaves the board smoothly
        float xc  = mod(hash(f * 9.13) * L + vg * t, L) - 3.0 * sx;
        float dx  = p.x - xc;
        float dy  = p.y - y0;
        float env = amp * exp(-0.5 * (dx * dx / (sx * sx) + dy * dy / (sy * sy)));
        float ph  = TAU / lam * (p.x - vp * t) + TAU * hash(f * 10.7);
        d += env * sin(ph);
        c -= env * cos(ph);
    }
    return vec2(d, c);
}

vec3 chalk(vec2 q, float s, vec2 R) {   // q in pixels from the top left
    float yTop = 200.0 * s;
    float hBot = 90.0 * s;
    float yBot = R.y - hBot;
    float u    = clamp(q.x / R.x, 0.0, 1.0);
    if (q.y < yTop) {
        return textureLod(iChannel0, vec2(u, 1.0 - clamp(q.y / yTop, 0.0, 1.0)), 0.0).rgb;
    }
    if (q.y < yBot) {
        return textureLod(iChannel1, vec2(u, 1.0 - (q.y - yTop) / (yBot - yTop)), 0.0).rgb;
    }
    return textureLod(iChannel2, vec2(u, 1.0 - clamp((q.y - yBot) / hBot, 0.0, 1.0)), 0.0).rgb;
}

void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2  R   = iResolution.xy;
    float s   = R.x / 1600.0;
    vec2  q   = vec2(fragCoord.x, R.y - fragCoord.y);
    vec2  w   = packets(q / R.x, iTime, R.y / R.x);
    vec3  col = chalk(q + vec2(strength * 6.0 * s * w.x, 0.0), s, R) * (1.0 + shade * 0.07 * w.y);
    // the FAIR/GSI logo where the master has it (24.10-27.30 cm by 14.35-15.15 cm of 28 by 15.75), not distorted
    vec2 size = vec2(181.9, 45.71) * s;
    vec2 lp   = (q - vec2(1377.6 * s, R.y - 80.0 * s)) / size;
    if (lp.x >= 0.0 && lp.x <= 1.0 && lp.y >= 0.0 && lp.y <= 1.0) {
        vec4 logo = textureLod(iChannel3, vec2(lp.x, 1.0 - lp.y), max(log2(iChannelResolution[3].x / size.x), 0.0));
        col = mix(col, logo.rgb, logo.a);
    }
    fragColor = vec4(col, 1.0);
}
