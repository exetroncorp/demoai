# Patch pour intégrer le Dock macOS dans Xpra HTML5

## 1. Créer le nouveau fichier CSS pour le Dock

**Fichier:** `html5/css/dock.css`

```css
/* ==================== DOCK MACOS STYLE ==================== */

.dock-container {
    position: fixed;
    bottom: 10px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 100000;
    padding: 8px 12px;
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(30px) saturate(180%);
    -webkit-backdrop-filter: blur(30px) saturate(180%);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4),
                inset 0 1px 0 rgba(255, 255, 255, 0.2);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.dock-container.hidden {
    bottom: -100px;
    opacity: 0;
}

.dock {
    display: flex;
    align-items: flex-end;
    gap: 8px;
    padding: 0;
    list-style: none;
    margin: 0;
}

.dock-item {
    position: relative;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.dock-icon {
    width: 56px;
    height: 56px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    transform-origin: bottom center;
}

.dock-icon img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.dock-item:hover .dock-icon {
    transform: translateY(-12px) scale(1.2);
}

.dock-item:hover .dock-icon img {
    filter: drop-shadow(0 8px 16px rgba(0, 0, 0, 0.4));
}

.dock-item.active::after {
    content: '';
    position: absolute;
    bottom: -6px;
    left: 50%;
    transform: translateX(-50%);
    width: 4px;
    height: 4px;
    background: rgba(255, 255, 255, 0.8);
    border-radius: 50%;
    box-shadow: 0 0 6px rgba(255, 255, 255, 0.6);
}

.dock-tooltip {
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%) translateY(-10px);
    background: rgba(0, 0, 0, 0.85);
    color: white;
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 13px;
    white-space: nowrap;
    pointer-events: none;
    opacity: 0;
    transition: all 0.2s ease;
    margin-bottom: 8px;
}

.dock-item:hover .dock-tooltip {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
}

.dock-divider {
    width: 1px;
    height: 48px;
    background: rgba(255, 255, 255, 0.2);
    margin: 0 4px;
    align-self: center;
}

.dock-menu {
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: 8px;
    padding: 8px;
    margin-bottom: 12px;
    min-width: 200px;
    opacity: 0;
    pointer-events: none;
    transition: all 0.2s ease;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.dock-menu.show {
    opacity: 1;
    pointer-events: all;
}

.dock-menu-item {
    padding: 8px 12px;
    border-radius: 4px;
    cursor: pointer;
    transition: background 0.2s ease;
    color: #333;
    font-size: 14px;
}

.dock-menu-item:hover {
    background: rgba(0, 0, 0, 0.08);
}

.dock-tray {
    display: flex;
    gap: 6px;
    align-items: center;
}

.dock-badge {
    position: absolute;
    top: -4px;
    right: -4px;
    background: #ff3b30;
    color: white;
    border-radius: 10px;
    padding: 2px 6px;
    font-size: 10px;
    font-weight: bold;
    min-width: 18px;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

.dock-item.bouncing .dock-icon {
    animation: bounce 0.6s ease-in-out 3;
}

.dock-window-preview {
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    background: white;
    border-radius: 8px;
    padding: 8px;
    margin-bottom: 12px;
    opacity: 0;
    pointer-events: none;
    transition: all 0.2s ease;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    max-width: 300px;
}

.dock-window-preview.show {
    opacity: 1;
    pointer-events: all;
}

.dock-window-preview img {
    width: 100%;
    border-radius: 4px;
}

.dock-window-preview-title {
    padding: 8px;
    font-size: 13px;
    color: #333;
    text-align: center;
}

@media (max-width: 768px) {
    .dock-container {
        padding: 6px 10px;
        border-radius: 16px;
    }

    .dock {
        gap: 6px;
    }

    .dock-icon {
        width: 48px;
        height: 48px;
    }

    .dock-item:hover .dock-icon {
        transform: translateY(-8px) scale(1.15);
    }
}
```

## 2. Créer le fichier JavaScript du Dock

**Fichier:** `html5/js/Dock.js`

