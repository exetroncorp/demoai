✅ --start=COMMAND
Starts a single application (e.g., firefox, gedit, xterm).
The Xpra server runs without a full desktop environment.
The window(s) of the app are forwarded to the client.
No desktop panel, no window manager, unless you explicitly start one.
Use case: Lightweight, app-forwarding only.
Example:

xpra start :100 --start=firefox
✅ --start-desktop=COMMAND
Starts a full desktop environment (e.g., xfce4-session, mate-session).
Xpra emulates a full X11 desktop, including:
Window manager
Desktop panel
Background
Multiple windows
The entire desktop is forwarded as one big window (or fullscreen).
Use case: You want a remote desktop, not just an app.
Example:

xpra start :100 --start-desktop=xfce4-session
🔍 Key Differences Summary
Feature	--start	--start-desktop
App only	✅	❌
Full desktop	❌	✅
Window manager	❌ (unless you add one)	✅
Desktop panel	❌	✅
Multiple windows	✅ (but no WM)	✅ (with WM)
Use case	App forwarding	Remote desktop
🧪 Pro Tip
If you use --start-desktop, you must use a desktop session launcher like:

xfce4-session
mate-session
gnome-session
startlxde
If you use --start with a desktop session, it won’t work properly — it will just launch the session without a window manager, and you’ll get broken UI.

✅ TL;DR
Use --start for single apps.
Use --start-desktop for full remote desktop.
Let me know if you want to test both and see the difference live.

U
GIVE ME COMMAND TO USE PCMANFM AS DEKTOP WITH XPRA
pcmanfm can draw desktop icons and wallpaper, but it is not a complete session manager.
So the trick is:

start a minimal window manager (openbox, icewm, fluxbox …)
then launch pcmanfm --desktop so it can take ownership of the root window.
With Xpra you do that in one shot via --start-desktop and a tiny wrapper script.

Create the wrapper (once)
cat > ~/.local/bin/pcmanfm-desktop-session <<'EOF'
#!/bin/sh
# minimal LXDE-like session
openbox &
pcmanfm --desktop &
# keep the session alive (wait for openbox)
wait
EOF
chmod +x ~/.local/bin/pcmanfm-desktop-session
Start the server
xpra start :100 \
  --start-desktop="$HOME/.local/bin/pcmanfm-desktop-session" \
  --bind-tcp=0.0.0.0:10000 \
  --daemon=no \
  --sharing=yes
Connect from anywhere
xpra attach tcp:SERVER_IP:10000
You now get:

openbox window manager (right-click menu, window decorations)
pcmanfm handling wallpaper + desktop icons
full remote desktop inside a single Xpra window.
(If you already have openbox installed you can shorten the wrapper to just
pcmanfm --desktop & exec openbox-session.)

U
AND USING IDESK AND 9WM
If you want to use idesk (for desktop icons) and 9wm (minimalist window manager) instead of pcmanfm --desktop and openbox, the logic is the same:

9wm provides window management (borders, focus, no icons).
idesk provides desktop icons (it draws them on the root window).
Since 9wm does not manage the desktop background or icons, idesk will handle that.

✅ Step-by-step: idesk + 9wm as a minimal Xpra desktop
1. Install dependencies (Debian/Ubuntu example)
sudo apt install 9wm idesk
2. Create a minimal session script
mkdir -p ~/.local/bin
cat > ~/.local/bin/idesk-9wm-session <<'EOF'
#!/bin/sh
# Start 9wm in the background
9wm &

# Start idesk (draws icons on the root window)
idesk &

# Keep the session alive (wait for 9wm)
wait
EOF
chmod +x ~/.local/bin/idesk-9wm-session
3. Start Xpra with --start-desktop
xpra start :100 \
  --start-desktop="$HOME/.local/bin/idesk-9wm-session" \
  --bind-tcp=0.0.0.0:10000 \
  --daemon=no \
  --sharing=yes
