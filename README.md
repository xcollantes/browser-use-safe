<picture>
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/user-attachments/assets/2ccdb752-22fb-41c7-8948-857fc1ad7e24">
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/user-attachments/assets/774a46d5-27a0-490c-b7d0-e65fcbbfa358">
  <img alt="Shows a black Browser Use Logo in light color mode and a white one in dark color mode." src="https://github.com/user-attachments/assets/2ccdb752-22fb-41c7-8948-857fc1ad7e24"  width="full">
</picture>

<div align="center">
    <picture>
    <source media="(prefers-color-scheme: light)" srcset="https://github.com/user-attachments/assets/9955dda9-ede3-4971-8ee0-91cbc3850125">
    <source media="(prefers-color-scheme: dark)" srcset="https://github.com/user-attachments/assets/6797d09b-8ac3-4cb9-ba07-b289e080765a">
    <img alt="The AI browser agent." src="https://github.com/user-attachments/assets/9955dda9-ede3-4971-8ee0-91cbc3850125"  width="400">
    </picture>
</div>

<div align="center">
<b>Local-only fork - all cloud/telemetry code removed</b>
</div>

---

<div align="center">
<a href="#demos">Demos</a> |
<a href="https://github.com/browser-use/browser-use">Upstream Repo</a>
</div>

</br>

# 👋 Quickstart (local-only fork)

