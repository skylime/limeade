"use strict"

var START = {
    rfb_state: 'loaded',
    settingsOpen: false,
    connSettingsOpen: false,
    clipboardOpen: false,
    keyboardVisible: false,
    
    load: function () {
        var html = '';
        var i, sheet, sheets, llevels;
        
        // Populate the controls if defaults are provided
        START.initSetting('host', HOST);
        START.initSetting('port', PORT);
        START.initSetting('password', '');
        START.initSetting('encrypt', false);
        START.initSetting('true_color', true);
        START.initSetting('cursor', false);
        START.initSetting('shared', true);
        START.initSetting('view_only', false);
        START.initSetting('connectTimeout', 2);
        START.initSetting('path', 'websockify?instance_id=' + INSTANCE_ID + '&token=' + TOKEN);
        START.initSetting('repeaterID', '');
        
        START.rfb = RFB({
            'target': $D('noVNC_canvas'),
            'onUpdateState': START.updateState,
            'onClipboard': START.clipReceive
        });
        START.updateVisualState();
        
        // Show mouse selector buttons on touch screen devices
        if ('ontouchstart' in document.documentElement) {
            // Show mobile buttons
            $D('noVNC_mobile_buttons').style.display = "inline-block";
            START.setMouseButton();
            // Remove the address bar
            setTimeout(function() { window.scrollTo(0, 1); }, 100);
            START.forceSetting('clip', true);
            $D('noVNC_clip').disabled = true;
        } else {
            START.initSetting('clip', false);
        }
        
        //iOS Safari does not support CSS position:fixed.
        //This detects iOS devices and enables javascript workaround.
        if ((navigator.userAgent.match(/iPhone/i)) ||
            (navigator.userAgent.match(/iPod/i)) ||
            (navigator.userAgent.match(/iPad/i))) {
            //START.setOnscroll();
            //START.setResize();
        }
        
        $D('noVNC_host').focus();
        
        START.setViewClip();
        Util.addEvent(window, 'resize', START.setViewClip);
        
        Util.addEvent(window, 'beforeunload', function () {
            if (START.rfb_state === 'normal') {
                return "You are currently connected.";
            }
        });
        
        // Start the engine
        START.connect();
    },
    // Read form control compatible setting from cookie
    getSetting: function(name) {
        var val, ctrl = $D('noVNC_' + name);
        val = WebUtil.readCookie(name);
        if (ctrl.type === 'checkbox') {
            if (val.toLowerCase() in {'0':1, 'no':1, 'false':1}) {
                val = false;
            } else {
                val = true;
            }
        }
        return val;
    },
    // Update cookie and form control setting. If value is not set, then
    // updates from control to current cookie setting.
    updateSetting: function(name, value) {
        var i, ctrl = $D('noVNC_' + name);
        // Save the cookie for this session
        if (typeof value !== 'undefined') {
            WebUtil.createCookie(name, value);
        }
        // Update the settings control
        value = START.getSetting(name);
        if (ctrl.type === 'checkbox') {
            ctrl.checked = value;
        } else if (typeof ctrl.options !== 'undefined') {
            for (i = 0; i < ctrl.options.length; i += 1) {
                if (ctrl.options[i].value === value) {
                    ctrl.selectedIndex = i;
                    break;
                }
            }
        } else {
            // Weird IE9 error leads to 'null' appearring in textboxes instead of ''
            if (value === null) {
                value = "";
            }
            ctrl.value = value;
        }
    },
    // Save control setting to cookie
    saveSetting: function(name) {
        var val, ctrl = $D('noVNC_' + name);
        if (ctrl.type === 'checkbox') {
            val = ctrl.checked;
        } else if (typeof ctrl.options !== 'undefined') {
            val = ctrl.options[ctrl.selectedIndex].value;
        } else {
            val = ctrl.value;
        }
        WebUtil.createCookie(name, val);
        //Util.Debug("Setting saved '" + name + "=" + val + "'");
        return val;
    },
    // Initial page load read/initialization of settings
    initSetting: function(name, defVal) {
        var val;
        // Check Query string followed by cookie
        val = WebUtil.getQueryVar(name);
        if (val === null) {
            val = WebUtil.readCookie(name, defVal);
        }
        START.updateSetting(name, val);
        //Util.Debug("Setting '" + name + "' initialized to '" + val + "'");
        return val;
    },
    // Force a setting to be a certain value
    forceSetting: function(name, val) {
        START.updateSetting(name, val);
        return val;
    },
    // Show the clipboard panel
    toggleClipboardPanel: function() {
        //Close settings if open
        if (START.settingsOpen === true) {
            START.settingsApply();
            START.closeSettingsMenu();
        }
        //Close connection settings if open
        if (START.connSettingsOpen === true) {
            START.toggleConnectPanel();
        }
        //Toggle Clipboard Panel
        if (START.clipboardOpen === true) {
            $D('noVNC_clipboard').style.display = "none";
            $D('clipboardButton').className = "noVNC_status_button";
            START.clipboardOpen = false;
        } else {
            $D('noVNC_clipboard').style.display = "block";
            $D('clipboardButton').className = "noVNC_status_button_selected";
            START.clipboardOpen = true;
        }
    },
    // Show the connection settings panel/menu
    toggleConnectPanel: function() {
        //Close connection settings if open
        if (START.settingsOpen === true) {
            START.settingsApply();
            START.closeSettingsMenu();
            $D('connectButton').className = "noVNC_status_button";
        }
        if (START.clipboardOpen === true) {
            START.toggleClipboardPanel();
        }
        //Toggle Connection Panel
        if (START.connSettingsOpen === true) {
            $D('noVNC_controls').style.display = "none";
            $D('connectButton').className = "noVNC_status_button";
            START.connSettingsOpen = false;
        } else {
            $D('noVNC_controls').style.display = "block";
            $D('connectButton').className = "noVNC_status_button_selected";
            START.connSettingsOpen = true;
            $D('noVNC_host').focus();
        }
    },
    // Toggle the settings menu:
    // On open, settings are refreshed from saved cookies
    // On close, settings are applied
    toggleSettingsPanel: function() {
        if (START.settingsOpen) {
            START.settingsApply();
            START.closeSettingsMenu();
        } else {
            START.updateSetting('encrypt');
            START.updateSetting('true_color');
            if (START.rfb.get_display().get_cursor_uri()) {
                START.updateSetting('cursor');
            } else {
                START.updateSetting('cursor', false);
                $D('noVNC_cursor').disabled = true;
            }
            START.updateSetting('clip');
            START.updateSetting('shared');
            START.updateSetting('view_only');
            START.updateSetting('connectTimeout');
            START.updateSetting('path');
            START.updateSetting('repeaterID');
            START.openSettingsMenu();
        }
    },
    // Open menu
    openSettingsMenu: function() {
        if (START.clipboardOpen === true) {
            START.toggleClipboardPanel();
        }
        // Close connection settings if open
        if (START.connSettingsOpen === true) {
            START.toggleConnectPanel();
        }
        $D('noVNC_settings').style.display = "block";
        $D('settingsButton').className = "noVNC_status_button_selected";
        START.settingsOpen = true;
    },
    // Close menu (without applying settings)
    closeSettingsMenu: function() {
        $D('noVNC_settings').style.display = "none";
        $D('settingsButton').className = "noVNC_status_button";
        START.settingsOpen = false;
    },
    // Save/apply settings when 'Apply' button is pressed
    settingsApply: function() {
        //Util.Debug(">> settingsApply");
        START.saveSetting('encrypt');
        START.saveSetting('true_color');
        if (START.rfb.get_display().get_cursor_uri()) {
            START.saveSetting('cursor');
        }
        START.saveSetting('clip');
        START.saveSetting('shared');
        START.saveSetting('view_only');
        START.saveSetting('connectTimeout');
        START.saveSetting('path');
        START.saveSetting('repeaterID');
        
        START.setViewClip();
        START.setViewDrag(START.rfb.get_viewportDrag());
        //Util.Debug("<< settingsApply");
    },
    setPassword: function() {
        START.rfb.sendPassword($D('noVNC_password').value);
        //Reset connect button.
        $D('noVNC_connect_button').value = "Connect";
        $D('noVNC_connect_button').onclick = START.Connect;
        //Hide connection panel.
        START.toggleConnectPanel();
        return false;
    },
    sendCtrlAltDel: function() {
        START.rfb.sendCtrlAltDel();
    },
    setMouseButton: function(num) {
        var b, blist = [0, 1,2,4], button;
        
        if (typeof num === 'undefined') {
            // Disable mouse buttons
            num = -1;
        }
        if (START.rfb) {
            START.rfb.get_mouse().set_touchButton(num);
        }
        
        for (b = 0; b < blist.length; b++) {
            button = $D('noVNC_mouse_button' + blist[b]);
            if (blist[b] === num) {
                button.style.display = "";
            } else {
                button.style.display = "none";
                /*
                button.style.backgroundColor = "black";
                button.style.color = "lightgray";
                button.style.backgroundColor = "";
                button.style.color = "";
                */
            }
        }
    },
    updateState: function(rfb, state, oldstate, msg) {
        var s, sb, c, d, cad, vd, klass;
        START.rfb_state = state;
        s = $D('noVNC_status');
        sb = $D('noVNC_status_bar');
        switch (state) {
            case 'failed':
            case 'fatal':
                klass = "noVNC_status_error";
                break;
            case 'normal':
                klass = "noVNC_status_normal";
                break;
            case 'disconnected':
                $D('noVNC_logo').style.display = "block";
                // Fall through
            case 'loaded':
                klass = "noVNC_status_normal";
                break;
            case 'password':
                START.toggleConnectPanel();
                $D('noVNC_connect_button').value = "Send Password";
                $D('noVNC_connect_button').onclick = START.setPassword;
                $D('noVNC_password').focus();
                klass = "noVNC_status_warn";
                break;
            default:
                klass = "noVNC_status_warn";
                break;
        }
        if (typeof(msg) !== 'undefined') {
            s.setAttribute("class", klass);
            sb.setAttribute("class", klass);
            s.innerHTML = msg;
        }
        START.updateVisualState();
    },
    // Disable/enable controls depending on connection state
    updateVisualState: function() {
        var connected = START.rfb_state === 'normal' ? true : false;
        
        //Util.Debug(">> updateVisualState");
        $D('noVNC_encrypt').disabled = connected;
        $D('noVNC_true_color').disabled = connected;
        if (START.rfb && START.rfb.get_display() && START.rfb.get_display().get_cursor_uri()) {
            $D('noVNC_cursor').disabled = connected;
        } else {
            START.updateSetting('cursor', false);
            $D('noVNC_cursor').disabled = true;
        }
        $D('noVNC_shared').disabled = connected;
        $D('noVNC_view_only').disabled = connected;
        $D('noVNC_connectTimeout').disabled = connected;
        $D('noVNC_path').disabled = connected;
        $D('noVNC_repeaterID').disabled = connected;
        
        if (connected) {
            START.setViewClip();
            START.setMouseButton(1);
            $D('clipboardButton').style.display = "inline";
            $D('showKeyboard').style.display = "inline";
            $D('sendCtrlAltDelButton').style.display = "inline";
        } else {
            START.setMouseButton();
            $D('clipboardButton').style.display = "none";
            $D('showKeyboard').style.display = "none";
            $D('sendCtrlAltDelButton').style.display = "none";
        }
        // State change disables viewport dragging.
        // It is enabled (toggled) by direct click on the button
        START.setViewDrag(false);
        
        switch (START.rfb_state) {
            case 'fatal':
            case 'failed':
            case 'loaded':
            case 'disconnected':
                $D('connectButton').style.display = "";
                $D('disconnectButton').style.display = "none";
                break;
            default:
                $D('connectButton').style.display = "none";
                $D('disconnectButton').style.display = "";
            break;
        }
        //Util.Debug("<< updateVisualState");
    },
    clipReceive: function(rfb, text) {
        Util.Debug(">> START.clipReceive: " + text.substr(0,40) + "...");
        $D('noVNC_clipboard_text').value = text;
        Util.Debug("<< START.clipReceive");
    },
    connect: function() {
        var host, port, password, path;
        
        START.closeSettingsMenu();
        //START.toggleConnectPanel();
        
        host = HOST;
        port = PORT;
        password = $D('noVNC_password').value;
        path = 'websockify?instance_id=' + INSTANCE_ID + '&token=' + TOKEN;
        
        if ((!host) || (!port)) {
            throw("Must set host and port");
        }
        
        START.rfb.set_encrypt(START.getSetting('encrypt'));
        START.rfb.set_true_color(START.getSetting('true_color'));
        START.rfb.set_local_cursor(START.getSetting('cursor'));
        START.rfb.set_shared(START.getSetting('shared'));
        START.rfb.set_view_only(START.getSetting('view_only'));
        START.rfb.set_connectTimeout(START.getSetting('connectTimeout'));
        START.rfb.set_repeaterID(START.getSetting('repeaterID'));
        
        START.rfb.connect(host, port, password, path);
        
        //Close dialog.
        setTimeout(START.setBarPosition, 100);
    },
    disconnect: function() {
        START.closeSettingsMenu();
        START.rfb.disconnect();
        
        START.connSettingsOpen = false;
        //START.toggleConnectPanel();
    },
    displayBlur: function() {
        START.rfb.get_keyboard().set_focused(false);
        START.rfb.get_mouse().set_focused(false);
    },
    displayFocus: function() {
        START.rfb.get_keyboard().set_focused(true);
        START.rfb.get_mouse().set_focused(true);
    },
    clipClear: function() {
        $D('noVNC_clipboard_text').value = "";
        START.rfb.clipboardPasteFrom("");
    },
    clipSend: function() {
        var text = $D('noVNC_clipboard_text').value;
        Util.Debug(">> START.clipSend: " + text.substr(0,40) + "...");
        START.rfb.clipboardPasteFrom(text);
        Util.Debug("<< START.clipSend");
    },
    // Enable/disable and configure viewport clipping
    setViewClip: function(clip) {
        var display, cur_clip, pos, new_w, new_h;
        
        if (START.rfb) {
            display = START.rfb.get_display();
        } else {
            return;
        }
        
        cur_clip = display.get_viewport();
        
        if (typeof(clip) !== 'boolean') {
            // Use current setting
            clip = START.getSetting('clip');
        }
        
        if (clip && !cur_clip) {
            // Turn clipping on
            START.updateSetting('clip', true);
        } else if (!clip && cur_clip) {
            // Turn clipping off
            START.updateSetting('clip', false);
            display.set_viewport(false);
            $D('noVNC_canvas').style.position = 'static';
            display.viewportChange();
        }
        
        if (START.getSetting('clip')) {
            // If clipping, update clipping settings
            $D('noVNC_canvas').style.position = 'absolute';
            pos = Util.getPosition($D('noVNC_canvas'));
            new_w = window.innerWidth - pos.x;
            new_h = window.innerHeight - pos.y;
            display.set_viewport(true);
            display.viewportChange(0, 0, new_w, new_h);
        }
    },
    // Toggle/set/unset the viewport drag/move button
    setViewDrag: function(drag) {
        var vmb = $D('noVNC_view_drag_button');
        if (!START.rfb) { return; }
        
        if (START.rfb_state === 'normal' && START.rfb.get_display().get_viewport()) {
            vmb.style.display = "inline";
        } else {
            vmb.style.display = "none";
        }
        
        if (typeof(drag) === "undefined") {
            // If not specified, then toggle
            drag = !START.rfb.get_viewportDrag();
        }
        if (drag) {
            vmb.className = "noVNC_status_button_selected";
            START.rfb.set_viewportDrag(true);
        } else {
            vmb.className = "noVNC_status_button";
            START.rfb.set_viewportDrag(false);
        }
    },
    // On touch devices, show the OS keyboard
    showKeyboard: function() {
        if(START.keyboardVisible === false) {
            $D('keyboardinput').focus();
            START.keyboardVisible = true;
            $D('showKeyboard').className = "noVNC_status_button_selected";
        } else if(START.keyboardVisible === true) {
            $D('keyboardinput').blur();
            $D('showKeyboard').className = "noVNC_status_button";
            START.keyboardVisible = false;
        }
    },
    keyInputBlur: function() {
        $D('showKeyboard').className = "noVNC_status_button";
        //Weird bug in iOS if you change keyboardVisible
        //here it does not actually occur so next time
        //you click keyboard icon it doesnt work.
        setTimeout(function() { START.setKeyboard(); },100);
    },
    setKeyboard: function() {
        START.keyboardVisible = false;
    },
    // iOS < Version 5 does not support position fixed. Javascript workaround:
    setOnscroll: function() {
        window.onscroll = function() {
            START.setBarPosition();
        };
    },
    setResize: function () {
        window.onResize = function() {
            START.setBarPosition();
        };
    },
    //Helper to add options to dropdown.
    addOption: function(selectbox,text,value ) {
        var optn = document.createElement("OPTION");
        optn.text = text;
        optn.value = value;
        selectbox.options.add(optn);
    },
    setBarPosition: function() {
        // don't do anything yet
    }
};
