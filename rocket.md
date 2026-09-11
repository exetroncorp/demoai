Here's a ready-to-use, copy-paste prompt engineered to get a high-quality single-file result. Paste it as-is into the AI of your choice:

Task
Build an interactive 3D rocket launch simulator as a single self-contained HTML file. All HTML, CSS, and JavaScript must live in one file that runs directly in the browser — no build step, no separate assets. Load Three.js from a CDN (pin a specific version, use an import map + ES modules) and include OrbitControls from the same source. No external 3D models, textures, or audio files — generate all geometry procedurally and all sound with the Web Audio API.

Scene & Rocket
Procedural rocket from Three.js primitives: cone nose, cylinder body sections, trapezoid fins, lathe-geometry engine bell, interstage rings, RCS blocks, launch escape tower (jettisons early). Two stages minimum.
Launch complex: concrete pad with flame trench, truss service tower, hold-down clamps, lightning masts.
Environment: large ground plane with vertex-color noise, distant low-poly mountains, fog. As altitude climbs, the sky fades to black, stars fade in (Points), fog disappears, and a subtle atmospheric glow shows at the horizon.
Physics (simplified but believable)
Semi-implicit Euler integration, fixed timestep with accumulator, delta-time independent.
Forces: gimbaled thrust (±10°) along the rocket axis, gravity, aerodynamic drag (Cd ≈ 0.4, exponential air-density falloff, scale height ~8.5 km), and decreasing mass as fuel burns (per-stage dry + fuel mass).
Manual stage separation (S key): jettison the spent stage with retro-thrust and spawn tumbling debris that falls with drag.
Compute dynamic pressure and flag Max Q.
Controls
Keys: Z/X or ↑/↓ = throttle, A/D or ←/→ = gimbal pitch/yaw, Space = ignition/countdown, S = stage separation, C = cycle camera, M = map/orbit view, R = restart, P = pause, N = mute.
Mouse: free orbit in ground-camera mode, scroll to zoom.
Show a collapsible on-screen controls panel.
Cameras (cycle with C)
Chase cam with smooth lag and shake proportional to thrust/dynamic pressure
Onboard cam looking down at the receding ground
Ground/pad tracking cam that pans to follow the rocket
Free orbit camSubtle FOV increase with speed; shake peaks near Max Q.
Effects
Engine plume: pooled particle system + additive cone mesh whose length/width responds to throttle and ambient pressure (plume widens in vacuum).
Ignition smoke billowing across the pad; separation puff + debris.
Plasma glow on the nose when speed exceeds a threshold in atmosphere.
Shadow-mapped sun, hemisphere fill, ACES tone mapping; 60 FPS target (InstancedMesh/pooled particles, pixelRatio capped at 2, handle resize).
HUD / UI
Mission clock (T-minus countdown → T+), altitude (m/km), vertical & total velocity, throttle bar, per-stage fuel bars, dynamic pressure with Max Q marker, estimated apoapsis, G-force.
Timestamped event log: Ignition, Liftoff, Max Q, MECO, Stage separation, Apogee, Touchdown/Crash.
End states: crash (high impact speed), soft landing, or "Kármán line reached" at 100 km.
Design: monospaced numerals, restrained dark HUD, no emoji — inline SVG icons only.
Audio
Procedural Web Audio: filtered-noise rumble tracking throttle and camera distance, deep ignition bass, separation thump. Mute toggle.

Quality bar
First impression must feel cinematic: pre-launch idle with vapor wisps and a slow ambient camera, then a dramatic countdown.
Clean code organized into modules (Physics, Effects, HUD, Input, Audio) inside the single file, with comments.
Deliver one complete runnable HTML file with no console errors and every key/button working.
Tips for tuning the prompt:

Harder simulation — add: "Extend with simple orbital mechanics: tangential velocity, apoapsis/periapsis markers, and gravity turn guidance hints."
Different destination — add: "Offer Earth / Moon / Mars presets that change gravity, atmosphere density, and terrain color."
Mobile support — add: "Add touch controls: virtual joystick for gimbal, throttle slider, and a stage button."
Shorter output — if the result gets cut off, follow up with: "Continue exactly where you left off, same file."
Want me to just build the simulator for you directly instead?
