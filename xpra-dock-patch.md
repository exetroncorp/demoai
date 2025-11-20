# Patch Dock macOS inspiré de shadcn/ui pour Xpra HTML5

## 1. Créer le nouveau fichier CSS pour le Dock (Style shadcn/ui)

**Fichier:** `html5/css/dock.css`

```css
/* ==================== DOCK MACOS STYLE (shadcn/ui inspired) ==================== */

:root {
    --dock-bg: rgba(255, 255, 255, 0.8);
    --dock-border: rgba(0, 0, 0, 0.1);
    --dock-shadow: 0 0 0 1px rgba(0, 0, 0, 0.05), 0 20px 50px rgba(0, 0, 0, 0.2);
    --dock-item-size: 48px;
    --dock-item-gap: 8px;
    --dock-magnify-scale: 1.5;
    --dock-radius: 16px;
}

@supports (backdrop-filter: blur(20px)) or (-webkit-backdrop-filter: blur(20px)) {
    :root {
        --dock-bg: rgba(255, 255, 255, 0.7);
    }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
    :root {
        --dock-bg: rgba(30, 30, 30, 0.8);
        --dock-border: rgba(255, 255, 255, 0.15);
    }
}

.dock-container {
    position: fixed;
    bottom: 16px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 100000;
    padding: 8px;
    background: var(--dock-bg);
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border-radius: var(--dock-radius);
    border: 1px solid var(--dock-border);
    box-shadow: var(--dock-shadow);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.dock-container.hidden {
    transform: translateX(-50%) translateY(100px);
    opacity: 0;
    pointer-events: none;
}

/* Dock List */
.dock {
    display: flex;
    align-items: flex-end;
    justify-content: center;
    gap: var(--dock-item-gap);
    padding: 0;
    margin: 0;
    list-style: none;
    position: relative;
    height: var(--dock-item-size);
}

/* Dock Item */
.dock-item {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    transform-origin: bottom center;
}

.dock-icon {
    width: var(--dock-item-size);
    height: var(--dock-item-size);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    border-radius: 12px;
}

.dock-icon img,
.dock-icon svg {
    width: 85%;
    height: 85%;
    object-fit: contain;
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    pointer-events: none;
}

/* Magnification Effect (like macOS) */
.dock-item:hover {
    transform: translateY(-8px) scale(var(--dock-magnify-scale));
    z-index: 10;
}

.dock-item:hover .dock-icon img,
.dock-item:hover .dock-icon svg {
    filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.15));
}

/* Magnification des items adjacents */
.dock-item:has(+ .dock-item:hover),
.dock-item:hover + .dock-item {
    transform: translateY(-4px) scale(1.2);
}

.dock-item:has(+ .dock-item + .dock-item:hover),
.dock-item:hover + .dock-item + .dock-item {
    transform: translateY(-2px) scale(1.1);
}

/* Active Indicator (dot sous l'icône) */
.dock-item.active::before {
    content: '';
    position: absolute;
    bottom: -6px;
    left: 50%;
    transform: translateX(-50%);
    width: 4px;
    height: 4px;
    background: currentColor;
    border-radius: 50%;
    opacity: 0.6;
}

/* Bounce Animation pour notifications */
@keyframes dock-bounce {
    0%, 100% { transform: translateY(0) scale(1); }
    25% { transform: translateY(-12px) scale(1.05); }
    50% { transform: translateY(-6px) scale(1.02); }
    75% { transform: translateY(-9px) scale(1.03); }
}

.dock-item.bouncing {
    animation: dock-bounce 0.6s ease-in-out 2;
}

/* Tooltip */
.dock-tooltip {
    position: absolute;
    bottom: calc(100% + 12px);
    left: 50%;
    transform: translateX(-50%) scale(0.9);
    background: rgba(0, 0, 0, 0.9);
    color: white;
    padding: 6px 10px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 500;
    white-space: nowrap;
    pointer-events: none;
    opacity: 0;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 1000;
}

.dock-item:hover .dock-tooltip {
    opacity: 1;
    transform: translateX(-50%) scale(1);
}

/* Divider */
.dock-divider {
    width: 1px;
    height: 32px;
    background: var(--dock-border);
    margin: 0 4px;
    align-self: center;
    flex-shrink: 0;
}

/* Badge (notifications count) */
.dock-badge {
    position: absolute;
    top: -2px;
    right: -2px;
    min-width: 18px;
    height: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #ff3b30;
    color: white;
    border-radius: 9px;
    padding: 0 5px;
    font-size: 10px;
    font-weight: 700;
    line-height: 1;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    pointer-events: none;
    z-index: 2;
}

/* Menu contextuel */
.dock-menu {
    position: absolute;
    bottom: calc(100% + 12px);
    left: 50%;
    transform: translateX(-50%) translateY(4px);
    min-width: 200px;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: 10px;
    padding: 6px;
    opacity: 0;
    visibility: hidden;
    pointer-events: none;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15),
                0 0 0 1px rgba(0, 0, 0, 0.05);
    z-index: 1001;
}

@media (prefers-color-scheme: dark) {
    .dock-menu {
        background: rgba(40, 40, 40, 0.95);
    }
}

.dock-menu.show {
    opacity: 1;
    visibility: visible;
    pointer-events: all;
    transform: translateX(-50%) translateY(0);
}

.dock-menu-item {
    padding: 8px 12px;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.15s ease;
    color: #1a1a1a;
    font-size: 13px;
    display: flex;
    align-items: center;
    gap: 8px;
}

@media (prefers-color-scheme: dark) {
    .dock-menu-item {
        color: #ffffff;
    }
}

.dock-menu-item:hover {
    background: rgba(0, 0, 0, 0.05);
}

@media (prefers-color-scheme: dark) {
    .dock-menu-item:hover {
        background: rgba(255, 255, 255, 0.1);
    }
}

.dock-menu-separator {
    height: 1px;
    background: var(--dock-border);
    margin: 4px 0;
}

/* Window Preview Card */
.dock-window-list {
    position: absolute;
    bottom: calc(100% + 12px);
    left: 50%;
    transform: translateX(-50%) translateY(4px);
    min-width: 280px;
    max-width: 400px;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: 10px;
    padding: 8px;
    opacity: 0;
    visibility: hidden;
    pointer-events: none;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15),
                0 0 0 1px rgba(0, 0, 0, 0.05);
    z-index: 1001;
    max-height: 400px;
    overflow-y: auto;
}

@media (prefers-color-scheme: dark) {
    .dock-window-list {
        background: rgba(40, 40, 40, 0.95);
    }
}

.dock-window-list.show {
    opacity: 1;
    visibility: visible;
    pointer-events: all;
    transform: translateX(-50%) translateY(0);
}

.dock-window-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.15s ease;
}

.dock-window-item:hover {
    background: rgba(0, 0, 0, 0.05);
}

@media (prefers-color-scheme: dark) {
    .dock-window-item:hover {
        background: rgba(255, 255, 255, 0.1);
    }
}

.dock-window-item-icon {
    width: 32px;
    height: 32px;
    flex-shrink: 0;
}

.dock-window-item-icon img {
    width: 100%;
    height: 100%;
    object-fit: contain;
}

.dock-window-item-info {
    flex: 1;
    min-width: 0;
}

.dock-window-item-title {
    font-size: 13px;
    font-weight: 500;
    color: #1a1a1a;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

@media (prefers-color-scheme: dark) {
    .dock-window-item-title {
        color: #ffffff;
    }
}

.dock-window-item-subtitle {
    font-size: 11px;
    color: #666;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

@media (prefers-color-scheme: dark) {
    .dock-window-item-subtitle {
        color: #999;
    }
}

.dock-window-item-actions {
    display: flex;
    gap: 4px;
    opacity: 0;
    transition: opacity 0.15s ease;
}

.dock-window-item:hover .dock-window-item-actions {
    opacity: 1;
}

.dock-window-item-action {
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 4px;
    cursor: pointer;
    transition: background 0.15s ease;
}

.dock-window-item-action:hover {
    background: rgba(0, 0, 0, 0.1);
}

@media (prefers-color-scheme: dark) {
    .dock-window-item-action:hover {
        background: rgba(255, 255, 255, 0.15);
    }
}

.dock-window-item-action svg {
    width: 14px;
    height: 14px;
}

/* Tray Area */
.dock-tray {
    display: flex;
    gap: var(--dock-item-gap);
    align-items: center;
}

/* Responsive */
@media (max-width: 768px) {
    :root {
        --dock-item-size: 44px;
        --dock-item-gap: 6px;
        --dock-magnify-scale: 1.3;
    }

    .dock-container {
        bottom: 8px;
        padding: 6px;
        border-radius: 12px;
    }

    .dock-item:hover {
        transform: translateY(-6px) scale(var(--dock-magnify-scale));
    }
}

/* Scrollbar pour la liste des fenêtres */
.dock-window-list::-webkit-scrollbar {
    width: 6px;
}

.dock-window-list::-webkit-scrollbar-track {
    background: transparent;
}

.dock-window-list::-webkit-scrollbar-thumb {
    background: rgba(0, 0, 0, 0.2);
    border-radius: 3px;
}

.dock-window-list::-webkit-scrollbar-thumb:hover {
    background: rgba(0, 0, 0, 0.3);
}

@media (prefers-color-scheme: dark) {
    .dock-window-list::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.2);
    }
    
    .dock-window-list::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.3);
    }
}

/* Empty state */
.dock-window-list-empty {
    padding: 24px;
    text-align: center;
    color: #666;
    font-size: 13px;
}

@media (prefers-color-scheme: dark) {
    .dock-window-list-empty {
        color: #999;
    }
}
```

