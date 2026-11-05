# ryoku-wotr

Ryoku bar plugin: WOTR index, the WOTR MCP's keys, Quill and the Minecraft server. IPC: `qs -c shell ipc call wotr toggle wotr|mcp|quill|mc`, `... sprint 25`, `... mcPress`.

MCP tab: `bin/mcp.sh` reads the WOTR MCP's key dashboard (http://127.0.0.1:8790, this PC only) every 30 s and lists each named key: online, idle, offline or disabled, its open sessions, its permission preset and tool count, when it was last used. Every token and link is stripped before the panel sees the data. COPY fetches that key's connector URL and puts it on the clipboard with `wl-copy`; ENABLE / DISABLE change the key through the dashboard (DISABLE asks once and ends its sessions); MANAGE opens the dashboard in the browser for new keys, names, permissions, rotate and delete; RESTART restarts `wotr-mcp-public.service`. Network: 127.0.0.1:8790 only. Writes: only those key changes, through the dashboard.

WOTR tab: Daemons lists the WOTR services and the private MCP (the local stdio sessions, counted from `pgrep`). Services is a short fixed list (Tailscale, Ollama, OmniRoute, Agent Loom, Jellyfin; one that is down shows red); RESTART appears only on the user services. Docker lists running containers from `docker ps`, each with RESTART (`docker restart <name>`).
