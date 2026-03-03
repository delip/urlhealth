# url-health Agent Skill

An [Agent Skill](https://agentskills.io) that lets you check URL liveness by asking naturally or using the `/url-health` slash command. Compatible with any agent that supports the agentskills.io open standard — Claude Code, Codex CLI, Gemini CLI, OpenHands, GitHub Copilot, and [others](https://agentskills.io).

## What It Does

Checks whether URLs are live, dead, or likely hallucinated using the [urlhealth](https://pypi.org/project/urlhealth/) Python library. For dead URLs, it automatically provides a Wayback Machine archive link when available.

| Status | Meaning |
|---|---|
| `LIVE` | URL returned HTTP 200 |
| `DEAD` | URL returned 404, Wayback snapshot available |
| `LIKELY_HALLUCINATED` | URL returned 404, no Wayback snapshot |
| `UNKNOWN` | Other HTTP status or connection error |

## Installation

Copy the skill directory into your agent's skills location. For example:

**Claude Code (personal):**

```bash
cp -r skill/url-health ~/.claude/skills/url-health
```

**Claude Code (project-specific):**

```bash
cp -r skill/url-health .claude/skills/url-health
```

For other agents, consult their documentation on where to install agentskills.io-compatible skills.

## Usage

**Natural language** (auto-triggers from context):

```
Check if https://example.com is alive
```

```
Is this link broken? https://some-old-page.com/article
```

```
Validate these URLs for me: https://a.com, https://b.com
```

**Slash command:**

```
/url-health https://example.com
```

```
/url-health https://example.com https://old-site.org/page
```

## Skill Structure

```
url-health/
├── SKILL.md                 # Main skill instructions
└── references/
    └── api-guide.md         # Detailed API and algorithm reference
```

## License

MIT
