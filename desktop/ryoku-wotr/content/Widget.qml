pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import Ryoku.PluginKit.Singletons

// The bar face: three marks in a row - swords (things waiting on Isaac; red
// when a wotr-* daemon is down), quill (words today, or the sprint clock) and
// the server cube (players online). Each mark opens the panel on its own tab;
// the cube starts the server when it is stopped, like the old bar button did.
Item {
    id: root

    property var pluginApi
    property var screen
    property bool active: false
    property string density: "glyph"
    property real s: 1
    property real widthBudget: 0

    readonly property var svc: pluginApi ? pluginApi.mainInstance : null
    readonly property var wotr: svc ? svc.wotr : null
    readonly property var quill: svc ? svc.quill : null
    readonly property var mcs: svc ? svc.mcs : null

    readonly property real mark: 19
    readonly property real gap: 5

    implicitWidth: row.implicitWidth
    implicitHeight: mark + 3

    component Mark: Item {
        id: m
        property string icon: ""
        property string label: ""
        property bool lit: false
        property bool urgent: false
        property string tip: ""
        signal clicked()
        implicitWidth: glyph.implicitWidth + (label.length > 0 ? root.gap + txt.implicitWidth : 0)
        implicitHeight: root.mark + 3
        Text {
            id: glyph
            anchors.verticalCenter: parent.verticalCenter
            text: m.icon
            font.family: "Material Symbols Rounded"
            font.pixelSize: root.mark
            font.weight: 500
            font.variableAxes: ({ "FILL": m.lit ? 1 : 0, "opsz": 20 })
            renderType: Text.QtRendering
            color: m.urgent ? Theme.verm : (m.lit ? Theme.accent : Theme.dim)
            Behavior on color { ColorAnimation { duration: 140 } }
        }
        Text {
            id: txt
            anchors.verticalCenter: parent.verticalCenter
            x: glyph.implicitWidth + root.gap
            visible: m.label.length > 0
            text: m.label
            color: Theme.cream
            font.family: Theme.mono
            font.pixelSize: 11
        }
        HoverHandler { id: hov }
        MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor; onClicked: m.clicked() }
        ToolTip {
            parent: m
            x: Math.round((m.width - width) / 2); y: m.height + 6
            delay: 350; visible: hov.hovered; text: m.tip
            background: Rectangle { color: Theme.panelBot; border.color: Theme.border; border.width: 1; radius: 0 }
            contentItem: Text { text: m.tip; color: Theme.cream; font.family: Theme.mono; font.pixelSize: 11 }
        }
    }

    Row {
        id: row
        spacing: 10
        anchors.verticalCenter: parent.verticalCenter

        Mark {
            icon: "swords"
            label: root.wotr && root.wotr.waiting > 0 ? String(root.wotr.waiting) : ""
            lit: root.svc && root.pluginApi.panelOpen && root.svc.tab === "wotr"
            urgent: root.wotr ? root.wotr.daemonDown : false
            tip: root.wotr && root.wotr.daemonDown ? "WOTR: a daemon is down" : "WOTR: " + (root.wotr ? root.wotr.waiting : 0) + " waiting on Isaac"
            onClicked: if (root.svc) root.svc.toggle("wotr")
        }
        Mark {
            icon: "stylus_note"
            label: !root.quill ? "" : root.quill.sprintRunning ? root.svc.mmss(root.quill.sprintSecondsLeft)
                 : root.quill.today > 0 ? (root.quill.today >= 1000 ? Math.round(root.quill.today / 1000) + "k" : String(root.quill.today)) : ""
            lit: root.quill ? (root.quill.sprintRunning || (root.pluginApi.panelOpen && root.svc.tab === "quill")) : false
            tip: root.quill ? "Quill: " + root.svc.signed(root.quill.today) + " words today" : "Quill"
            onClicked: if (root.svc) root.svc.toggle("quill")
        }
        Mark {
            icon: "deployed_code"
            label: root.mcs && root.mcs.running && root.mcs.info.online > 0 ? String(root.mcs.info.online) : ""
            lit: root.mcs ? (root.mcs.running || root.mcs.pending) : false
            tip: !root.mcs ? "Minecraft" : root.mcs.running ? "Minecraft: online, " + root.mcs.info.online + "/" + root.mcs.info.max + " players" : "Minecraft: stopped (click to start)"
            onClicked: if (root.mcs) root.mcs.press()
        }
    }
}