## 2. Créer le fichier JavaScript du Dock (Logique shadcn/ui)

**Fichier:** `html5/js/Dock.js`

```javascript
/*
 * Xpra macOS-style Dock (inspired by shadcn/ui)
 * Modern dock interface with magnification effect
 */

class XpraDock {
    constructor(client) {
        this.client = client;
        this.dock_element = null;
        this.dock_items = {};
        this.window_items = {};
        this.tray_items = {};
        this.active_menu = null;
        this.init();
    }

    init() {
        this.create_dock();
        this.setup_event_listeners();
        this.setup_magnification();
    }

    create_dock() {
        const dock_container = document.createElement('div');
        dock_container.id = 'dock_container';
        dock_container.className = 'dock-container';

        const dock = document.createElement('ul');
        dock.id = 'xpra_dock';
        dock.className = 'dock';

        // Menu principal
        this.add_main_menu(dock);

        // Fenêtres avec liste déroulante
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

        // Animation d'entrée
        setTimeout(() => {
            dock_container.style.transform = 'translateX(-50%)';
        }, 100);
    }

    add_main_menu(dock) {
        const menu_item = this.create_dock_item({
            id: 'menu',
            tooltip: 'Xpra Menu',
            icon: this.get_icon('menu'),
            color: '#007AFF'
        });
        
        const menu_content = document.createElement('div');
        menu_content.className = 'dock-menu';
        menu_content.id = 'dock_main_menu';

        const menu_items = [
            { 
                label: 'About Xpra', 
                icon: this.get_icon('info'),
                action: () => this.show_about() 
            },
            { 
                label: 'Session Info', 
                icon: this.get_icon('chart'),
                action: () => this.show_session_info() 
            },
            { 
                label: 'Bug Report', 
                icon: this.get_icon('bug'),
                action: () => this.show_bug_report() 
            },
            { type: 'separator' },
            { 
                label: 'Reload', 
                icon: this.get_icon('refresh'),
                action: () => location.reload() 
            },
            { 
                label: 'Disconnect', 
                icon: this.get_icon('logout'),
                action: () => this.disconnect(),
                danger: true
            }
        ];

        menu_items.forEach(item => {
            if (item.type === 'separator') {
                const separator = document.createElement('div');
                separator.className = 'dock-menu-separator';
                menu_content.appendChild(separator);
            } else {
                const menu_item_el = document.createElement('div');
                menu_item_el.className = 'dock-menu-item';
                if (item.danger) menu_item_el.style.color = '#ff3b30';
                
                if (item.icon) {
                    menu_item_el.innerHTML = item.icon;
                }
                
                const text = document.createElement('span');
                text.textContent = item.label;
                menu_item_el.appendChild(text);
                
                menu_item_el.onclick = (e) => {
                    e.stopPropagation();
                    this.close_all_menus();
                    item.action();
                };
                
                menu_content.appendChild(menu_item_el);
            }
        });

        menu_item.appendChild(menu_content);
        dock.appendChild(menu_item);

        this.dock_items['menu'] = menu_item;
    }

    add_windows_section(dock) {
        const windows_item = this.create_dock_item({
            id: 'windows',
            tooltip: 'Windows',
            icon: this.get_icon('windows'),
            color: '#34C759'
        });
        
        const badge = document.createElement('span');
        badge.className = 'dock-badge';
        badge.id = 'dock_windows_badge';
        badge.textContent = '0';
        badge.style.display = 'none';
        windows_item.querySelector('.dock-icon').appendChild(badge);

        // Liste des fenêtres
        const window_list = document.createElement('div');
        window_list.className = 'dock-window-list';
        window_list.id = 'dock_window_list';
        windows_item.appendChild(window_list);

        dock.appendChild(windows_item);
        this.dock_items['windows'] = windows_item;
    }

    add_quick_actions(dock) {
        const actions = [
            { 
                id: 'fullscreen', 
                tooltip: 'Fullscreen', 
                icon: this.get_icon('fullscreen'),
                color: '#FF9500',
                action: () => this.toggle_fullscreen() 
            },
            { 
                id: 'keyboard', 
                tooltip: 'Keyboard', 
                icon: this.get_icon('keyboard'),
                color: '#5856D6',
                action: () => this.toggle_keyboard() 
            },
            { 
                id: 'clipboard', 
                tooltip: 'Clipboard', 
                icon: this.get_icon('clipboard'),
                color: '#FF2D55',
                action: () => this.copy_clipboard() 
            },
            { 
                id: 'audio', 
                tooltip: 'Audio', 
                icon: this.get_icon('audio'),
                color: '#AF52DE',
                action: () => this.toggle_audio() 
            }
        ];

        actions.forEach(action => {
            const item = this.create_dock_item(action);
            item.onclick = (e) => {
                e.stopPropagation();
                action.action();
            };
            dock.appendChild(item);
            this.dock_items[action.id] = item;
        });
    }

    add_divider(dock) {
        const divider = document.createElement('div');
        divider.className = 'dock-divider';
        dock.appendChild(divider);
    }

    create_dock_item(config) {
        const { id, tooltip, icon, color } = config;
        
        const item = document.createElement('li');
        item.className = 'dock-item';
        item.dataset.action = id;
        if (color) item.style.color = color;

        const icon_container = document.createElement('div');
        icon_container.className = 'dock-icon';
        icon_container.innerHTML = icon;

        const tooltip_el = document.createElement('span');
        tooltip_el.className = 'dock-tooltip';
        tooltip_el.textContent = tooltip;

        icon_container.appendChild(tooltip_el);
        item.appendChild(icon_container);

        return item;
    }

    setup_event_listeners() {
        const dock = document.getElementById('xpra_dock');
        
        // Gestion des clics
        dock.addEventListener('click', (e) => {
            const dock_item = e.target.closest('.dock-item');
            if (!dock_item) return;

            const action = dock_item.dataset.action;

            if (action === 'menu') {
                this.toggle_menu('dock_main_menu');
            } else if (action === 'windows') {
                this.toggle_windows_list();
            }
        });

        // Fermer les menus au clic extérieur
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.dock-container')) {
                this.close_all_menus();
            }
        });

        // Gestion du hover pour masquer le dock (optionnel)
        let hide_timeout;
        
        this.dock_element.addEventListener('mouseenter', () => {
            clearTimeout(hide_timeout);
            this.dock_element.classList.remove('hidden');
        });

        this.dock_element.addEventListener('mouseleave', () => {
            // Optionnel: auto-hide après 3 secondes
            // hide_timeout = setTimeout(() => {
            //     this.dock_element.classList.add('hidden');
            // }, 3000);
        });

        // Montrer le dock quand la souris est en bas de l'écran
        document.addEventListener('mousemove', (e) => {
            if (e.clientY > window.innerHeight - 100) {
                clearTimeout(hide_timeout);
                this.dock_element.classList.remove('hidden');
            }
        });
    }

    setup_magnification() {
        const dock = document.getElementById('xpra_dock');
        const items = dock.querySelectorAll('.dock-item');
        
        // L'effet de magnification est géré par CSS avec :hover
        // Cette fonction peut être utilisée pour des effets additionnels
    }

    toggle_menu(menu_id) {
        const menu = document.getElementById(menu_id);
        if (!menu) return;

        const is_open = menu.classList.contains('show');
        this.close_all_menus();
        
        if (!is_open) {
            menu.classList.add('show');
            this.active_menu = menu;
        }
    }

    close_all_menus() {
        document.querySelectorAll('.dock-menu.show, .dock-window-list.show').forEach(menu => {
            menu.classList.remove('show');
        });
        this.active_menu = null;
    }

    toggle_windows_list() {
        const list = document.getElementById('dock_window_list');
        if (!list) return;

        const is_open = list.classList.contains('show');
        this.close_all_menus();
        
        if (!is_open) {
            this.update_windows_list();
            list.classList.add('show');
            this.active_menu = list;
        }
    }

    update_windows_list() {
        const list = document.getElementById('dock_window_list');
        list.innerHTML = '';

        const window_count = Object.keys(this.window_items).length;

        if (window_count === 0) {
            const empty = document.createElement('div');
            empty.className = 'dock-window-list-empty';
            empty.textContent = 'No windows open';
            list.appendChild(empty);
            return;
        }

        // Trier les fenêtres par ordre de focus
        const windows = Object.entries(this.window_items)
            .sort(([, a], [, b]) => (b.win.stacking_layer || 0) - (a.win.stacking_layer || 0));

        windows.forEach(([wid, item]) => {
            const win_item = this.create_window_list_item(item.win);
            list.appendChild(win_item);
        });
    }

    create_window_list_item(win) {
        const item = document.createElement('div');
        item.className = 'dock-window-item';

        // Icône
        const icon = document.createElement('div');
        icon.className = 'dock-window-item-icon';
        icon.innerHTML = `<img src="${win.icon || 'favicon.png'}" alt="">`;

        // Info
        const info = document.createElement('div');
        info.className = 'dock-window-item-info';
        
        const title = document.createElement('div');
        title.className = 'dock-window-item-title';
        title.textContent = win.title || 'Window';
        
        const subtitle = document.createElement('div');
        subtitle.className = 'dock-window-item-subtitle';
        subtitle.textContent = win.minimized ? 'Minimized' : 'Active';
        
        info.appendChild(title);
        info.appendChild(subtitle);

        // Actions
        const actions = document.createElement('div');
        actions.className = 'dock-window-item-actions';

        const minimize_btn = document.createElement('div');
        minimize_btn.className = 'dock-window-item-action';
        minimize_btn.innerHTML = this.get_icon('minimize');
        minimize_btn.onclick = (e) => {
            e.stopPropagation();
            win.toggle_minimized();
            this.toggle_windows_list();
        };

        const close_btn = document.createElement('div');
        close_btn.className = 'dock-window-item-action';
        close_btn.innerHTML = this.get_icon('close');
        close_btn.onclick = (e) => {
            e.stopPropagation();
            this.client.send_close_window(win);
            this.toggle_windows_list();
        };

        actions.appendChild(minimize_btn);
        actions.appendChild(close_btn);

        // Click sur l'item
        item.onclick = () => {
            if (win.minimized) {
                win.toggle_minimized();
            }
            this.client.set_focus(win);
            this.close_all_menus();
        };

        item.appendChild(icon);
        item.appendChild(info);
        item.appendChild(actions);

        return item;
    }

    // Gestion des fenêtres
    add_window(win) {
        const wid = win.wid;
        if (this.window_items[wid]) return;

        const tray = document.getElementById('dock_tray');
        const window_item = this.create_dock_item({
            id: `window_${wid}`,
            tooltip: win.title || 'Window',
            icon: `<img src="${win.icon || 'favicon.png'}" alt="">`,
            color: null
        });

        window_item.classList.add('active');

        window_item.onclick = (e) => {
            e.stopPropagation();
            if (win.minimized) {
                win.toggle_minimized();
            }
            this.client.set_focus(win);
        };

        // Animation bounce pour nouvelle fenêtre
        window_item.classList.add('bouncing');
        setTimeout(() => window_item.classList.remove('bouncing'), 1200);

        tray.appendChild(window_item);
        this.window_items[wid] = { element: window_item, win: win };

        this.update_windows_count();
    }

    remove_window(wid) {
        if (this.window_items[wid]) {
            this.window_items[wid].element.remove();
            delete this.window_items[wid];
            this.update_windows_count();
        }
    }

    update_window_icon(wid, icon_src) {
        if (this.window_items[wid]) {
            const img = this.window_items[wid].element.querySelector('img');
            if (img) img.src = icon_src;
        }
    }

    update_window_title(wid, title) {
        if (this.window_items[wid]) {
            const tooltip = this.window_items[wid].element.querySelector('.dock-tooltip');
            if (tooltip) tooltip.textContent = title;
        }
    }

    update_windows_count() {
        const count = Object.keys(this.window_items).length;
        const badge = document.getElementById('dock_windows_badge');
        
        if (count > 0) {
            badge.textContent = count;
            badge.style.display = 'flex';
        } else {
            badge.style.display = 'none';
        }
    }

    // Gestion du tray
    add_tray(wid, metadata) {
        const tray = document.getElementById('dock_tray');
        const tray_item = this.create_dock_item({
            id: `tray_${wid}`,
            tooltip: metadata.title || 'Tray',
            icon: `<img src="favicon.png" alt="">`,
            color: null
        });

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
            if (img) img.src = icon_src;
        }
    }

    // Actions
    toggle_fullscreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen();
            this.dock_items['fullscreen'].querySelector('.dock-icon').innerHTML = this.get_icon('fullscreen_exit');
        } else {
            document.exitFullscreen();
            this.dock_items['fullscreen'].querySelector('.dock-icon').innerHTML = this.get_icon('fullscreen');
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
        if (typeof client !== 'undefined' && client.audio_enabled) {
            if (client.audio_state === 'playing') {
                client.close_audio();
            } else {
                client._audio_start_receiving();
            }
        }
    }

    show_about() {
        this.close_all_menus();
        const about = document.getElementById('about');
        if (about) {
            about.style.display = 'block';
        }
    }

    show_session_info() {
        this.close_all_menus();
        const info = document.getElementById('sessioninfo');
        if (info) {
            info.style.display = 'block';
            if (typeof client !== 'undefined') {
                client.start_info_timer();
            }
        }
    }

    show_bug_report() {
        this.close_all_menus();
        const bug = document.getElementById('bugreport');
        if (bug) {
            bug.style.display = 'block';
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

    // Icônes SVG (style minimaliste shadcn/ui)
    get_icon(name) {
        const icons = {
            menu: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/></svg>`,
            
            windows: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M9 3v18"/></svg>`,
            
            fullscreen: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3H5a2 2 0 0 0-2 2v3"/><path d="M21 8V5a2 2 0 0 0-2-2h-3"/><path d="M3 16v3a2 2 0 0 0 2 2h3"/><path d="M16 21h3a2 2 0 0 0 2-2v-3"/></svg>`,
            
            fullscreen_exit: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3v3a2 2 0 0 1-2 2H3"/><path d="M21 8h-3a2 2 0 0 1-2-2V3"/><path d="M3 16h3a2 2 0 0 1 2 2v3"/><path d="M16 21v-3a2 2 0 0 1 2-2h3"/></svg>`,
            
            keyboard: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 8h.01"/><path d="M12 12h.01"/><path d="M14 8h.01"/><path d="M16 12h.01"/><path d="M18 8h.01"/><path d="M6 8h.01"/><path d="M7 16h10"/><path d="M8 12h.01"/><rect width="20" height="16" x="2" y="4" rx="2"/></svg>`,
            
            clipboard: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/></svg>`,
            
            audio: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg>`,
            
            info: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>`,
            
            chart: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/></svg>`,
            
            bug: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m8 2 1.88 1.88"/><path d="M14.12 3.88 16 2"/><path d="M9 7.13v-1a3.003 3.003 0 1 1 6 0v1"/><path d="M12 20c-3.3 0-6-2.7-6-6v-3a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v3c0 3.3-2.7 6-6 6"/><path d="M12 20v-9"/><path d="M6.53 9C4.6 8.8 3 7.1 3 5"/><path d="M6 13H2"/><path d="M3 21c0-2.1 1.7-3.9 3.8-4"/><path d="M20.97 5c0 2.1-1.6 3.8-3.5 4"/><path d="M22 13h-4"/><path d="M17.2 17c2.1.1 3.8 1.9 3.8 4"/></svg>`,
            
            refresh: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/><path d="M16 16h5v5"/></svg>`,
            
            logout: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" x2="9" y1="12" y2="12"/></svg>`,
            
            minimize: `<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3v3a2 2 0 0 1-2 2H3"/><path d="M21 8h-3a2 2 0 0 1-2-2V3"/><path d="M3 16h3a2 2 0 0 1 2 2v3"/><path d="M16 21v-3a2 2 0 0 1 2-2h3"/></svg>`,
            
            close: `<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>`
        };
        
        return icons[name] || icons.windows;
    }
}