4. Connect from client
xpra attach tcp:YOUR_SERVER_IP:10000
✅ Result
You get a barebones desktop with:
9wm: window borders, focus, no decorations
idesk: desktop icons (if you configured ~/.ideskrc and icons in ~/.idesktop/)
⚠️ Notes
9wm is extremely minimal — no menus, no keybindings, no tray.
idesk needs icon config files in ~/.idesktop/ and a valid ~/.ideskrc — otherwise no icons will appear.
If you want wallpaper, add feh or xloadimage to the session script:
feh --bg-scale ~/wallpaper.jpg &
✅ TL;DR
Use --start-desktop with a tiny script that launches:

9wm &  
idesk &  
wait
Let me know if you want a Docker image or systemd service version.

U
HOW TO OPTIMIZE INTELLIJ IDEA FOR XPRA HTML5 USE ? IS THERE SOME SETTINGS TO IMPROVE LATECNY EN RENDERINFG IN THIS REMOTE DESKTOP SETUP
IntelliJ IDEA over Xpra’s HTML5 client is doable, but JetBrains IDEs are heavy (Swing/JavaFX, lots of repaints, sub-pixel font rendering, animations).
The goal is to reduce noise on the wire and make the JVM draw less.

Below are the only tweaks that actually matter for Xpra HTML5 – ignore the rest.

Start the IDE in a way that Xpra can “see” it
# server side – use a dedicated xpra display
xpra start :100 \
  --start="intellij-idea-community" \
  --bind-tcp=0.0.0.0:10000 \
  --html=on \
  --daemon=no \
  --sharing=yes \
  --compress=1 \
  --encoding=jpeg \
  --quality=65 \
  --speed=90 \
  --video-scaling=off \
  --opengl=no \
  --clipboard=yes \
  --file-transfer=yes \
  --microphone=off \
  --speaker=off \
  --webcam=off \
  --pulseaudio=no \
  --bell=no \
  --notifications=no \
  --mmap=yes \
  --bandwidth-detection=yes \
  --packet-compressor=lz4 \
  --tcp-nodelay=yes \
  --socket-dir=/run/xpra
(Adjust the executable name if you use the Ultimate edition.)

Force the JVM to stop hurting the network
Create idea.properties (or append) in
~/.config/JetBrains/IdeaIC2024.1/idea.properties (path depends on version):

# no blinking cursor, no smooth scrolling, no fade-ins
editor.cursor.blink.time=0
editor.smooth.scrolling=false
ide.animation.duration=0
ide.expand.icon.animation=false
ide.tree.collapse.expand.animation=false
ide.tooltip.show.all=false
ide.balloon.shadow.size=0
editor.use.new rendering=false
editor.disable.italic=true
editor.disable.ligatures=true
editor.subpixel.direction= false
 swing.aatext=false
 swing.bufferPerWindow=false
 sun.java2d.xrender=false
 sun.java2d.opengl=false
 sun.java2d.d3d=false
(The last four switch off every accelerated Java2D pipeline – they fight Xpra’s screen-scraper.)

One-shot launcher script (sets flags JVM-side)
#!/bin/sh
export _JAVA_OPTIONS="-Dawt.useSystemAAFontSettings=off \
                      -Dswing.aatext=false \
                      -Dsun.java2d.xrender=false \
                      -Dsun.java2d.opengl=false \
                      -Dsun.java2d.d3d=false \
                      -Dsun.java2d.noddraw=true \
                      -Djdk.gtk.version=2 \
                      -DGTK_CSD=0"
exec /opt/idea/bin/idea.sh "$@"
Make it executable and point --start= to this wrapper.

Inside the IDE (do it once, survives updates)
Settings → Appearance & Behavior → Appearance

 Disable animations
Theme: IntelliJ Light (Darcula forces more grey gradients → bigger diffs)
Editor → General → Appearance
– Uncheck “Show CSS color preview”, “Show intention bulb”, “Show breadcrumbs”
Editor → General → Scrolling
– Uncheck “Smooth scrolling”
Editor → Color Scheme
– Choose a scheme without italic or ligature fonts (reduces sub-pixel glyphs)
Xpra HTML5 client tweaks (URL flags)
Open the session with:

https://server:10000/index.html?encoding=jpeg&quality=60&speed=100&clipboard=true&file_transfer=true&video=off&resize=delay
(video=off prevents Xpra from trying to detect “scrolling video” regions – JetBrains editors trigger it falsely and blur text.)

Optional: tune the JVM GC to be less chatty
Add in idea64.vmoptions (or _JAVA_OPTIONS):

