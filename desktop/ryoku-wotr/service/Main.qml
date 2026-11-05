pragma ComponentBehavior: Bound

import QtQuick
import Quickshell
import Quickshell.Io

// The WOTR plugin's service: four pollers (bin/collect.sh, bin/mcp.sh, bin/words.sh,
// bin/status.sh) and every action the glyph and the panel can take. One
// instance lives as long as the bar row; the views bind it as
// pluginApi.mainInstance. `tab` is which of the four the panel shows.
// IPC (for keybinds):  qs -c shell ipc call wotr toggle wotr|mcp|quill|mc
//                      qs -c shell ipc call wotr sprint 25
//                      qs -c shell ipc call wotr mcPress
Item {
    id: svc

    property var pluginApi
    readonly property var settings: pluginApi ? pluginApi.pluginSettings : null
    readonly property string bin: pluginApi ? pluginApi.pluginDir + "/bin" : ""
    readonly property string home: Quickshell.env("HOME")
    readonly property string repo: home + "/wotr-rule-index"
    readonly property string mcDir: home + "/minecraft"
    readonly property string mc: mcDir + "/mc"
    readonly property var quillPaths: [repo + "/scenes", repo + "/book", repo + "/vault", home + "/wotr-vault/true-canon"]
    readonly property int dailyGoal: (settings && settings.dailyGoal) ? Number(settings.dailyGoal) : 150000

    property string tab: "wotr"

    function run(cmd) { Quickshell.execDetached(["sh", "-c", cmd]) }
    function q(v) { return "'" + String(v).replace(/'/g, "'\\''") + "'" }
    function fmt(n) { return Number(n || 0).toLocaleString(Qt.locale(), "f", 0) }
    function signed(n) { return (n > 0 ? "+" : "") + fmt(n) }
    function mmss(s) { const m = Math.floor(s / 60), r = s % 60; return m + ":" + (r < 10 ? "0" : "") + r }

    function show(t) { tab = t; if (pluginApi) pluginApi.openPanel() }
    function toggle(t) {
        if (!pluginApi) return;
        if (pluginApi.panelOpen && tab === t) pluginApi.closePanel();
        else { tab = t; pluginApi.openPanel(); }
    }
    function refreshAll() { if (bin) { wotr.refresh(); mcp.refresh(); quill.refresh(); mcs.refresh(); } }
    onBinChanged: refreshAll()
    Timer { id: soon; interval: 2500; onTriggered: svc.refreshAll() }

    // ── WOTR: rule index, daemons, timers, repo ──────────────────────────────
    property QtObject wotr: QtObject {
        id: wotr
        property var info: ({})
        readonly property bool loaded: info && info.daemons !== undefined
        readonly property int waiting: (info.docket || 0) + ((info.conflicts && info.conflicts.open) || 0)
        readonly property bool daemonDown: (info.daemons || []).some(d => d.unit && d.state !== "active")  // the private MCP has no unit: no session open is not a fault
        property string buf: ""
        property Process proc: Process {
            command: ["bash", svc.bin + "/collect.sh", svc.repo]
            stdout: StdioCollector { onStreamFinished: wotr.buf = text }
            onExited: { try { wotr.info = JSON.parse(wotr.buf || "{}"); } catch (e) { wotr.info = { error: "collector output was not JSON" }; } }
        }
        function refresh() { if (svc.bin && !proc.running) proc.running = true }
        function openRepo()      { svc.run("code " + svc.q(svc.repo)) }
        function openVault()     { svc.run("obsidian " + svc.q("obsidian://open?path=" + svc.repo)) }
        function openConflicts() { svc.run("code " + svc.q(svc.repo + "/CONFLICTS.md")) }
        function openContinue()  { svc.run("code " + svc.q(svc.repo + "/CONTINUE.md")) }
        function openLogs()      { svc.run("ghostty --class=wotr-logs -e journalctl --user -f -n 200 -u wotr-bot -u wotr-jobs -u wotr-mcp-public -u wotr-sync -u wotr-nightly -u wotr-book") }
        function syncNow()       { svc.run("systemctl --user start wotr-sync.service"); soon.restart() }
        function restartUnit(u)  { svc.run("systemctl --user restart " + svc.q(u + ".service")); soon.restart() }
        function restartContainer(n) { Quickshell.execDetached(["docker", "restart", n]); soon.restart() }
        function startUnit(u)    { svc.run("systemctl --user start " + svc.q(u + ".service")); soon.restart() }
    }
    Timer { interval: 60000; running: true; repeat: true; onTriggered: wotr.refresh() }

    // ── MCP: the named keys on the WOTR MCP, through the dashboard (127.0.0.1:8790) ──
    // bin/mcp.sh keeps every token out of what this object holds.
    property QtObject mcp: QtObject {
        id: mcp
        property var info: ({ up: false, keys: [] })
        property bool loaded: false
        readonly property int online: info.online || 0
        property string buf: ""
        property Process proc: Process {
            command: ["bash", svc.bin + "/mcp.sh", "list"]
            stdout: StdioCollector { onStreamFinished: mcp.buf = text }
            onExited: { try { mcp.info = JSON.parse(mcp.buf || "{}"); mcp.loaded = true; } catch (e) { mcp.info = { up: false, keys: [] }; } }
        }
        function refresh() { if (svc.bin && !proc.running) proc.running = true }
        // argv, never a shell string
        function act(verb, id) { Quickshell.execDetached(["bash", svc.bin + "/mcp.sh", verb, id]); mcpSoon.restart() }
        function manage()      { Quickshell.execDetached(["xdg-open", "http://127.0.0.1:8790/"]) }
        function restart()     { svc.run("systemctl --user restart wotr-mcp-public.service"); mcpSoon.restart() }
        function ago(t) {
            if (!t) return "never used";
            const s = (info.now || 0) - t;
            if (s < 60) return "just now";
            if (s < 3600) return Math.floor(s / 60) + " min ago";
            if (s < 86400) return Math.floor(s / 3600) + " h ago";
            return Math.floor(s / 86400) + " d ago";
        }
    }
    Timer { interval: 30000; running: true; repeat: true; onTriggered: mcp.refresh() }
    Timer { id: mcpSoon; interval: 800; onTriggered: mcp.refresh() }

    // ── Quill: words today, history, sprints ─────────────────────────────────
    property QtObject quill: QtObject {
        id: quill
        property var info: ({})
        readonly property bool loaded: info && info.total !== undefined
        readonly property int today: loaded ? Number(info.today) : 0
        readonly property real progress: Math.max(0, Math.min(1, today / svc.dailyGoal))
        property int sprintMinutes: 0
        property int sprintSecondsLeft: 0
        property int sprintStartWords: 0
        property bool sprintDone: false
        readonly property bool sprintRunning: sprintSecondsLeft > 0
        readonly property int sprintWords: today - sprintStartWords
        property string buf: ""
        property Process proc: Process {
            command: ["bash", svc.bin + "/words.sh"].concat(svc.quillPaths)
            stdout: StdioCollector { onStreamFinished: quill.buf = text }
            onExited: { try { quill.info = JSON.parse(quill.buf || "{}"); } catch (e) { quill.info = {}; } }
        }
        function refresh() { if (svc.bin && !proc.running) proc.running = true }
        function startSprint(minutes) { sprintMinutes = minutes; sprintSecondsLeft = minutes * 60; sprintStartWords = today; sprintDone = false; refresh() }
        function stopSprint() { sprintSecondsLeft = 0; sprintDone = false }
        function tick() {
            sprintSecondsLeft -= 1;
            if (sprintSecondsLeft === 0) {
                sprintDone = true; refresh();
                svc.run("notify-send " + svc.q("Sprint over") + " " + svc.q(sprintWords + " words in " + sprintMinutes + " min"));
            }
        }
        function isoKey(d) {
            const m = d.getMonth() + 1, day = d.getDate();
            return d.getFullYear() + "-" + (m < 10 ? "0" : "") + m + "-" + (day < 10 ? "0" : "") + day;
        }
        // Last 14 days / 12 weeks / 12 months from the per-day history. No snapshot = not counted, not zero.
        function unitsFor(mode, history) {
            const now = new Date(), units = [], n = mode === 0 ? 14 : 12;
            for (let i = n - 1; i >= 0; i--) {
                let start, end, label, name;
                if (mode === 0) {
                    start = new Date(now.getFullYear(), now.getMonth(), now.getDate() - i);
                    end = new Date(start.getFullYear(), start.getMonth(), start.getDate() + 1);
                    label = Qt.formatDate(start, "d"); name = Qt.formatDate(start, "ddd d MMM");
                } else if (mode === 1) {
                    start = new Date(now.getFullYear(), now.getMonth(), now.getDate() - ((now.getDay() + 6) % 7) - 7 * i);
                    end = new Date(start.getFullYear(), start.getMonth(), start.getDate() + 7);
                    label = Qt.formatDate(start, "d/M"); name = "Week of " + Qt.formatDate(start, "d MMM");
                } else {
                    start = new Date(now.getFullYear(), now.getMonth() - i, 1);
                    end = new Date(start.getFullYear(), start.getMonth() + 1, 1);
                    label = Qt.formatDate(start, "MMM"); name = Qt.formatDate(start, "MMMM yyyy");
                }
                let words = 0, known = false;
                for (let d = new Date(start); d < end; d.setDate(d.getDate() + 1)) {
                    const k = isoKey(d);
                    if (k in history) { words += history[k]; known = true; }
                }
                units.push({ label, name, words, known });
            }
            return units;
        }
    }
    Timer { interval: 30000; running: true; repeat: true; onTriggered: quill.refresh() }
    Timer { interval: 1000; repeat: true; running: quill.sprintRunning; onTriggered: quill.tick() }

    // ── Minecraft server (~/minecraft, docker) ───────────────────────────────
    property QtObject mcs: QtObject {
        id: mcs
        property var info: ({ state: "unknown", players: [], online: 0, max: 0 })
        property bool pending: false
        readonly property bool running: info.state === "running"
        readonly property bool booting: running && info.health !== "healthy"
        readonly property bool missing: info.state === "missing"
        property string buf: ""
        property Process proc: Process {
            command: ["bash", svc.bin + "/status.sh", svc.mcDir]
            stdout: StdioCollector { onStreamFinished: mcs.buf = text }
            onExited: {
                try {
                    const next = JSON.parse(mcs.buf || "{}");
                    if (mcs.pending && next.state !== mcs.info.state) mcs.pending = false;
                    mcs.info = next;
                } catch (e) { mcs.info = { state: "unknown", players: [], online: 0, max: 0 }; }
            }
        }
        function refresh() { if (svc.bin && !proc.running) proc.running = true }
        function start() { if (missing) return; pending = true; svc.run(svc.q(svc.mc) + " up >/dev/null 2>&1 && notify-send 'Minecraft server starting'"); fastPoll.restart() }
        function stop()  { pending = true; svc.run(svc.q(svc.mc) + " down >/dev/null 2>&1 && notify-send 'Minecraft server stopped'"); fastPoll.restart(); if (svc.pluginApi) svc.pluginApi.closePanel() }
        function press() { if (running || pending) svc.toggle("mc"); else start() }
        function openLogs()    { svc.run("ghostty --class=mc-logs -e " + svc.q(svc.mc) + " logs") }
        function openConsole() { svc.run("ghostty --class=mc-console -e " + svc.q(svc.mc) + " console") }
        function backup()      { svc.run("ghostty --class=mc-backup -e sh -c " + svc.q(svc.q(svc.mc) + " backup; echo; read -p 'Done. Enter to close.'")) }
        function openFolder()  { svc.run("code " + svc.q(svc.mcDir + "/.env")) }
    }
    Timer { interval: 15000; running: true; repeat: true; onTriggered: mcs.refresh() }
    Timer { id: fastPoll; interval: 2000; repeat: true; running: mcs.pending || mcs.booting; onTriggered: mcs.refresh() }
    Timer { interval: 60000; running: mcs.pending; onTriggered: mcs.pending = false }

    // The bar hosts one service per bar variant, so a second copy registers the
    // same target; Quickshell keeps the first and warns. Both copies share one
    // panel, so whichever wins works.
    IpcHandler {
        target: "wotr"
        function open(tab: string): void { svc.show(tab || "wotr"); }
        function close(): void { if (svc.pluginApi) svc.pluginApi.closePanel(); }
        function toggle(tab: string): void { svc.toggle(tab || "wotr"); }
        function refresh(): void { svc.refreshAll(); }
        function sprint(minutes: string): void { quill.startSprint(parseInt(minutes, 10) || 25); svc.show("quill"); }
        function sprintStop(): void { quill.stopSprint(); }
        function mcPress(): void { mcs.press(); }
    }
}