// Export pour utilisation
if (typeof module !== 'undefined' && module.exports) {
    module.exports = XpraDock;
}
```

## 3. Modifications dans index.html

**Fichier:** `html5/index.html`

### A. Ajouter le CSS du Dock (après la ligne ~18)

```html
<!-- Dock macOS CSS -->
<link rel="stylesheet" href="css/dock.css" />
```

### B. Ajouter le JS du Dock (après la ligne ~44, avant Client.js)

```html
<!-- Dock macOS JS -->
<script type="text/javascript" src="js/Dock.js"></script>
```

### C. Modifier la fonction init_float_menu (vers ligne ~625)

Remplacer la fonction complète par:

```javascript
function init_float_menu() {
    const floating_menu = getboolparam("floating_menu", true);
    const toolbar_position = getstrparam("toolbar_position");
    
    // MASQUER L'ANCIEN MENU FLOTTANT
    $("#float_menu").hide();
    $("#float_menu_button").hide();
    
    // INITIALISER LE NOUVEAU DOCK MACOS
    if (floating_menu && typeof XpraDock !== 'undefined') {
        console.log("Initializing macOS Dock...");
        window.xpra_dock = new XpraDock(client);
        client.toolbar_position = "dock"; // Nouveau mode
    }
    
    // Ne pas exécuter le reste du code original
    return;
}
```

## 4. Modifications dans Client.js

**Fichier:** `html5/js/Client.js`

### A. Dans `_process_new_window` (ligne ~2880)

Ajouter après `this._new_window_common(packet, false);`:

```javascript
_process_new_window(packet) {
    this._new_window_common(packet, false);
    
    // AJOUTER AU DOCK MACOS
    if (window.xpra_dock) {
        const wid = packet[1];
        const win = this.id_to_window[wid];
        if (win && !win.tray && !win.override_redirect && !this.server_is_desktop) {
            setTimeout(() => {
                window.xpra_dock.add_window(win);
            }, 100);
        }
    }
}
```

### B. Dans `_process_lost_window` (ligne ~2950)

Ajouter au début de la fonction:

```javascript
_process_lost_window(packet) {
    const wid = packet[1];
    
    // RETIRER DU DOCK MACOS
    if (window.xpra_dock) {
        window.xpra_dock.remove_window(wid);
    }
    
    const win = this.id_to_window[wid];
    // ... reste du code original ...
}
```

### C. Dans `_process_new_tray` (ligne ~3020)

Ajouter à la fin de la fonction:

```javascript
_process_new_tray(packet) {
    const wid = packet[1];
    const metadata = packet[4];
    
    // ... code original pour créer le tray ...
    
    // AJOUTER AU DOCK MACOS
    if (window.xpra_dock) {
        window.xpra_dock.add_tray(wid, metadata);
    }
}
```

### D. Dans `_process_window_icon` (ligne ~3200)

Ajouter après l'update de l'icône:

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
        
        // METTRE À JOUR L'ICÔNE DANS LE DOCK MACOS
        if (window.xpra_dock) {
            if (win.tray) {
                window.xpra_dock.update_tray_icon(wid, source);
            } else {
                window.xpra_dock.update_window_icon(wid, source);
            }
        }
        
        // ... reste du code original ...
    }
}
```

