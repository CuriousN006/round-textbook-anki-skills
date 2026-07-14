# Native AnkiMCP Setup

This repository supports one Anki connection path:

```text
AI agent -> native AnkiMCP connection at http://127.0.0.1:3141 -> Anki Desktop
```

Do not install or combine additional Anki bridges for this workflow.

## Read-Only Diagnosis First

Before installing the add-on or changing agent settings, run the bundled read-only diagnostic from the repository root:

```powershell
python .\skills\round-textbook-anki\scripts\diagnose_environment.py
```

It checks the operating system, Python packages, whether Anki appears to be running, and whether `127.0.0.1:3141` is reachable. It does not install software, change configuration, or write Anki notes.

Installing Anki, installing the add-on, or editing the agent's MCP configuration changes the computer. The agent must explain the exact change and obtain approval before performing it.

## Setup

1. Install [Anki Desktop](https://apps.ankiweb.net/) from its official source.
2. Open Anki Desktop and select the intended profile.
3. Open **Tools -> Add-ons -> Get Add-ons**, enter code `124672614`, and install the [AnkiMCP Server add-on](https://ankiweb.net/shared/info/124672614).
4. Restart Anki Desktop.
5. Configure the AI agent to use the endpoint.
6. Restart or refresh the agent so its Anki tools appear.

The only endpoint used by this repository is:

```text
http://127.0.0.1:3141
```

Codex configuration:

```toml
[mcp_servers.anki]
url = "http://127.0.0.1:3141"
```

Codex stores MCP configuration in `~/.codex/config.toml`; on Windows, `~` means the user's profile folder. Other agents may use a different settings screen or file, so confirm the current official product documentation before editing their configuration.

## Reachability Check

From PowerShell:

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:3141" -UseBasicParsing
```

A plain web request may return a protocol-level response such as `406` or `Missing session ID`. That can still mean the add-on is listening. The authoritative check is whether the agent exposes Anki tools and can perform a harmless read action such as listing note types or decks.

## Security

- Keep the endpoint bound to `127.0.0.1`; this means only programs on the same computer can reach it.
- Do not expose Anki write access to the public internet.
- Do not commit real agent configuration files, local Anki profile paths, private deck data, or credentials.
- Use read-only Anki calls before allowing note creation, updates, deletion, rating, or sync.

## Troubleshooting

| Symptom | Likely cause | Next action |
| --- | --- | --- |
| Port `3141` is closed | Anki is closed, the add-on is missing, or the add-on did not start | Open Anki, select the profile, verify the add-on, then restart Anki |
| Port `3141` responds but no Anki tools appear | The agent configuration was not loaded | Verify the endpoint in the agent settings and restart or refresh the agent |
| Anki tools appear but reads fail | Anki is busy, the profile is locked, or the add-on is stale | Finish other Anki operations and restart Anki |
| A web request returns a protocol error | The endpoint expects MCP traffic rather than a browser request | Test with the agent's Anki tools instead of treating the web response as failure |

## Verification Checklist

1. Anki Desktop is open.
2. The correct Anki profile is selected and unlocked.
3. The native AnkiMCP add-on is installed and enabled.
4. `127.0.0.1:3141` is reachable.
5. The agent shows Anki tools.
6. A harmless read action succeeds, such as listing note types or decks.
7. Only after read verification, request approval for Anki writes.
8. Create only 2-3 trial notes first.
9. Re-read their Front, Back, deck, tags, images, and answers.
10. Continue to the full batch only after the trial readback passes.

## References

- AnkiMCP Server add-on on AnkiWeb: <https://ankiweb.net/shared/info/124672614>
- AnkiMCP Server add-on source: <https://github.com/ankimcp/anki-mcp-server-addon>