**1. Clone and set up with [uv](https://docs.astral.sh/uv/) (Python>=3.11):**
```bash
uv venv --python 3.11
source .venv/bin/activate   # Windows: .venv\Scripts\activate
uv sync
uv run browser-use doctor   # optional sanity check
uv run browser-use --help   # fast CLI (default entry point)
```

**2. Set your LLM API key:**
```
# .env
OPENAI_API_KEY=your-key
# GOOGLE_API_KEY=your-key
# ANTHROPIC_API_KEY=your-key
```

**3. Run your first agent:**
```python
from browser_use import Agent, Browser, ChatOpenAI
# from browser_use import ChatGoogle  # ChatGoogle(model='gemini-3-flash-preview')
# from browser_use import ChatAnthropic  # ChatAnthropic(model='claude-sonnet-4-6')
import asyncio

async def main():
    browser = Browser()

    agent = Agent(
        task="Find the number of stars of the browser-use repo",
        llm=ChatOpenAI(model='gpt-4o'),
        # llm=ChatGoogle(model='gemini-3-flash-preview'),
        # llm=ChatAnthropic(model='claude-sonnet-4-6'),
        browser=browser,
    )
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
```

This is a **local-only fork** with all cloud/telemetry code removed.

<br/>

<br/>

# Demos


### 📋 Form-Filling
#### Task = "Fill in this job application with my resume and information."
![Job Application Demo](https://github.com/user-attachments/assets/57865ee6-6004-49d5-b2c2-6dff39ec2ba9)
[Example code ↗](https://github.com/browser-use/browser-use/blob/main/examples/use-cases/apply_to_job.py)


### 🍎 Grocery-Shopping
#### Task = "Put this list of items into my instacart."

https://github.com/user-attachments/assets/a6813fa7-4a7c-40a6-b4aa-382bf88b1850

[Example code ↗](https://github.com/browser-use/browser-use/blob/main/examples/use-cases/buy_groceries.py)


### 💻 Personal-Assistant.
#### Task = "Help me find parts for a custom PC."

https://github.com/user-attachments/assets/ac34f75c-057a-43ef-ad06-5b2c9d42bf06

[Example code ↗](https://github.com/browser-use/browser-use/blob/main/examples/use-cases/pcpartpicker.py)


### 💡See [more examples here ↗](https://docs.browser-use.com/examples) and give us a star!

<br/>

# 🚀 Template Quickstart

**Want to get started even faster?** Generate a ready-to-run template from the files shipped in the package (no network fetch):

```bash
uvx browser-use init --template default
```

`init` needs a template name. List names with `uvx browser-use init --list` (or run `init` without `--template` to print the same list and exit).

This creates a `browser_use_default.py` file with a working example. Available templates:
- `default` - Minimal setup to get started quickly
- `advanced` - All configuration options with detailed comments
- `tools` - Examples of custom tools and extending the agent

You can also specify a custom output path:
```bash
uvx browser-use init --template default --output my_agent.py
```

<br/>

# 💻 CLI

The **`browser-use`** command (also **`bu`**, **`browseruse`**, **`browser`**) is the default: a fast CLI backed by a persistent local daemon so the browser stays up between commands.

**Start using it:**
```bash
browser-use --help                      # Overview and subcommands
browser-use open https://example.com    # Navigate to URL (starts daemon if needed)
browser-use state                       # See clickable elements
browser-use click 5                     # Click element by index
browser-use type "Hello"                # Type text
browser-use screenshot page.png         # Take screenshot
browser-use close                       # Close browser
```

**MCP server (stdin/stdout JSON-RPC for tools like Claude Desktop):**
```bash
uvx browser-use --mcp
# or: browser-use --mcp
```

**Legacy full-screen TUI** (Textual UI, separate entry point): install the optional CLI extra, then run **`browser-use-tui`** instead of `browser-use`:
```bash
uv add "browser-use[cli]"    # or: pip install "browser-use[cli]"
browser-use-tui
```

See [CLI docs](browser_use/skill_cli/README.md) for all commands.

### Claude Code Skill

For [Claude Code](https://claude.ai/code), install the skill to enable AI-assisted browser automation:

```bash
mkdir -p ~/.claude/skills/browser-use
curl -o ~/.claude/skills/browser-use/SKILL.md \
  https://raw.githubusercontent.com/browser-use/browser-use/main/skills/browser-use/SKILL.md
```

<br/>

## Custom tools, MCP, and more

<br/>

# FAQ

<details>
<summary><b>What's the best model to use?</b></summary>

This fork supports any OpenAI-compatible, Google, Anthropic, or Ollama model. Choose whichever fits your use case.
</details>

<details>
<summary><b>Can I use custom tools with the agent?</b></summary>

Yes! You can add custom tools to extend the agent's capabilities:

```python
from browser_use import Tools

tools = Tools()

@tools.action(description='Description of what this tool does.')
def custom_tool(param: str) -> str:
    return f"Result: {param}"

agent = Agent(
    task="Your task",
    llm=llm,
    browser=browser,
    tools=tools,
)
```

</details>

<details>
<summary><b>Can I use this for free?</b></summary>

Yes! Browser-Use is open source and free to use. You only need to choose an LLM provider (like OpenAI, Google, Anthropic, or run local models with Ollama).
</details>

<details>
<summary><b>Terms of Service</b></summary>

This open-source library is licensed under the MIT License.
</details>

<details>
<summary><b>How do I handle authentication?</b></summary>

Check out our authentication examples:
- [Using real browser profiles](https://github.com/browser-use/browser-use/blob/main/examples/browser/real_browser.py) - Reuse your existing Chrome profile with saved logins
- If you want to use temporary accounts with inbox, choose AgentMail

These examples show how to maintain sessions and handle authentication seamlessly.
</details>

<details>
<summary><b>How do I solve CAPTCHAs?</b></summary>

CAPTCHA handling requires better browser fingerprinting and proxies. You can configure a proxy via `Browser(proxy=ProxySettings(server='...'))` and use a real Chrome profile to reduce detection.
</details>

<details>
<summary><b>How do I go into production?</b></summary>

Chrome can consume a lot of memory, and running many agents in parallel can be tricky to manage.

For production deployments, consider:
- Running browsers in Docker containers for isolation
- Using a proxy provider for stealth and geo-targeting
- Monitoring memory (Chrome is hungry) and using headless mode
- Connecting to remote browsers via `cdp_url` for scaling
</details>

<br/>

<div align="center">

**Tell your computer what to do, and it gets it done.**

<img src="https://github.com/user-attachments/assets/06fa3078-8461-4560-b434-445510c1766f" width="400"/>

[![Twitter Follow](https://img.shields.io/twitter/follow/Magnus?style=social)](https://x.com/intent/user?screen_name=mamagnus00)
&emsp;&emsp;&emsp;
[![Twitter Follow](https://img.shields.io/twitter/follow/Gregor?style=social)](https://x.com/intent/user?screen_name=gregpr07)

</div>

<div align="center"> Made with ❤️ in Zurich and San Francisco </div>
