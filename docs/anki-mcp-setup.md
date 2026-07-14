# Anki MCP Setup

This skill tells Codex how to create and verify Anki notes, but it does not provide Anki access by itself. Each computer also needs a local bridge between the MCP host and Anki Desktop.

Use one of the setups below. Do not mix ports or configuration snippets from different Anki MCP variants unless you intentionally installed that variant.

## Read-Only Diagnosis First

Before installing a bridge or changing MCP settings, run the bundled read-only diagnostic from the repository root:

```powershell
python .\skills\round-textbook-anki\scripts\diagnose_environment.py
```

It checks the operating system, Python packages, Node/`npx`, whether Anki appears to be running, ports `3141` and `8765`, and the harmless AnkiConnect `version` action. It does not install software, change configuration, or write Anki notes. Use its recommendation to select one path below.

Installing Anki, an add-on, Python packages, Node packages, or an MCP server and editing MCP configuration are state-changing actions. An agent must explain the exact change and obtain approval before performing them. A harmless deck-list read should succeed before any Anki write is allowed.

## Recommended Decision Path

| Situation | Recommended setup | Local endpoint |
| --- | --- | --- |
| Codex Desktop can connect directly to a local Anki add-on | Native AnkiMCP add-on inside Anki | `http://127.0.0.1:3141` |
| MCP host expects a stdio server and you already use AnkiConnect | `@ankimcp/anki-mcp-server` wrapping AnkiConnect | AnkiConnect at `http://localhost:8765` |
| Existing scripts or non-MCP tools use AnkiConnect directly | AnkiConnect only | `http://127.0.0.1:8765` |
| Web-only assistant cannot reach your computer | MCP HTTP server plus a tunnel only when needed | Varies; treat as internet-exposed |

## Option A: Native AnkiMCP Add-on

Use this path when your MCP host can talk to an HTTP/SSE endpoint started by an Anki add-on on the same machine.

1. Install Anki Desktop.
2. Open Anki.
3. Install the native AnkiMCP add-on variant you intend to use.
4. Restart Anki and open the correct profile.
5. Confirm the local endpoint is reachable.
6. Point Codex or your MCP host at that endpoint.

For the local Codex setup used by this workflow, the expected endpoint is:

```text
http://127.0.0.1:3141
```

Codex-style MCP config:

```toml
[mcp_servers.anki]
url = "http://127.0.0.1:3141"
```

Quick reachability check from PowerShell:

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:3141" -UseBasicParsing
```

A plain browser or `Invoke-WebRequest` request may return an HTTP error such as `406`, `Missing session ID`, or another protocol-level response. That can still mean the add-on is listening. The real check is whether the MCP host exposes Anki tools and can run a harmless read action such as listing decks.

## Option B: AnkiConnect plus an MCP Wrapper

Use this path when your MCP host launches a stdio MCP server and that server talks to AnkiConnect.

1. Install Anki Desktop.
2. Install AnkiConnect, commonly listed on AnkiWeb as code `2055492159`.
3. Restart Anki and open the correct profile.
4. Confirm AnkiConnect responds on `http://localhost:8765`.
5. Configure an MCP wrapper such as `@ankimcp/anki-mcp-server`.

Check AnkiConnect from PowerShell:

```powershell
$body = '{"action":"version","version":6}'
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8765" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

Example MCP stdio config:

```json
{
  "mcpServers": {
    "anki-mcp": {
      "command": "npx",
      "args": ["-y", "@ankimcp/anki-mcp-server", "--stdio"],
      "env": {
        "ANKI_CONNECT_URL": "http://localhost:8765"
      }
    }
  }
}
```

Windows MCP hosts sometimes cannot spawn `npx` directly. In that case, use `cmd /c`:

```json
{
  "mcpServers": {
    "anki-mcp": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@ankimcp/anki-mcp-server", "--stdio"],
      "env": {
        "ANKI_CONNECT_URL": "http://localhost:8765"
      }
    }
  }
}
```

Read-only exploration:

```json
{
  "mcpServers": {
    "anki-mcp": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@ankimcp/anki-mcp-server", "--stdio", "--read-only"],
      "env": {
        "ANKI_CONNECT_URL": "http://localhost:8765"
      }
    }
  }
}
```

Do not use read-only mode when you expect Codex to create or update notes.

## Option C: AnkiConnect Directly

AnkiConnect is useful for scripts and compatibility layers, but it is not an MCP server by itself.

Use it directly only when your automation code already knows the AnkiConnect HTTP API. If the client expects MCP tools, place an MCP wrapper in front of AnkiConnect.

## Security Notes

- Keep local-only setups bound to `127.0.0.1` or `localhost`.
- Do not expose Anki write access to the public internet.
- Use tunnels such as `ngrok` only when a remote web client truly cannot reach your local MCP host.
- If you tunnel, use the shortest practical session, avoid sharing the URL broadly, and stop the tunnel after the task.
- Do not commit real `config.toml`, local Anki profile paths, tunnel tokens, or public tunnel URLs.

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| No Anki tools appear in the MCP host | MCP config not loaded, wrong config file, or host not restarted | Restart the host and verify the exact MCP config path |
| `connection refused` on `3141` | Native add-on is not running or wrong variant/port | Open Anki, load the profile, check add-on config |
| `connection refused` on `8765` | AnkiConnect is not installed or Anki is closed | Install/enable AnkiConnect, restart Anki |
| `502`, upstream error, or timeout | Anki was closed, profile locked, or add-on server stale | Open Anki, select the profile, restart Anki if needed |
| AnkiConnect works but MCP tools do not | MCP wrapper is misconfigured | Check `ANKI_CONNECT_URL`, `npx`/Node availability, and wrapper logs |
| Native MCP docs mention a different add-on code or SSE path | Different AnkiMCP variant | Use one variant consistently; do not combine `3141`, `4473/sse`, and `8765` snippets |
| Codex sees a stale Anki connector but not local MCP tools | Tool manifest/session not refreshed | Restart Codex after changing MCP config |

## Verification Checklist

1. Anki Desktop is open.
2. The correct Anki profile is selected and unlocked.
3. The intended bridge is installed and enabled.
4. The expected local endpoint responds or at least shows a protocol-level response.
5. The MCP host shows Anki tools.
6. A harmless read action works, such as listing decks or reading deck names.
7. Only after read verification, allow note creation or update workflows.
8. Create only 2-3 trial notes first, then re-read their Front, Back, deck, tags, images, and answers.
9. Continue to the full batch only after the trial readback passes.

## References

- Native Anki MCP server package: <https://github.com/ankimcp/anki-mcp-server>
- AnkiMCP add-on documentation variant: <https://ankimcp.com/docs>
- AnkiConnect project: <https://github.com/FooSoft/anki-connect>