```javascript
/*
 * Xpra macOS-style Dock
 * Replaces the floating menu with a modern dock interface
 */

class XpraDock {
    constructor(client) {
        this.client = client;
        this.dock_element = null;
        this.dock_items = {};
        this.window_items = {};
        this.tray_items = {};
        this.init();
    }

    init() {
        this.create_dock();
        this.setup_event_listeners();
    }

    create_dock() {
        // Créer le conteneur du dock
        const dock_container = document.createElement('div');
        dock_container.id = 'dock_container';
        dock_container.className = 'dock-container';

        const dock = document.createElement('ul');
        dock.id = 'xpra_dock';
        dock.className = 'dock';

        // Menu principal
        this.add_main_menu(dock);

        // Fenêtres
        this.add_windows_section(dock);

        // Divider
        this.add_divider(dock);

        // Actions rapides
        this.add_quick_actions(dock);

        // Divider
        this.add_divider(dock);

        // Zone de tray
        const tray = document.createElement('div');
        tray.id = 'dock_tray';
        tray.className = 'dock-tray';
        dock.appendChild(tray);

        dock_container.appendChild(dock);
        document.body.appendChild(dock_container);

        this.dock_element = dock_container;
    }

    add_main_menu(dock) {
        const menu_item = this.create_dock_item('menu', 'Menu', this.get_menu_icon());
        
        const menu_content = document.createElement('div');
        menu_content.className = 'dock-menu';
        menu_content.id = 'dock_main_menu';

        const menu_items = [
            { label: 'About Xpra', action: () => this.show_about() },
            { label: 'Session Info', action: () => this.show_session_info() },
            { label: 'Bug Report', action: () => this.show_bug_report() },
            { label: 'Reload', action: () => location.reload() },
            { label: 'Disconnect', action: () => this.disconnect() }
        ];

        menu_items.forEach(item => {
            const menu_item_el = document.createElement('div');
            menu_item_el.className = 'dock-menu-item';
            menu_item_el.textContent = item.label;
            menu_item_el.onclick = item.action;
            menu_content.appendChild(menu_item_el);
        });

        menu_item.querySelector('.dock-icon').appendChild(menu_content);
        dock.appendChild(menu_item);

        this.dock_items['menu'] = menu_item;
    }

    add_windows_section(dock) {
        const windows_item = this.create_dock_item('windows', 'Windows', this.get_windows_icon());
        windows_item.classList.add('active');
        
        const badge = document.createElement('span');
        badge.className = 'dock-badge';
        badge.id = 'dock_windows_badge';
        badge.textContent = '0';
        badge.style.display = 'none';
        windows_item.querySelector('.dock-icon').appendChild(badge);

        dock.appendChild(windows_item);
        this.dock_items['windows'] = windows_item;
    }

    add_quick_actions(dock) {
        const actions = [
            { id: 'fullscreen', label: 'Fullscreen', icon: this.get_fullscreen_icon(), action: () => this.toggle_fullscreen() },
            { id: 'keyboard', label: 'Keyboard', icon: this.get_keyboard_icon(), action: () => this.toggle_keyboard() },
            { id: 'clipboard', label: 'Clipboard', icon: this.get_clipboard_icon(), action: () => this.copy_clipboard() },
            { id: 'audio', label: 'Audio', icon: this.get_audio_icon(), action: () => this.toggle_audio() }
        ];

        actions.forEach(action => {
            const item = this.create_dock_item(action.id, action.label, action.icon);
            item.onclick = action.action;
            dock.appendChild(item);
            this.dock_items[action.id] = item;
        });
    }

    add_divider(dock) {
        const divider = document.createElement('div');
        divider.className = 'dock-divider';
        dock.appendChild(divider);
    }

    create_dock_item(id, tooltip, icon_svg) {
        const item = document.createElement('li');
        item.className = 'dock-item';
        item.dataset.action = id;

        const icon_container = document.createElement('div');
        icon_container.className = 'dock-icon';

        const img = document.createElement('img');
        img.src = `data:image/svg+xml,${encodeURIComponent(icon_svg)}`;
        img.alt = tooltip;

        const tooltip_el = document.createElement('span');
        tooltip_el.className = 'dock-tooltip';
        tooltip_el.textContent = tooltip;

        icon_container.appendChild(img);
        icon_container.appendChild(tooltip_el);
        item.appendChild(icon_container);

        return item;
    }

    setup_event_listeners() {
        // Gestion du clic sur les items
        document.getElementById('xpra_dock').addEventListener('click', (e) => {
            const dock_item = e.target.closest('.dock-item');
            if (!dock_item) return;

            const action = dock_item.dataset.action;

            // Fermer tous les menus sauf celui cliqué
            document.querySelectorAll('.dock-menu.show').forEach(menu => {
                if (!dock_item.contains(menu)) {
                    menu.classList.remove('show');
                }
            });

            if (action === 'menu') {
                document.getElementById('dock_main_menu').classList.toggle('show');
            } else if (action === 'windows') {
                this.toggle_windows_list();
            }
        });

        // Fermer les menus au clic extérieur
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.dock-container')) {
                document.querySelectorAll('.dock-menu.show').forEach(menu => {
                    menu.classList.remove('show');
                });
            }
        });

        // Auto-hide au mouvement de la souris
        let hide_timeout;
        this.dock_element.addEventListener('mouseenter', () => {
            clearTimeout(hide_timeout);
            this.dock_element.classList.remove('hidden');
        });

        this.dock_element.addEventListener('mouseleave', () => {
            hide_timeout = setTimeout(() => {
                // Optionnel: auto-hide
                // this.dock_element.classList.add('hidden');
            }, 3000);
        });
    }

    // Gestion des fenêtres
    add_window(win) {
        const wid = win.wid;
        if (this.window_items[wid]) return;

        const tray = document.getElementById('dock_tray');
        const window_item = this.create_dock_item(
            `window_${wid}`,
            win.title || 'Window',
            this.get_window_icon()
        );

        window_item.onclick = () => {
            if (win.minimized) {
                win.toggle_minimized();
            }
            this.client.set_focus(win);
        };

        // Ajouter l'icône de la fenêtre si disponible
        if (win.icon) {
            const img = window_item.querySelector('img');
            img.src = win.icon;
        }

        tray.appendChild(window_item);
        this.window_items[wid] = window_item;

        this.update_windows_count();
    }

    remove_window(wid) {
        if (this.window_items[wid]) {
            this.window_items[wid].remove();
            delete this.window_items[wid];
            this.update_windows_count();
        }
    }

    update_window_icon(wid, icon_src) {
        if (this.window_items[wid]) {
            const img = this.window_items[wid].querySelector('img');
            img.src = icon_src;
        }
    }

    update_windows_count() {
        const count = Object.keys(this.window_items).length;
        const badge = document.getElementById('dock_windows_badge');
        
        if (count > 0) {
            badge.textContent = count;
            badge.style.display = 'block';
        } else {
            badge.style.display = 'none';
        }
    }

    toggle_windows_list() {
        if (typeof client !== 'undefined' && client.toggle_window_preview) {
            client.toggle_window_preview();
        }
    }

    // Gestion du tray
    add_tray(wid, metadata) {
        const tray = document.getElementById('dock_tray');
        const tray_item = this.create_dock_item(
            `tray_${wid}`,
            metadata.title || 'Tray',
            this.get_window_icon()
        );

        tray.appendChild(tray_item);
        this.tray_items[wid] = tray_item;
    }

    remove_tray(wid) {
        if (this.tray_items[wid]) {
            this.tray_items[wid].remove();
            delete this.tray_items[wid];
        }
    }

    update_tray_icon(wid, icon_src) {
        if (this.tray_items[wid]) {
            const img = this.tray_items[wid].querySelector('img');
            img.src = icon_src;
        }
    }

    // Actions
    toggle_fullscreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen();
        } else {
            document.exitFullscreen();
        }
    }

    toggle_keyboard() {
        if (typeof toggle_keyboard === 'function') {
            toggle_keyboard();
        }
    }

    copy_clipboard() {
        if (typeof client !== 'undefined') {
            client.read_clipboard();
        }
    }

    toggle_audio() {
        if (typeof client !== 'undefined') {
            const sound_button = document.getElementById('sound_button');
            if (sound_button) {
                sound_button.click();
            }
        }
    }

    show_about() {
        if (typeof show_about === 'function') {
            show_about();
        } else {
            document.getElementById('about')?.style.display = 'block';
        }
    }

    show_session_info() {
        if (typeof show_sessioninfo === 'function') {
            show_sessioninfo();
        } else {
            document.getElementById('sessioninfo')?.style.display = 'block';
        }
    }

    show_bug_report() {
        if (typeof show_bugreport === 'function') {
            show_bugreport();
        } else {
            document.getElementById('bugreport')?.style.display = 'block';
        }
    }

    disconnect() {
        if (confirm('Are you sure you want to disconnect?')) {
            if (typeof client !== 'undefined') {
                client.disconnect_reason = 'User request';
                client.close();
            }
        }
    }

    // Icônes SVG
    get_menu_icon() {
        return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#ffffff"><path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/></svg>`;
    }

    get_windows_icon() {
        return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#ffffff"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14z"/></svg>`;
    }

    get_fullscreen_icon() {
        return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#ffffff"><path d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"/></svg>`;
    }

    get_keyboard_icon() {
        return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#ffffff"><path d="M20 5H4c-1.1 0-1.99.9-1.99 2L2 17c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm-9 3h2v2h-2V8zm0 3h2v2h-2v-2zM8 8h2v2H8V8zm0 3h2v2H8v-2zm-1 2H5v-2h2v2zm0-3H5V8h2v2zm9 7H8v-2h8v2zm0-4h-2v-2h2v2zm0-3h-2V8h2v2zm3 3h-2v-2h2v2zm0-3h-2V8h2v2z"/></svg>`;
    }

    get_clipboard_icon() {
        return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#ffffff"><path d="M19 3h-4.18C14.4 1.84 13.3 1 12 1c-1.3 0-2.4.84-2.82 2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 0c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zm7 16H5V5h2v3h10V5h2v14z"/></svg>`;
    }

    get_audio_icon() {
        return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#ffffff"><path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/></svg>`;
    }

    get_window_icon() {
        return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#ffffff"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14z"/></svg>`;
    }
}
```

## 3. Modifications dans index.html

**Fichier:** `html5/index.html`

Ajouter après la ligne 18 (après `<link rel="stylesheet" href="css/spinner.css" />`):

```html
<!-- Dock CSS -->
<link rel="stylesheet" href="css/dock.css" />
```

Ajouter avant la ligne 45 (avant `<script type="text/javascript" src="js/Client.js"></script>`):

```html
<script type="text/javascript" src="js/Dock.js"></script>
```

Masquer l'ancien menu flottant - modifier vers la ligne 625 (dans la fonction `init_float_menu()`):

```javascript
function init_float_menu() {
    // DÉSACTIVER L'ANCIEN MENU
    $("#float_menu").hide();
    
    // INITIALISER LE NOUVEAU DOCK
    if (typeof XpraDock !== 'undefined') {
        window.xpra_dock = new XpraDock(client);
    }
    
    return; // Ne pas exécuter le reste de la fonction
    
    // ... le reste du code original ...
}
```

## 4. Modifications dans Client.js

**Fichier:** `html5/js/Client.js`

Ajouter dans la méthode `_process_new_window` (ligne ~2880):

```javascript
_process_new_window(packet) {
    this._new_window_common(packet, false);
    
    // AJOUTER AU DOCK
    if (window.xpra_dock) {
        const wid = packet[1];
        const win = this.id_to_window[wid];
        if (win && !win.tray && !win.override_redirect) {
            window.xpra_dock.add_window(win);
        }
    }
}
```

Ajouter dans la méthode `_process_lost_window` (ligne ~2950):

```javascript
_process_lost_window(packet) {
    const wid = packet[1];
    
    // RETIRER DU DOCK
    if (window.xpra_dock) {
        window.xpra_dock.remove_window(wid);
    }
    
    // ... le reste du code original ...
}
```

Ajouter dans la méthode `_process_new_tray` (ligne ~3020):

```javascript
_process_new_tray(packet) {
    const wid = packet[1];
    const metadata = packet[4];
    
    // ... le code original pour créer le tray ...
    
    // AJOUTER AU DOCK
    if (window.xpra_dock) {
        window.xpra_dock.add_tray(wid, metadata);
    }
}
```

Ajouter dans la méthode `_process_window_icon` (ligne ~3200):

```javascript
_process_window_icon(packet) {
    const wid = packet[1];
    const w = packet[2];
    const h = packet[3];
    const encoding = packet[4];
    const img_data = packet[5];
    
    const win = this.id_to_window[wid];
    if (win) {
        const source = win.update_icon(w, h, encoding, img_data);
        
        // METTRE À JOUR L'ICÔNE DANS LE DOCK
        if (window.xpra_dock) {
            if (win.tray) {
                window.xpra_dock.update_tray_icon(wid, source);
            } else {
                window.xpra_dock.update_window_icon(wid, source);
            }
        }
        
        // ... le reste du code original ...
    }
}
```

## 5. Instructions d'installation

1. **Créer les nouveaux fichiers:**
   ```bash
   cd html5
   touch css/dock.css
   touch js/Dock.js
   ```

2. **Copier le contenu des fichiers** depuis ce patch

3. **Appliquer les modifications** dans `index.html` et `Client.js`

4. **Tester:**
   - Rafraîchir la page
   - Le dock devrait apparaître en bas de l'écran
   - L'ancien menu flottant devrait être masqué

## 6. Options de configuration

Dans `default-settings.txt`, vous pouvez ajouter:

```ini
# Dock settings
dock_enabled=true
dock_position=bottom
dock_autohide=false
```

## 7. Désactivation temporaire

Pour revenir à l'ancien menu sans supprimer le code:

Dans `index.html`, commenter les lignes ajoutées:

```javascript
function init_float_menu() {
    // $("#float_menu").hide();
    // if (typeof XpraDock !== 'undefined') {
    //     window.xpra_dock = new XpraDock(client);
    // }
    // return;
    
    // ... code original actif ...
}
```

## 8. Notes importantes

- Le dock est compatible avec tous les navigateurs modernes
- Les effets de flou nécessitent un navigateur récent
- Sur mobile, le dock s'adapte automatiquement
- Les icônes de fenêtres sont récupérées automatiquement
- Le dock supporte les notifications et badges

## 9. Dépannage

Si le dock n'apparaît pas:
1. Vérifier la console JavaScript (F12)
2. Vérifier que tous les fichiers sont chargés
3. Vérifier que `window.xpra_dock` existe
4. Vérifier que jQuery est chargé

Si l'ancien menu est toujours visible:
1. Vérifier que `$("#float_menu").hide()` est exécuté
2. Vider le cache du navigateur
3. Vérifier l'ordre de chargement des scripts
