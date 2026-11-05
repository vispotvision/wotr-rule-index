pragma ComponentBehavior: Bound

import QtQuick
import Ryoku.PluginKit
import Ryoku.PluginKit.Singletons

// The bar panel: WOTR / MCP / QUILL / SERVER on four tabs, the tab picked by the
// service (a mark click, a keybind through IPC, or the tab row here). The host
// owns the surface; this root only reports its size.
Item {
    id: root

    property var pluginApi
    property string density: "full"
    property real s: 1
    property real widthBudget: 460
    property bool active: false

    readonly property var svc: pluginApi ? pluginApi.mainInstance : null
    readonly property var wotr: svc ? svc.wotr : null
    readonly property var mcp: svc ? svc.mcp : null
    readonly property var quill: svc ? svc.quill : null
    readonly property var mcs: svc ? svc.mcs : null
    readonly property string tab: svc ? svc.tab : "wotr"
    readonly property real w: widthBudget > 0 ? widthBudget : 460

    implicitWidth: w
    implicitHeight: col.implicitHeight

    onActiveChanged: if (active && svc) svc.refreshAll()

    // ── pieces ───────────────────────────────────────────────────────────────
    component Hero: Item {
        id: h
        property string icon: ""
        property string title: ""
        property string caption: ""
        property string number: ""
        property string numberLabel: ""
        property bool urgent: false
        width: parent ? parent.width : 0
        implicitHeight: Math.max(hg.implicitHeight, hl.implicitHeight, hn.implicitHeight)
        Text { id: hg; anchors.left: parent.left; anchors.verticalCenter: parent.verticalCenter; text: h.icon; font.family: "Material Symbols Rounded"; font.pixelSize: 34 * root.s; font.variableAxes: ({ "FILL": 1, "opsz": 40 }); color: Theme.accent; renderType: Text.QtRendering }
        Column {
            id: hl
            anchors.left: hg.right; anchors.leftMargin: 12 * root.s; anchors.right: hn.left; anchors.rightMargin: 12 * root.s; anchors.verticalCenter: parent.verticalCenter
            spacing: 2
            Text { width: parent.width; text: h.title; color: Theme.cream; font.family: Theme.display; font.pixelSize: 17 * root.s; elide: Text.ElideRight }
            Text { width: parent.width; text: h.caption; color: Theme.faint; font.family: Theme.mono; font.pixelSize: 9 * root.s; font.letterSpacing: 1.2 * root.s; elide: Text.ElideRight }
        }
        Column {
            id: hn
            anchors.right: parent.right; anchors.verticalCenter: parent.verticalCenter
            Text { anchors.right: parent.right; text: h.number; color: h.urgent ? Theme.verm : Theme.cream; font.family: Theme.display; font.pixelSize: 26 * root.s }
            Text { anchors.right: parent.right; text: h.numberLabel; color: Theme.faint; font.family: Theme.mono; font.pixelSize: 8 * root.s; font.letterSpacing: 1.6 * root.s }
        }
    }

    component Btn: Rectangle {
        id: b
        property string icon: ""
        property string label: ""
        property bool enabled: true
        signal clicked()
        height: 30 * root.s
        radius: Theme.radius
        color: bh.hovered && b.enabled ? Theme.sheen : "transparent"
        border.width: 1; border.color: b.enabled ? Theme.lineStrong : Theme.border
        opacity: b.enabled ? 1 : 0.5
        Row {
            anchors.centerIn: parent; spacing: 5 * root.s
            Text { anchors.verticalCenter: parent.verticalCenter; text: b.icon; font.family: "Material Symbols Rounded"; font.pixelSize: 15 * root.s; color: Theme.cream; renderType: Text.QtRendering }
            Text { anchors.verticalCenter: parent.verticalCenter; text: b.label; color: Theme.cream; font.family: Theme.mono; font.pixelSize: 9.5 * root.s; font.weight: Font.DemiBold; font.letterSpacing: 1 * root.s }
        }
        HoverHandler { id: bh; cursorShape: b.enabled ? Qt.PointingHandCursor : Qt.ArrowCursor }
        TapHandler { enabled: b.enabled; onTapped: b.clicked() }
    }

    // key/value line; clickable when it has an onClicked
    component KV: Item {
        id: kv
        property string label: ""
        property string value: ""
        property bool link: false
        signal clicked()
        width: parent ? parent.width : 0
        height: Math.max(17 * root.s, vt.implicitHeight)
        Text { id: kt; anchors.left: parent.left; anchors.verticalCenter: parent.verticalCenter; width: 96 * root.s; text: kv.label; color: Theme.faint; font.family: Theme.mono; font.pixelSize: 9 * root.s; font.letterSpacing: 1.2 * root.s; font.capitalization: Font.AllUppercase; elide: Text.ElideRight }
        Text { id: vt; anchors.left: kt.right; anchors.leftMargin: 6 * root.s; anchors.right: parent.right; anchors.verticalCenter: parent.verticalCenter; text: kv.value; color: kh.hovered && kv.link ? Theme.accent : Theme.cream; font.family: Theme.mono; font.pixelSize: 10.5 * root.s; elide: Text.ElideMiddle; horizontalAlignment: Text.AlignRight }
        HoverHandler { id: kh; cursorShape: kv.link ? Qt.PointingHandCursor : Qt.ArrowCursor }
        TapHandler { enabled: kv.link; onTapped: kv.clicked() }
    }

    // status line: dot, label, detail, one action chip
    component SRow: Item {
        id: sr
        property color dot: Theme.dim
        property string label: ""
        property string detail: ""
        property string action: ""
        signal triggered()
        width: parent ? parent.width : 0
        height: 20 * root.s
        Rectangle { id: d; width: 7 * root.s; height: width; radius: width / 2; color: sr.dot; anchors.left: parent.left; anchors.verticalCenter: parent.verticalCenter }
        Text { id: lt; anchors.left: d.right; anchors.leftMargin: 9 * root.s; anchors.verticalCenter: parent.verticalCenter; text: sr.label; color: Theme.cream; font.family: Theme.font; font.pixelSize: 11 * root.s }
        Text { anchors.left: lt.right; anchors.leftMargin: 8 * root.s; anchors.right: chip.left; anchors.rightMargin: 8 * root.s; anchors.verticalCenter: parent.verticalCenter; text: sr.detail; color: Theme.faint; font.family: Theme.mono; font.pixelSize: 9 * root.s; elide: Text.ElideRight }
        Rectangle {
            id: chip; visible: sr.action !== ""; anchors.right: parent.right; anchors.verticalCenter: parent.verticalCenter
            width: sr.action !== "" ? ct.implicitWidth + 12 * root.s : 0; height: 15 * root.s; radius: 0
            color: ch.hovered ? Theme.sheen : "transparent"; border.width: 1; border.color: Theme.lineStrong
            Text { id: ct; anchors.centerIn: parent; text: sr.action; color: Theme.cream; font.family: Theme.mono; font.pixelSize: 8 * root.s; font.weight: Font.DemiBold; font.letterSpacing: 1.2 * root.s }
            HoverHandler { id: ch; cursorShape: Qt.PointingHandCursor }
            TapHandler { onTapped: sr.triggered() }
        }
    }

    // a small action chip
    component Chip: Rectangle {
        id: cp
        property string text: ""
        property bool hot: false
        signal tapped()
        width: cpt.implicitWidth + 12 * root.s; height: 15 * root.s; radius: 0
        color: cph.hovered ? Theme.sheen : "transparent"; border.width: 1; border.color: cp.hot ? Theme.verm : Theme.lineStrong
        Text { id: cpt; anchors.centerIn: parent; text: cp.text; color: cp.hot ? Theme.verm : Theme.cream; font.family: Theme.mono; font.pixelSize: 8 * root.s; font.weight: Font.DemiBold; font.letterSpacing: 1.2 * root.s }
        HoverHandler { id: cph; cursorShape: Qt.PointingHandCursor }
        TapHandler { onTapped: cp.tapped() }
    }

    // one MCP key: its state, what it can reach, COPY for its link and an on/off that asks once
    // before cutting a key off (disabling ends its open sessions)
    component KeyRow: Item {
        id: kr
        required property var modelData
        property bool arming: false
        width: parent ? parent.width : 0
        height: 34 * root.s
        readonly property string state_: !modelData.enabled ? "disabled" : modelData.online ? "online" : modelData.sessions > 0 ? "idle" : "offline"
        Timer { id: disarm; interval: 3000; onTriggered: kr.arming = false }
        Rectangle {
            id: kd; width: 7 * root.s; height: width; radius: width / 2; anchors.left: parent.left; anchors.top: parent.top; anchors.topMargin: 5 * root.s
            color: kr.state_ === "online" ? Theme.accent : kr.state_ === "disabled" ? Theme.verm : kr.state_ === "idle" ? Theme.cream : Theme.dim
        }
        Column {
            anchors.left: kd.right; anchors.leftMargin: 9 * root.s; anchors.right: kc.left; anchors.rightMargin: 8 * root.s; anchors.top: parent.top
            spacing: 2
            Text { width: parent.width; text: kr.modelData.name; color: Theme.cream; font.family: Theme.font; font.pixelSize: 11 * root.s; elide: Text.ElideRight }
            Text {
                width: parent.width; elide: Text.ElideRight; color: Theme.faint; font.family: Theme.mono; font.pixelSize: 9 * root.s
                text: kr.state_ + (kr.modelData.sessions > 0 ? " · " + kr.modelData.sessions + " session" + (kr.modelData.sessions === 1 ? "" : "s") : "")
                      + " · " + kr.modelData.preset + " · " + kr.modelData.tools + " tools · " + (root.mcp ? root.mcp.ago(kr.modelData.last_used) : "")
            }
        }
        Row {
            id: kc; anchors.right: parent.right; anchors.top: parent.top; spacing: 4 * root.s
            Chip { text: "COPY"; onTapped: root.mcp.act("copy", kr.modelData.id) }
            Chip {
                text: !kr.modelData.enabled ? "ENABLE" : kr.arming ? "SURE?" : "DISABLE"; hot: kr.arming
                onTapped: {
                    if (!kr.modelData.enabled) root.mcp.act("enable", kr.modelData.id);
                    else if (kr.arming) { kr.arming = false; root.mcp.act("disable", kr.modelData.id); }
                    else { kr.arming = true; disarm.restart(); }
                }
            }
        }
    }

    component Hair: Rectangle { width: parent ? parent.width : 0; height: 1; color: Theme.hair }

    // ── layout ───────────────────────────────────────────────────────────────
    Column {
        id: col
        width: root.w
        spacing: 10 * root.s

        // tab row
        Row {
            width: parent.width
            spacing: 6 * root.s
            Repeater {
                model: [{ id: "wotr", t: "WOTR" }, { id: "mcp", t: "MCP" }, { id: "quill", t: "QUILL" }, { id: "mc", t: "SERVER" }]
                Rectangle {
                    id: tb
                    required property var modelData
                    readonly property bool on: root.tab === modelData.id
                    width: (col.width - 18 * root.s) / 4; height: 22 * root.s; radius: 0
                    color: on ? Theme.accent : (th.hovered ? Theme.sheen : "transparent")
                    border.width: 1; border.color: on ? Theme.accent : Theme.border
                    Text { anchors.centerIn: parent; text: tb.modelData.t; color: tb.on ? Theme.panelBot : Theme.cream; font.family: Theme.mono; font.pixelSize: 9 * root.s; font.weight: Font.DemiBold; font.letterSpacing: 2 * root.s }
                    HoverHandler { id: th; cursorShape: Qt.PointingHandCursor }
                    TapHandler { onTapped: if (root.svc) root.svc.tab = tb.modelData.id }
                }
            }
        }

        // ── WOTR ────────────────────────────────────────────────────────────
        Column {
            visible: root.tab === "wotr"
            width: parent.width
            spacing: 10 * root.s
            readonly property var info: root.wotr ? root.wotr.info : ({})
            id: wv
            // every field the view reads must be present, not just the daemons key the service keys on
            readonly property bool loaded: !!(info && info.rules && info.scenes && info.conflicts && info.git && info.continue)

            Hero {
                icon: "swords"; title: "War of the Realms"
                caption: wv.loaded ? (root.svc.fmt(wv.info.rules.live) + " LIVE RULES · " + root.svc.fmt(wv.info.scenes.count) + " SCENES · " + Math.round(wv.info.scenes.words / 1000) + "K WORDS")
                                   : (wv.info.error ? String(wv.info.error).toUpperCase() : "LOADING…")
                number: wv.loaded ? String(root.wotr.waiting) : "—"; numberLabel: "WAITING ON ISAAC"; urgent: root.wotr ? root.wotr.waiting > 0 : false
            }
            Row {
                width: parent.width; spacing: 6 * root.s
                readonly property real cell: (width - spacing * 4) / 5
                Btn { width: parent.cell; icon: "folder_code"; label: "REPO";     onClicked: root.wotr.openRepo() }
                Btn { width: parent.cell; icon: "auto_stories"; label: "VAULT";   onClicked: root.wotr.openVault() }
                Btn { width: parent.cell; icon: "description"; label: "CONTINUE"; onClicked: root.wotr.openContinue() }
                Btn { width: parent.cell; icon: "sync"; label: "SYNC";            onClicked: root.wotr.syncNow() }
                Btn { width: parent.cell; icon: "receipt_long"; label: "LOGS";    onClicked: root.wotr.openLogs() }
            }
            MicroLabel { label: "Daemons"; s: root.s }
            Repeater {
                model: wv.info.daemons || []
                SRow { required property var modelData; dot: modelData.state === "active" ? Theme.accent : modelData.unit ? Theme.verm : Theme.dim; label: modelData.label; detail: modelData.detail || (modelData.unit + " · " + modelData.state); action: modelData.unit ? "RESTART" : ""; onTriggered: root.wotr.restartUnit(modelData.unit) }
            }
            MicroLabel { label: "Services"; s: root.s; visible: (wv.info.services || []).length > 0 }
            Repeater {
                model: wv.info.services || []
                SRow { required property var modelData; dot: modelData.state === "active" ? Theme.accent : Theme.verm; label: modelData.label; detail: modelData.state; action: modelData.restart ? "RESTART" : ""; onTriggered: root.wotr.restartUnit(modelData.unit) }
            }
            MicroLabel { label: "Docker"; s: root.s }
            Repeater {
                model: wv.info.containers || []
                SRow { required property var modelData; dot: modelData.healthy ? Theme.accent : Theme.verm; label: modelData.name; detail: modelData.status + " · " + modelData.image; action: "RESTART"; onTriggered: root.wotr.restartContainer(modelData.name) }
            }
            Text { visible: wv.loaded && !(wv.info.containers || []).length; text: "no containers running"; color: Theme.faint; font.family: Theme.mono; font.pixelSize: 9 * root.s }
            MicroLabel { label: "Timers"; s: root.s }
            Repeater {
                model: wv.info.timers || []
                SRow { required property var modelData; dot: modelData.running ? Theme.accent : Theme.dim; label: modelData.label; detail: modelData.running ? "running now" : (modelData.next + "  ·  " + modelData.left); action: "RUN"; onTriggered: root.wotr.startUnit(modelData.unit) }
            }
            MicroLabel { label: "Index & repo"; s: root.s }
            KV { label: "Docket";         value: wv.loaded ? wv.info.docket + " outstanding" : "" }
            KV { label: "Conflicts";      value: wv.loaded ? (wv.info.conflicts.open + " open of " + wv.info.conflicts.total) : ""; link: true; onClicked: root.wotr.openConflicts() }
            KV { label: "Rulings queued"; value: wv.loaded ? String(wv.info.rulings) : "" }
            KV { label: "Branch";         value: wv.loaded ? (wv.info.git.branch + (wv.info.git.dirty ? "  ·  " + wv.info.git.dirty + " uncommitted" : "  ·  clean")) : "" }
            KV { label: "Last commit";    value: wv.loaded ? (wv.info.git.hash + "  " + wv.info.git.when + "  ·  " + wv.info.git.subject) : "" }
            KV { label: "CONTINUE.md";    value: wv.loaded ? (wv.info.continue.date + (wv.info.continue.headline ? "  ·  " + wv.info.continue.headline : "")) : ""; link: true; onClicked: root.wotr.openContinue() }
            Text { width: parent.width; text: wv.loaded ? "refreshed " + wv.info.generated : ""; color: Theme.faint; font.family: Theme.mono; font.pixelSize: 8 * root.s; horizontalAlignment: Text.AlignRight }
        }

        // ── MCP ─────────────────────────────────────────────────────────────
        Column {
            id: keyv
            visible: root.tab === "mcp"
            width: parent.width
            spacing: 10 * root.s
            readonly property var info: root.mcp ? root.mcp.info : ({})
            readonly property bool up: !!info.up
            readonly property var keys: info.keys || []

            Hero {
                icon: "hub"; title: "WOTR MCP"
                caption: !root.mcp || !root.mcp.loaded ? "LOADING…" : keyv.up ? (keyv.keys.length + " KEY" + (keyv.keys.length === 1 ? "" : "S") + " · " + (keyv.info.total || 0) + " TOOLS") : "THE MCP SERVER IS NOT ANSWERING"
                number: keyv.up ? String(keyv.info.online || 0) : "—"; numberLabel: "ONLINE"; urgent: !keyv.up && !!(root.mcp && root.mcp.loaded)
            }
            Row {
                width: parent.width; spacing: 6 * root.s
                readonly property real cell: (width - spacing * 2) / 3
                Btn { width: parent.cell; icon: "tune"; label: "MANAGE"; enabled: keyv.up; onClicked: root.mcp.manage() }
                Btn { width: parent.cell; icon: "restart_alt"; label: "RESTART"; onClicked: root.mcp.restart() }
                Btn { width: parent.cell; icon: "refresh"; label: "REFRESH"; onClicked: root.mcp.refresh() }
            }
            MicroLabel { label: "Servers"; s: root.s }
            Repeater {
                model: root.wotr ? (root.wotr.info.daemons || []).filter(d => d.label.indexOf("MCP") >= 0) : []
                SRow { required property var modelData; dot: modelData.state === "active" ? Theme.accent : modelData.unit ? Theme.verm : Theme.dim; label: modelData.label; detail: modelData.detail || (modelData.unit + " · " + modelData.state); action: "" }
            }
            MicroLabel { label: "Keys"; s: root.s }
            Repeater { model: keyv.keys; KeyRow {} }
            Text {
                width: parent.width; wrapMode: Text.WordWrap; color: Theme.faint; font.family: Theme.mono; font.pixelSize: 8.5 * root.s
                text: "MANAGE opens the dashboard: new keys, names, permissions, rotate, delete."
            }
        }

        // ── QUILL ───────────────────────────────────────────────────────────
        Column {
            id: qv
            visible: root.tab === "quill"
            width: parent.width
            spacing: 10 * root.s
            readonly property var info: root.quill ? root.quill.info : ({})
            readonly property bool loaded: root.quill ? root.quill.loaded : false
            property int mode: 0
            property int picked: -1
            readonly property var units: root.quill ? root.quill.unitsFor(mode, info.history || {}) : []
            readonly property var focused: units[picked >= 0 && picked < units.length ? picked : units.length - 1] || { name: "", words: 0, known: false }
            readonly property int peak: units.reduce((m, u) => Math.max(m, u.words), 0)

            Hero {
                icon: "stylus_note"; title: "Quill"
                caption: qv.loaded ? (root.svc.fmt(qv.info.total) + " WORDS TRACKED · GOAL " + root.svc.fmt(root.svc.dailyGoal) + " A DAY") : "COUNTING…"
                number: qv.loaded ? root.svc.signed(root.quill.today) : "—"; numberLabel: "WORDS TODAY"
            }
            Rectangle {
                width: parent.width; height: 5 * root.s; radius: 0; color: Theme.hair
                Rectangle { width: parent.width * (root.quill ? root.quill.progress : 0); height: parent.height; color: Theme.accent }
            }
            Item {
                width: parent.width; implicitHeight: modes.implicitHeight
                MicroLabel { anchors.left: parent.left; anchors.verticalCenter: parent.verticalCenter; s: root.s; label: qv.focused.name + " · " + (qv.focused.known ? root.svc.fmt(qv.focused.words) + " words" : "not counted") }
                Row {
                    id: modes; anchors.right: parent.right; spacing: 4 * root.s
                    Repeater {
                        model: ["DAYS", "WEEKS", "MONTHS"]
                        Rectangle {
                            required property string modelData; required property int index
                            width: mt.implicitWidth + 12 * root.s; height: 16 * root.s; radius: 0
                            color: qv.mode === index ? Theme.accent : "transparent"; border.width: 1; border.color: qv.mode === index ? Theme.accent : Theme.border
                            Text { id: mt; anchors.centerIn: parent; text: parent.modelData; color: qv.mode === parent.index ? Theme.panelBot : Theme.cream; font.family: Theme.mono; font.pixelSize: 8 * root.s; font.letterSpacing: 1.2 * root.s }
                            TapHandler { onTapped: qv.mode = parent.index }
                            HoverHandler { cursorShape: Qt.PointingHandCursor }
                        }
                    }
                }
            }
            Row {
                id: bars
                width: parent.width; spacing: 3 * root.s
                readonly property real cell: (width - spacing * (qv.units.length - 1)) / Math.max(1, qv.units.length)
                readonly property real barH: 44 * root.s
                Repeater {
                    model: qv.units
                    Item {
                        id: cell
                        required property var modelData; required property int index
                        readonly property bool lit: index === (qv.picked >= 0 ? qv.picked : qv.units.length - 1)
                        width: bars.cell; height: bars.barH + lbl.implicitHeight + 2
                        Rectangle { anchors.bottom: lbl.top; anchors.bottomMargin: 2; width: parent.width; height: Math.max(3, bars.barH * (qv.peak > 0 ? cell.modelData.words / qv.peak : 0)); color: cell.lit ? Theme.accent : (cell.modelData.known ? Theme.dim : Theme.hair) }
                        Text { id: lbl; anchors.bottom: parent.bottom; anchors.horizontalCenter: parent.horizontalCenter; text: cell.modelData.label; color: Theme.faint; font.family: Theme.mono; font.pixelSize: 7.5 * root.s }
                        MouseArea { anchors.fill: parent; hoverEnabled: true; onEntered: qv.picked = cell.index; onExited: qv.picked = -1 }
                    }
                }
            }
            MicroLabel { s: root.s; label: !root.quill ? "Sprint" : root.quill.sprintRunning ? "Sprint · " + root.svc.mmss(root.quill.sprintSecondsLeft) + " left" : (root.quill.sprintDone ? "Sprint over · " + root.svc.signed(root.quill.sprintWords) + " words" : "Sprint") }
            Row {
                width: parent.width; spacing: 6 * root.s
                readonly property int count: root.quill && root.quill.sprintRunning ? 1 : 3
                readonly property real cell: (width - spacing * (count - 1)) / count
                Repeater {
                    model: root.quill && root.quill.sprintRunning ? [] : [15, 25, 45]
                    Btn { required property int modelData; width: parent.cell; icon: "timer"; label: modelData + " MIN"; onClicked: root.quill.startSprint(modelData) }
                }
                Btn { visible: root.quill ? root.quill.sprintRunning : false; width: parent.cell; icon: "stop_circle"; label: "STOP · " + (root.quill ? root.svc.signed(root.quill.sprintWords) : "") + " SO FAR"; onClicked: root.quill.stopSprint() }
            }
            MicroLabel { label: "Touched today"; s: root.s }
            Text { visible: qv.loaded && (qv.info.files || []).length === 0; width: parent.width; text: "Nothing yet. The page is patient."; color: Theme.faint; font.family: Theme.font; font.pixelSize: 11 * root.s }
            Repeater {
                model: qv.loaded ? (qv.info.files || []).slice(0, 8) : []
                KV { required property var modelData; label: modelData.name; value: root.svc.signed(modelData.delta); link: true; onClicked: root.svc.run("code " + root.svc.q(modelData.path)) }
            }
        }

        // ── SERVER ──────────────────────────────────────────────────────────
        Column {
            id: mv
            visible: root.tab === "mc"
            width: parent.width
            spacing: 10 * root.s
            readonly property var info: root.mcs ? root.mcs.info : ({})
            readonly property bool running: root.mcs ? root.mcs.running : false
            readonly property bool booting: root.mcs ? root.mcs.booting : false
            readonly property bool pending: root.mcs ? root.mcs.pending : false

            Hero {
                icon: "deployed_code"; title: mv.info.motd || "Minecraft server"
                caption: mv.pending ? "WORKING…" : mv.booting ? "BOOTING" : mv.running ? "ONLINE · UP " + mv.info.uptime : (root.mcs && root.mcs.missing) ? "NO SERVER FOLDER" : "STOPPED"
                number: mv.running ? mv.info.online + "/" + mv.info.max : "—"; numberLabel: "PLAYERS"
            }
            Row {
                width: parent.width; spacing: 6 * root.s
                readonly property real cell: (width - spacing * 3) / 4
                Btn { width: parent.cell; icon: mv.running ? "stop_circle" : "play_circle"; label: mv.running ? "STOP" : "START"; onClicked: mv.running ? root.mcs.stop() : root.mcs.start() }
                Btn { width: parent.cell; icon: "terminal"; label: "CONSOLE"; enabled: mv.running && !mv.booting; onClicked: root.mcs.openConsole() }
                Btn { width: parent.cell; icon: "receipt_long"; label: "LOGS"; onClicked: root.mcs.openLogs() }
                Btn { width: parent.cell; icon: "backup"; label: "BACKUP"; onClicked: root.mcs.backup() }
            }
            MicroLabel { label: "Online now"; s: root.s }
            Text { visible: (mv.info.players || []).length === 0; width: parent.width; text: mv.running ? (mv.booting ? "Server is still booting." : "Nobody's on. The realm sleeps.") : "Server is stopped."; color: Theme.faint; font.family: Theme.font; font.pixelSize: 11 * root.s }
            Repeater {
                model: mv.info.players || []
                Text { required property string modelData; width: parent.width; text: "•  " + modelData; color: Theme.cream; font.family: Theme.font; font.pixelSize: 11 * root.s }
            }
            MicroLabel { label: "Server"; s: root.s }
            KV { label: "Version"; value: [mv.info.type, mv.info.version].filter(x => x).join(" ") }
            KV { label: "Modpack"; value: mv.info.pack || "—" }
            KV { label: "Folder";  value: root.svc ? root.svc.mcDir : ""; link: true; onClicked: root.mcs.openFolder() }
        }
    }
}