### E. Dans `_process_window_metadata` (ligne ~2900)

Ajouter pour mettre à jour les titres:

```javascript
_process_window_metadata(packet) {
    const wid = packet[1];
    const metadata = packet[2];
    const win = this.id_to_window[wid];
    
    if (win) {
        win.update_metadata(metadata);
        
        // METTRE À JOUR LE TITRE DANS LE DOCK
        if (window.xpra_dock && metadata.title) {
            window.xpra_dock.update_window_title(wid, metadata.title);
        }
    }
}
```

## 5. Masquer les éléments de l'ancien menu (optionnel)

**Fichier:** `html5/css/client.css`

Ajouter à la fin du fichier:

```css
/* Masquer l'ancien menu quand le dock est activé */
#float_menu,
#float_menu_button {
    display: none !important;
}

/* Ajuster l'espace en bas pour le dock */
#screen {
    padding-bottom: 80px;
}
```

## 6. Instructions d'installation complètes

### Étape 1: Créer les fichiers
```bash
cd html5
touch css/dock.css
touch js/Dock.js
```

### Étape 2: Copier le contenu
Copier le contenu de `dock.css` et `Dock.js` depuis ce patch dans les fichiers créés.

### Étape 3: Modifier index.html
- Ajouter les balises `<link>` et `<script>` comme indiqué
- Modifier la fonction `init_float_menu()`