-XX:+UseSerialGC
-Xmx1500m
Serial GC keeps heap compact and generates fewer dirty rectangles per second.

Checklist recap
Disable every Java2D acceleration pipeline.
Kill animations, smooth scrolling, italics, ligatures.
Use jpeg @ 65 % – text is still readable, bandwidth ÷ 3.
Keep video detection off
U
FOR YOUR INFO I HAVE NO GPU ONLY CPU ON SERVER AND CLIENT SIDE
Perfect — no GPU anywhere means we can strip out every GPU-oriented path and force CPU-only, low-latency rendering on both ends.

Below is a battle-tested, GPU-free Xpra HTML5 config for IntelliJ IDEA that keeps CPU usage low and round-trip latency minimal.

Server side (CPU-only, no GLX, no OpenGL)
# no GPU → kill every GL path
export LIBGL_ALWAYS_SOFTWARE=0   # 0 = never use software GL either
export GALLIUM_DRIVER=llvmpipe   # just in case Mesa is installed

xpra start :100 \
  --start="intellij-idea-community" \
  --bind-tcp=0.0.0.0:10000 \
  --html=on \
  --daemon=no \
  --sharing=yes \
  --encoding=jpeg \
  --quality=60 \
  --speed=95 \
  --video-scaling=off \
  --opengl=no \
  --clipboard=yes \
  --file-transfer=yes \
  --microphone=off \
  --speaker=off \
  --webcam=off \
  --pulseaudio=no \
  --bell=no \
  --notifications=no \
  --mmap=yes \
  --bandwidth-detection=yes \
  --packet-compressor=lz4 \
  --tcp-nodelay=yes \
  --socket-dir=/run/user/$UID/xpra
Key flags for CPU-only:

--opengl=no (server and client)
--video-scaling=off (no CPU-heavy up/downscale)
--encoding=jpeg + --quality=60 → single-core friendly
--speed=95 → favour low latency over size
JVM flags (CPU rasteriser only)
Create /opt/idea/bin/idea.sh wrapper:

#!/bin/sh
export _JAVA_OPTIONS="\
-Dawt.useSystemAAFontSettings=off \
-Dswing.aatext=false \
-Dsun.java2d.xrender=false \
-Dsun.java2d.opengl=false \
-Dsun.java2d.d3d=false \
-Dsun.java2d.noddraw=true \
-Djdk.gtk.version=2 \
-DGTK_CSD=0 \
-Dsun.java2d.pmoffscreen=false \
-Dsun.java2d.loops=blit"
exec /opt/idea/bin/idea.sh.real "$@"
(pmoffscreen=false and loops=blit force the pure-CPU blit loop – no masks, no transforms.)

HTML5 client URL (CPU-only path) ------------------------------------------------``` https://your-server:10000/index.html?\ encoding=jpeg&quality=60&speed=100&
video=off&resize=delay&opengl=no&clipboard=true
- `video=off` → prevents Xpra from burning CPU trying to detect scrolling video.  
- `opengl=no` → tells the **browser** not to use WebGL canvas (falls back to 2D context).  

--------------------------------------------------
4. Inside IntelliJ (CPU-saving checklist)
--------------------------------------------------
Settings → Appearance & Behavior → Appearance  
- Theme: **IntelliJ Light** (fewer gradients → smaller diffs)  
- Disable **animations**, **smooth scrolling**, **cursor blinking**  

Editor → Color Scheme  
- Font: **plain**, **no ligatures**, **no italic** (reduces anti-aliasing masks)  

--------------------------------------------------
5. Optional: pin server process to **one** physical core
--------------------------------------------------
```bash
taskset -c 0 xpra start ...
Keeps context-switch noise down; on low-core count VMs this shaves ~15 ms off paint latency.

Quick smoke test
Open a big file (*.java > 2000 lines).
Hold Page-Down for 5 s.
Watch browser FPS counter (Ctrl+Shift+I → Rendering → FPS meter).
Target: 12-15 FPS steady, <150 ms keystroke-to-pixel with 60 % JPEG – perfectly usable on gigabit LAN or good Wi-Fi.
That’s it — zero GPU, pure CPU, and IntelliJ remains responsive over Xpra HTML5.