### Étape 4: Modifier Client.js
Appliquer les modifications dans les 5 fonctions indiquées:
- `_process_new_window`
- `_process_lost_window`
- `_process_new_tray`
- `_process_window_icon`
- `_process_window_metadata`

### Étape 5: Tester
```bash
# Rafraîchir la page Xpra
# Le dock devrait apparaître en bas de l'écran
# L'ancien menu devrait être masqué
```

## 7. Fonctionnalités du Dock shadcn/ui

✅ **Effet de magnification** au survol (comme macOS)
✅ **Magnification des icônes adjacentes**
✅ **Animations fluides** (bouncing, transitions)
✅ **Mode sombre automatique** (détection système)
✅ **Badges de notification** pour le compteur de fenêtres
✅ **Menus contextuels** avec backdrop-filter
✅ **Liste des fenêtres** avec actions (minimize, close)
✅ **Tooltips élégants**
✅ **Responsive design**
✅ **Support des tray icons**
✅ **Icônes SVG minimalistes** (style shadcn/ui)

## 8. Configuration

Dans `default-settings.txt`:

```ini
# Dock macOS settings
floating_menu=true
toolbar_position=dock
```

## 9. Désactivation

Pour revenir à l'ancien menu:

Dans `init_float_menu()`, commenter:
```javascript
// $("#float_menu").hide();
// window.xpra_dock = new XpraDock(client);
// return;
```

## 10. Personnalisation

### Changer la taille des icônes:
```css
:root {
    --dock-item-size: 56px; /* Augmenter ou diminuer */
}
```

### Changer l'effet de magnification:
```css
:root {
    --dock-magnify-scale: 1.7; /* Plus grand = plus de zoom */
}
```

### Activer l'auto-hide:
Dans `Dock.js`, décommenter dans `setup_event_listeners()`:
```javascript
hide_timeout = setTimeout(() => {
    this.dock_element.classList.add('hidden');
}, 3000);
```

## 11. Dépannage

**Le dock n'apparaît pas:**
- Vérifier la console (F12)
- Vérifier que `dock.css` et `Dock.js` sont chargés
- Vérifier que `window.xpra_dock` existe

**L'ancien menu est encore visible:**
- Vérifier que `$("#float_menu").hide()` est appelé
- Ajouter `!important` dans le CSS si nécessaire
- Vider le cache du navigateur

**Les icônes ne s'affichent pas:**
- Vérifier les chemins des images
- Vérifier que les SVG sont correctement encodés
- Ouvrir la console pour voir les erreurs

**L'effet de magnification ne fonctionne pas:**
- Vérifier que les CSS variables sont définies
- Tester dans un navigateur moderne (Chrome, Firefox, Safari)
- Vérifier que le CSS n'est pas écrasé

---

Ce patch crée un dock macOS moderne inspiré de shadcn/ui avec toutes les fonctionnalités nécessaires pour remplacer l'ancien menu flottant. 🚀