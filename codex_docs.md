# OpenAI Codex - 全部文档

本文档整合了来自 `openai/codex` GitHub 仓库的主要文档。

---
---

# 1. README.md

[Skip to content](https://github.com/openai/codex/blob/main/README.md#start-of-content)

[openai](https://github.com/openai)/ **[codex](https://github.com/openai/codex)** Public

- [Notifications](https://github.com/login?return_to=%2Fopenai%2Fcodex) You must be signed in to change notification settings
- [Fork\
3k](https://github.com/login?return_to=%2Fopenai%2Fcodex)
- [Star\
28.4k](https://github.com/login?return_to=%2Fopenai%2Fcodex)

# OpenAI Codex CLI

Lightweight coding agent that runs in your terminal

`npm i -g @openai/codex`

[![Codex demo GIF using: codex "explain this codebase to me"](https://github.com/openai/codex/raw/main/.github/demo.gif)](https://github.com/openai/codex/blob/main/.github/demo.gif)

* * *

**Table of contents**

- [Experimental technology disclaimer](https://github.com/openai/codex/blob/main/README.md#experimental-technology-disclaimer)
- [Quickstart](https://github.com/openai/codex/blob/main/README.md#quickstart)
- [Why Codex?](https://github.com/openai/codex/blob/main/README.md#why-codex)
- [Security model & permissions](https://github.com/openai/codex/blob/main/README.md#security-model--permissions)
  - [Platform sandboxing details](https://github.com/openai/codex/blob/main/README.md#platform-sandboxing-details)
- [System requirements](https://github.com/openai/codex/blob/main/README.md#system-requirements)
- [CLI reference](https://github.com/openai/codex/blob/main/README.md#cli-reference)
- [Memory & project docs](https://github.com/openai/codex/blob/main/README.md#memory--project-docs)
- [Non-interactive / CI mode](https://github.com/openai/codex/blob/main/README.md#non-interactive--ci-mode)
- [Tracing / verbose logging](https://github.com/openai/codex/blob/main/README.md#tracing--verbose-logging)
- [Recipes](https://github.com/openai/codex/blob/main/README.md#recipes)
- [Installation](https://github.com/openai/codex/blob/main/README.md#installation)
- [Configuration guide](https://github.com/openai/codex/blob/main/README.md#configuration-guide)
  - [Basic configuration parameters](https://github.com/openai/codex/blob/main/README.md#basic-configuration-parameters)
  - [Custom AI provider configuration](https://github.com/openai/codex/blob/main/README.md#custom-ai-provider-configuration)
  - [History configuration](https://github.com/openai/codex/blob/main/README.md#history-configuration)
  - [Configuration examples](https://github.com/openai/codex/blob/main/README.md#configuration-examples)
  - [Full configuration example](https://github.com/openai/codex/blob/main/README.md#full-configuration-example)
  - [Custom instructions](https://github.com/openai/codex/blob/main/README.md#custom-instructions)
  - [Environment variables setup](https://github.com/openai/codex/blob/main/README.md#environment-variables-setup)
- [FAQ](https://github.com/openai/codex/blob/main/README.md#faq)
- [Zero data retention (ZDR) usage](https://github.com/openai/codex/blob/main/README.md#zero-data-retention-zdr-usage)
- [Codex open source fund](https://github.com/openai/codex/blob/main/README.md#codex-open-source-fund)
- [Contributing](https://github.com/openai/codex/blob/main/README.md#contributing)
  - [Development workflow](https://github.com/openai/codex/blob/main/README.md#development-workflow)
  - [Git hooks with Husky](https://github.com/openai/codex/blob/main/README.md#git-hooks-with-husky)
  - [Debugging](https://github.com/openai/codex/blob/main/README.md#debugging)
  - [Writing high-impact code changes](https://github.com/openai/codex/blob/main/README.md#writing-high-impact-code-changes)
  - [Opening a pull request](https://github.com/openai/codex/blob/main/README.md#opening-a-pull-request)
  - [Review process](https://github.com/openai/codex/blob/main/README.md#review-process)
  - [Community values](https://github.com/openai/codex/blob/main/README.md#community-values)
  - [Getting help](https://github.com/openai/codex/blob/main/README.md#getting-help)
  - [Contributor license agreement (CLA)](https://github.com/openai/codex/blob/main/README.md#contributor-license-agreement-cla)
    - [Quick fixes](https://github.com/openai/codex/blob/main/README.md#quick-fixes)
  - [Releasing `codex`](https://github.com/openai/codex/blob/main/README.md#releasing-codex)
  - [Alternative build options](https://github.com/openai/codex/blob/main/README.md#alternative-build-options)
    - [Nix flake development](https://github.com/openai/codex/blob/main/README.md#nix-flake-development)
- [Security & responsible AI](https://github.com/openai/codex/blob/main/README.md#security--responsible-ai)
- [License](https://github.com/openai/codex/blob/main/README.md#license)

* * *

## Experimental technology disclaimer

Codex CLI is an experimental project under active development. It is not yet stable, may contain bugs, incomplete features, or undergo breaking changes. We're building it in the open with the community and welcome:

- Bug reports
- Feature requests
- Pull requests
- Good vibes

Help us improve by filing issues or submitting PRs (see the section below for how to contribute)!

## Quickstart

Install globally:

`npm install -g @openai/codex`

Next, set your OpenAI API key as an environment variable:

`export OPENAI_API_KEY="your-api-key-here"`

> **Note:** This command sets the key only for your current terminal session. You can add the `export` line to your shell's configuration file (e.g., `~/.zshrc`) but we recommend setting for the session. **Tip:** You can also place your API key into a `.env` file at the root of your project:
>
> `OPENAI_API_KEY=your-api-key-here`
>
> The CLI will automatically load variables from `.env` (via `dotenv/config`).

**Use `--provider` to use other models**

> Codex also allows you to use other providers that support the OpenAI Chat Completions API. You can set the provider in the config file or use the `--provider` flag. The possible options for `--provider` are:
>
> - openai (default)
> - openrouter
> - azure
> - gemini
> - ollama
> - mistral
> - deepseek
> - xai
> - groq
> - arceeai
> - any other provider that is compatible with the OpenAI API
>
> If you use a provider other than OpenAI, you will need to set the API key for the provider in the config file or in the environment variable as:
>
> `export <provider>_API_KEY="your-api-key-here"`
>
> If you use a provider not listed above, you must also set the base URL for the provider:
>
> `export <provider>_BASE_URL="https://your-provider-api-base-url"`

Run interactively:

`codex`

Or, run with a prompt as input (and optionally in `Full Auto` mode):

`codex "explain this codebase to me"`

`codex --approval-mode full-auto "create the fanciest todo-list app"`

That's it - Codex will scaffold a file, run it inside a sandbox, install any
missing dependencies, and show you the live result. Approve the changes and
they'll be committed to your working directory.

* * *

## Why Codex?

Codex CLI is built for developers who already **live in the terminal** and want
ChatGPT-level reasoning **plus** the power to actually run code, manipulate
files, and iterate - all under version control. In short, it's _chat-driven_
_development_ that understands and executes your repo.

- **Zero setup** \- bring your OpenAI API key and it just works!
- **Full auto-approval, while safe + secure** by running network-disabled and directory-sandboxed
- **Multimodal** \- pass in screenshots or diagrams to implement features ✨

And it's **fully open-source** so you can see and contribute to how it develops!

* * *

## Security model & permissions

Codex lets you decide _how much autonomy_ the agent receives and auto-approval policy via the
`--approval-mode` flag (or the interactive onboarding prompt):

| Mode | What the agent may do without asking | Still requires approval |
| --- | --- | --- |
| **Suggest**<br>(default) | Read any file in the repo | **All** file writes/patches<br>**Any** arbitrary shell commands (aside from reading files) |
| **Auto Edit** | Read **and** apply-patch writes to files | **All** shell commands |
| **Full Auto** | Read/write files <br>Execute shell commands (network disabled, writes limited to your workdir) | - |

In **Full Auto** every command is run **network-disabled** and confined to the
current working directory (plus temporary files) for defense-in-depth. Codex
will also show a warning/confirmation if you start in **auto-edit** or
**full-auto** while the directory is _not_ tracked by Git, so you always have a
safety net.

Coming soon: you'll be able to whitelist specific commands to auto-execute with
the network enabled, once we're confident in additional safeguards.

### Platform sandboxing details

The hardening mechanism Codex uses depends on your OS:

- **macOS 12+** \- commands are wrapped with **Apple Seatbelt** ( `sandbox-exec`).
  - Everything is placed in a read-only jail except for a small set of
    writable roots ( `$PWD`, `$TMPDIR`, `~/.codex`, etc.).
  - Outbound network is _fully blocked_ by default - even if a child process
    tries to `curl` somewhere it will fail.
- **Linux** \- there is no sandboxing by default.
We recommend using Docker for sandboxing, where Codex launches itself inside a **minimal**
**container image** and mounts your repo _read/write_ at the same path. A
custom `iptables`/ `ipset` firewall script denies all egress except the
OpenAI API. This gives you deterministic, reproducible runs without needing
root on the host. You can use the [`run_in_container.sh`](https://github.com/openai/codex/blob/main/codex-cli/scripts/run_in_container.sh) script to set up the sandbox.


* * *

## System requirements

| Requirement | Details |
| --- | --- |
| Operating systems | macOS 12+, Ubuntu 20.04+/Debian 10+, or Windows 11 **via WSL2** |
| Node.js | **22 or newer** (LTS recommended) |
| Git (optional, recommended) | 2.23+ for built-in PR helpers |
| RAM | 4-GB minimum (8-GB recommended) |

> Never run `sudo npm install -g`; fix npm permissions instead.

* * *

## CLI reference

| Command | Purpose | Example |
| --- | --- | --- |
| `codex` | Interactive REPL | `codex` |
| `codex "..."` | Initial prompt for interactive REPL | `codex "fix lint errors"` |
| `codex -q "..."` | Non-interactive "quiet mode" | `codex -q --json "explain utils.ts"` |
| `codex completion <bash|zsh|fish>` | Print shell completion script | `codex completion bash` |

Key flags: `--model/-m`, `--approval-mode/-a`, `--quiet/-q`, and `--notify`.

* * *

## Memory & project docs

You can give Codex extra instructions and guidance using `AGENTS.md` files. Codex looks for `AGENTS.md` files in the following places, and merges them top-down:

1. `~/.codex/AGENTS.md` \- personal global guidance
2. `AGENTS.md` at repo root - shared project notes
3. `AGENTS.md` in the current working directory - sub-folder/feature specifics

Disable loading of these files with `--no-project-doc` or the environment variable `CODEX_DISABLE_PROJECT_DOC=1`.

* * *

## Non-interactive / CI mode

Run Codex head-less in pipelines. Example GitHub Action step:

`
- name: Update changelog via Codex
  run: |
    npm install -g @openai/codex
    export OPENAI_API_KEY="${{ secrets.OPENAI_KEY }}"
    codex -a auto-edit --quiet "update CHANGELOG for next release"
`

Set `CODEX_QUIET_MODE=1` to silence interactive UI noise.

## Tracing / verbose logging

Setting the environment variable `DEBUG=true` prints full API request and response details:

`DEBUG=true codex`

* * *

## Recipes

Below are a few bite-size examples you can copy-paste. Replace the text in quotes with your own task. See the [prompting guide](https://github.com/openai/codex/blob/main/codex-cli/examples/prompting_guide.md) for more tips and usage patterns.

| ✨ | What you type | What happens |
| --- | --- | --- |
| 1 | `codex "Refactor the Dashboard component to React Hooks"` | Codex rewrites the class component, runs `npm test`, and shows the diff. |
| 2 | `codex "Generate SQL migrations for adding a users table"` | Infers your ORM, creates migration files, and runs them in a sandboxed DB. |
| 3 | `codex "Write unit tests for utils/date.ts"` | Generates tests, executes them, and iterates until they pass. |
| 4 | `codex "Bulk-rename *.jpeg -> *.jpg with git mv"` | Safely renames files and updates imports/usages. |
| 5 | `codex "Explain what this regex does: ^(?=.*[A-Z]).{8,}$"` | Outputs a step-by-step human explanation. |
| 6 | `codex "Carefully review this repo, and propose 3 high impact well-scoped PRs"` | Suggests impactful PRs in the current codebase. |
| 7 | `codex "Look for vulnerabilities and create a security review report"` | Finds and explains security bugs. |

* * *

## Installation

**From npm (Recommended)**

`
npm install -g @openai/codex
# or
yarn global add @openai/codex
# or
bun install -g @openai/codex
# or
pnpm add -g @openai/codex
`

**Build from source**

`
# Clone the repository and navigate to the CLI package
git clone https://github.com/openai/codex.git
cd codex/codex-cli

# Enable corepack
corepack enable

# Install dependencies and build
pnpm install
pnpm build

# Linux-only: download prebuilt sandboxing binaries (requires gh and zstd).
./scripts/install_native_deps.sh

# Get the usage and the options
node ./dist/cli.js --help

# Run the locally-built CLI directly
node ./dist/cli.js

# Or link the command globally for convenience
pnpm link
`

* * *

## Configuration guide

Codex configuration files can be placed in the `~/.codex/` directory, supporting both YAML and JSON formats.

### Basic configuration parameters

| Parameter | Type | Default | Description | Available Options |
| --- | --- | --- | --- | --- |
| `model` | string | `o4-mini` | AI model to use | Any model name supporting OpenAI API |
| `approvalMode` | string | `suggest` | AI assistant's permission mode | `suggest` (suggestions only)<br>`auto-edit` (automatic edits)<br>`full-auto` (fully automatic) |
| `fullAutoErrorMode` | string | `ask-user` | Error handling in full-auto mode | `ask-user` (prompt for user input)<br>`ignore-and-continue` (ignore and proceed) |
| `notify` | boolean | `true` | Enable desktop notifications | `true`/ `false` |

### Custom AI provider configuration

In the `providers` object, you can configure multiple AI service providers. Each provider requires the following parameters:

| Parameter | Type | Description | Example |
| --- | --- | --- | --- |
| `name` | string | Display name of the provider | `"OpenAI"` |
| `baseURL` | string | API service URL | `"https://api.openai.com/v1"` |
| `envKey` | string | Environment variable name (for API key) | `"OPENAI_API_KEY"` |

### History configuration

In the `history` object, you can configure conversation history settings:

| Parameter | Type | Description | Example Value |
| --- | --- | --- | --- |
| `maxSize` | number | Maximum number of history entries to save | `1000` |
| `saveHistory` | boolean | Whether to save history | `true` |
| `sensitivePatterns` | array | Patterns of sensitive information to filter in history | `[]` |

### Configuration examples

1. YAML format (save as `~/.codex/config.yaml`):

`
model: o4-mini
approvalMode: suggest
fullAutoErrorMode: ask-user
notify: true
`

2. JSON format (save as `~/.codex/config.json`):

`
{
  "model": "o4-mini",
  "approvalMode": "suggest",
  "fullAutoErrorMode": "ask-user",
  "notify": true
}
`

### Full configuration example

Below is a comprehensive example of `config.json` with multiple custom providers:

`
{
  "model": "o4-mini",
  "provider": "openai",
  "providers": {
    "openai": {
      "name": "OpenAI",
      "baseURL": "https://api.openai.com/v1",
      "envKey": "OPENAI_API_KEY"
    },
    "azure": {
      "name": "AzureOpenAI",
      "baseURL": "https://YOUR_PROJECT_NAME.openai.azure.com/openai",
      "envKey": "AZURE_OPENAI_API_KEY"
    },
    "openrouter": {
      "name": "OpenRouter",
      "baseURL": "https://openrouter.ai/api/v1",
      "envKey": "OPENROUTER_API_KEY"
    },
    "gemini": {
      "name": "Gemini",
      "baseURL": "https://generativelanguage.googleapis.com/v1beta/openai",
      "envKey": "GEMINI_API_KEY"
    },
    "ollama": {
      "name": "Ollama",
      "baseURL": "http://localhost:11434/v1",
      "envKey": "OLLAMA_API_KEY"
    },
    "mistral": {
      "name": "Mistral",
      "baseURL": "https://api.mistral.ai/v1",
      "envKey": "MISTRAL_API_KEY"
    },
    "deepseek": {
      "name": "DeepSeek",
      "baseURL": "https://api.deepseek.com",
      "envKey": "DEEPSEEK_API_KEY"
    },
    "xai": {
      "name": "xAI",
      "baseURL": "https://api.x.ai/v1",
      "envKey": "XAI_API_KEY"
    },
    "groq": {
      "name": "Groq",
      "baseURL": "https://api.groq.com/openai/v1",
      "envKey": "GROQ_API_KEY"
    },
    "arceeai": {
      "name": "ArceeAI",
      "baseURL": "https://conductor.arcee.ai/v1",
      "envKey": "ARCEEAI_API_KEY"
    }
  },
  "history": {
    "maxSize": 1000,
    "saveHistory": true,
    "sensitivePatterns": []
  }
}
`

### Custom instructions

You can create a `~/.codex/AGENTS.md` file to define custom guidance for the agent:

`
- Always respond with emojis
- Only use git commands when explicitly requested
`

### Environment variables setup

For each AI provider, you need to set the corresponding API key in your environment variables. For example:

`
# OpenAI
export OPENAI_API_KEY="your-api-key-here"

# Azure OpenAI
export AZURE_OPENAI_API_KEY="your-azure-api-key-here"
export AZURE_OPENAI_API_VERSION="2025-03-01-preview" (Optional)

# OpenRouter
export OPENROUTER_API_KEY="your-openrouter-key-here"

# Similarly for other providers
`

* * *

## FAQ

OpenAI released a model called Codex in 2021 - is this related?

In 2021, OpenAI released Codex, an AI system designed to generate code from natural language prompts. That original Codex model was deprecated as of March 2023 and is separate from the CLI tool.

Which models are supported?

Any model available with [Responses API](https://platform.openai.com/docs/api-reference/responses). The default is `o4-mini`, but pass `--model gpt-4.1` or set `model: gpt-4.1` in your config file to override.

Why does `o3` or `o4-mini` not work for me?

It's possible that your [API account needs to be verified](https://help.openai.com/en/articles/10910291-api-organization-verification) in order to start streaming responses and seeing chain of thought summaries from the API. If you're still running into issues, please let us know!

How do I stop Codex from editing my files?

Codex runs model-generated commands in a sandbox. If a proposed command or file change doesn't look right, you can simply type **n** to deny the command or give the model feedback.

Does it work on Windows?

Not directly. It requires [Windows Subsystem for Linux (WSL2)](https://learn.microsoft.com/en-us/windows/wsl/install) \- Codex has been tested on macOS and Linux with Node 22.

* * *

## Zero data retention (ZDR) usage

Codex CLI **does** support OpenAI organizations with [Zero Data Retention (ZDR)](https://platform.openai.com/docs/guides/your-data#zero-data-retention) enabled. If your OpenAI organization has Zero Data Retention enabled and you still encounter errors such as:

`
OpenAI rejected the request. Error details: Status: 400, Code: unsupported_parameter, Type: invalid_request_error, Message: 400 Previous response cannot be used for this organization due to Zero Data Retention.
`

You may need to upgrade to a more recent version with: `npm i -g @openai/codex@latest`

* * *

## Codex open source fund

We're excited to launch a **$1 million initiative** supporting open source projects that use Codex CLI and other OpenAI models.

- Grants are awarded up to **$25,000** API credits.
- Applications are reviewed **on a rolling basis**.

**Interested? [Apply here](https://openai.com/form/codex-open-source-fund/).**

* * *

## Contributing

This project is under active development and the code will likely change pretty significantly. We'll update this message once that's complete!

More broadly we welcome contributions - whether you are opening your very first pull request or you're a seasoned maintainer. At the same time we care about reliability and long-term maintainability, so the bar for merging code is intentionally **high**. The guidelines below spell out what "high-quality" means in practice and should make the whole process transparent and friendly.

### Development workflow

- Create a _topic branch_ from `main` \- e.g. `feat/interactive-prompt`.
- Keep your changes focused. Multiple unrelated fixes should be opened as separate PRs.
- Use `pnpm test:watch` during development for super-fast feedback.
- We use **Vitest** for unit tests, **ESLint** \+ **Prettier** for style, and **TypeScript** for type-checking.
- Before pushing, run the full test/type/lint suite:

### Git hooks with Husky

This project uses [Husky](https://typicode.github.io/husky/) to enforce code quality checks:

- **Pre-commit hook**: Automatically runs lint-staged to format and lint files before committing
- **Pre-push hook**: Runs tests and type checking before pushing to the remote

These hooks help maintain code quality and prevent pushing code with failing tests. For more details, see [HUSKY.md](https://github.com/openai/codex/blob/main/codex-cli/HUSKY.md).

`pnpm test && pnpm run lint && pnpm run typecheck`

- If you have **not** yet signed the Contributor License Agreement (CLA), add a PR comment containing the exact text

`I have read the CLA Document and I hereby sign the CLA`

The CLA-Assistant bot will turn the PR status green once all authors have signed.

`
# Watch mode (tests rerun on change)
pnpm test:watch

# Type-check without emitting files
pnpm typecheck

# Automatically fix lint + prettier issues
pnpm lint:fix
pnpm format:fix
`

### Debugging

To debug the CLI with a visual debugger, do the following in the `codex-cli` folder:

- Run `pnpm run build` to build the CLI, which will generate `cli.js.map` alongside `cli.js` in the `dist` folder.
- Run the CLI with `node --inspect-brk ./dist/cli.js` The program then waits until a debugger is attached before proceeding. Options:

  - In VS Code, choose **Debug: Attach to Node Process** from the command palette and choose the option in the dropdown with debug port `9229` (likely the first option)
  - Go to chrome://inspect in Chrome and find **localhost:9229** and click **trace**

### Writing high-impact code changes

1. **Start with an issue.** Open a new one or comment on an existing discussion so we can agree on the solution before code is written.
2. **Add or update tests.** Every new feature or bug-fix should come with test coverage that fails before your change and passes afterwards. 100% coverage is not required, but aim for meaningful assertions.
3. **Document behaviour.** If your change affects user-facing behaviour, update the README, inline help ( `codex --help`), or relevant example projects.
4. **Keep commits atomic.** Each commit should compile and the tests should pass. This makes reviews and potential rollbacks easier.

### Opening a pull request

- Fill in the PR template (or include similar information) - **What? Why? How?**
- Run **all** checks locally ( `npm test && npm run lint && npm run typecheck`). CI failures that could have been caught locally slow down the process.
- Make sure your branch is up-to-date with `main` and that you have resolved merge conflicts.
- Mark the PR as **Ready for review** only when you believe it is in a merge-able state.

### Review process

1. One maintainer will be assigned as a primary reviewer.
2. We may ask for changes - please do not take this personally. We value the work, we just also value consistency and long-term maintainability.
3. When there is consensus that the PR meets the bar, a maintainer will squash-and-merge.

### Community values

- **Be kind and inclusive.** Treat others with respect; we follow the [Contributor Covenant](https://www.contributor-covenant.org/).
- **Assume good intent.** Written communication is hard - err on the side of generosity.
- **Teach & learn.** If you spot something confusing, open an issue or PR with improvements.

### Getting help

If you run into problems setting up the project, would like feedback on an idea, or just want to say _hi_ \- please open a Discussion or jump into the relevant issue. We are happy to help.

Together we can make Codex CLI an incredible tool. **Happy hacking!** 🚀

### Contributor license agreement (CLA)

All contributors **must** accept the CLA. The process is lightweight:

1. Open your pull request.

2. Paste the following comment (or reply `recheck` if you've signed before):

`I have read the CLA Document and I hereby sign the CLA`

3. The CLA-Assistant bot records your signature in the repo and marks the status check as passed.

No special Git commands, email attachments, or commit footers required.

#### Quick fixes

| Scenario | Command |
| --- | --- |
| Amend last commit | `git commit --amend -s --no-edit && git push -f` |

The **DCO check** blocks merges until every commit in the PR carries the footer (with squash this is just the one).

### Releasing `codex`

To publish a new version of the CLI you first need to stage the npm package. A
helper script in `codex-cli/scripts/` does all the heavy lifting. Inside the
`codex-cli` folder run:

`
# Classic, JS implementation that includes small, native binaries for Linux sandboxing.
pnpm stage-release

# Optionally specify the temp directory to reuse between runs.
RELEASE_DIR=$(mktemp -d)
pnpm stage-release --tmp "$RELEASE_DIR"

# "Fat" package that additionally bundles the native Rust CLI binaries for
# Linux. End-users can then opt-in at runtime by setting CODEX_RUST=1.
pnpm stage-release --native
`

Go to the folder where the release is staged and verify that it works as intended. If so, run the following from the temp folder:

`
cd "$RELEASE_DIR"
npm publish
`

### Alternative build options

#### Nix flake development

Prerequisite: Nix >= 2.4 with flakes enabled ( `experimental-features = nix-command flakes` in `~/.config/nix/nix.conf`).

Enter a Nix development shell:

`
# Use either one of the commands according to which implementation you want to work with
nix develop .#codex-cli # For entering codex-cli specific shell
nix develop .#codex-rs # For entering codex-rs specific shell
`

This shell includes Node.js, installs dependencies, builds the CLI, and provides a `codex` command alias.

Build and run the CLI directly:

`
# Use either one of the commands according to which implementation you want to work with
nix build .#codex-cli # For building codex-cli
nix build .#codex-rs # For building codex-rs
./result/bin/codex --help
`

Run the CLI via the flake app:

`
# Use either one of the commands according to which implementation you want to work with
nix run .#codex-cli # For running codex-cli
nix run .#codex-rs # For running codex-rs
`

Use direnv with flakes

If you have direnv installed, you can use the following `.envrc` to automatically enter the Nix shell when you `cd` into the project directory:

`
cd codex-rs
echo "use flake ../flake.nix#codex-cli" >> .envrc && direnv allow
cd codex-cli
echo "use flake ../flake.nix#codex-rs" >> .envrc && direnv allow
`

* * *

## Security & responsible AI

Have you discovered a vulnerability or have concerns about model output? Please e-mail **[security@openai.com](mailto:security@openai.com)** and we will respond promptly.

* * *

## License

This repository is licensed under the [Apache-2.0 License](https://github.com/openai/codex/blob/main/LICENSE).

---
---

# 2. AGENTS.md

[openai](https://github.com/openai)/ **[codex](https://github.com/openai/codex)** Public

- [Notifications](https://github.com/login?return_to=%2Fopenai%2Fcodex) You must be signed in to change notification settings
- [Fork\
3k](https://github.com/login?return_to=%2Fopenai%2Fcodex)
- [Star\
28.4k](https://github.com/login?return_to=%2Fopenai%2Fcodex)

# Rust/codex-rs

In the codex-rs folder where the rust code lives:

- Never add or modify any code related to `CODEX_SANDBOX_NETWORK_DISABLED_ENV_VAR`. You operate in a sandbox where `CODEX_SANDBOX_NETWORK_DISABLED=1` will be set whenever you use the `shell` tool. Any existing code that uses `CODEX_SANDBOX_NETWORK_DISABLED_ENV_VAR` was authored with this fact in mind. It is often used to early exit out of tests that the author knew you would not be able to run given your sandbox limitations.

---
---

# 3. CHANGELOG.md

[openai](https://github.com/openai)/ **[codex](https://github.com/openai/codex)** Public

- [Notifications](https://github.com/login?return_to=%2Fopenai%2Fcodex) You must be signed in to change notification settings
- [Fork\
3k](https://github.com/login?return_to=%2Fopenai%2Fcodex)
- [Star\
28.4k](https://github.com/login?return_to=%2Fopenai%2Fcodex)

# Changelog

You can install any of these versions: `npm install -g codex@version`

## `0.1.2505172129`

### 🪲 Bug Fixes

- Add node version check (#1007)
- Persist token after refresh (#1006)

## `0.1.2505171619`

- `codex --login` \+ `codex --free` (#998)

## `0.1.2505161800`

- Sign in with chatgpt credits (#974)
- Add support for OpenAI tool type, local\_shell (#961)

## `0.1.2505161243`

- Sign in with chatgpt (#963)
- Session history viewer (#912)
- Apply patch issue when using different cwd (#942)
- Diff command for filenames with special characters (#954)

## `0.1.2505160811`

- `codex-mini-latest` (#951)

## `0.1.2505140839`

### 🪲 Bug Fixes

- Gpt-4.1 apply\_patch handling (#930)
- Add support for fileOpener in config.json (#911)
- Patch in #366 and #367 for marked-terminal (#916)
- Remember to set lastIndex = 0 on shared RegExp (#918)
- Always load version from package.json at runtime (#909)
- Tweak the label for citations for better rendering (#919)
- Tighten up some logic around session timestamps and ids (#922)
- Change EventMsg enum so every variant takes a single struct (#925)
- Reasoning default to medium, show workdir when supplied (#931)
- Test\_dev\_null\_write() was not using echo as intended (#923)

## `0.1.2504301751`

### 🚀 Features

- User config api key (#569)
- `@mention` files in codex (#701)
- Add `--reasoning` CLI flag (#314)
- Lower default retry wait time and increase number of tries (#720)
- Add common package registries domains to allowed-domains list (#414)

### 🪲 Bug Fixes

- Insufficient quota message (#758)
- Input keyboard shortcut opt+delete (#685)
- `/diff` should include untracked files (#686)
- Only allow running without sandbox if explicitly marked in safe container (#699)
- Tighten up check for /usr/bin/sandbox-exec (#710)
- Check if sandbox-exec is available (#696)
- Duplicate messages in quiet mode (#680)

## `0.1.2504251709`

### 🚀 Features

- Add openai model info configuration (#551)
- Added provider to run quiet mode function (#571)
- Create parent directories when creating new files (#552)
- Print bug report URL in terminal instead of opening browser (#510) (#528)
- Add support for custom provider configuration in the user config (#537)
- Add support for OpenAI-Organization and OpenAI-Project headers (#626)
- Add specific instructions for creating API keys in error msg (#581)
- Enhance toCodePoints to prevent potential unicode 14 errors (#615)
- More native keyboard navigation in multiline editor (#655)
- Display error on selection of invalid model (#594)

### 🪲 Bug Fixes

- Model selection (#643)
- Nits in apply patch (#640)
- Input keyboard shortcuts (#676)
- `apply_patch` unicode characters (#625)
- Don't clear turn input before retries (#611)
- More loosely match context for apply\_patch (#610)
- Update bug report template - there is no --revision flag (#614)
- Remove outdated copy of text input and external editor feature (#670)
- Remove unreachable "disableResponseStorage" logic flow introduced in #543 (#573)
- Non-openai mode - fix for gemini content: null, fix 429 to throw before stream (#563)
- Only allow going up in history when not already in history if input is empty (#654)
- Do not grant "node" user sudo access when using run\_in\_container.sh (#627)
- Update scripts/build\_container.sh to use pnpm instead of npm (#631)
- Update lint-staged config to use pnpm --filter (#582)
- Non-openai mode - don't default temp and top\_p (#572)
- Fix error catching when checking for updates (#597)
- Close stdin when running an exec tool call (#636)

## `0.1.2504221401`

### 🚀 Features

- Show actionable errors when api keys are missing (#523)
- Add CLI `--version` flag (#492)

### 🪲 Bug Fixes

- Agent loop for ZDR ( `disableResponseStorage`) (#543)
- Fix relative `workdir` check for `apply_patch` (#556)
- Minimal mid-stream #429 retry loop using existing back-off (#506)
- Inconsistent usage of base URL and API key (#507)
- Remove requirement for api key for ollama (#546)
- Support `[provider]_BASE_URL` (#542)

## `0.1.2504220136`

### 🚀 Features

- Add support for ZDR orgs (#481)
- Include fractional portion of chunk that exceeds stdout/stderr limit (#497)

## `0.1.2504211509`

### 🚀 Features

- Support multiple providers via Responses-Completion transformation (#247)
- Add user-defined safe commands configuration and approval logic #380 (#386)
- Allow switching approval modes when prompted to approve an edit/command (#400)
- Add support for `/diff` command autocomplete in TerminalChatInput (#431)
- Auto-open model selector if user selects deprecated model (#427)
- Read approvalMode from config file (#298)
- `/diff` command to view git diff (#426)
- Tab completions for file paths (#279)
- Add /command autocomplete (#317)
- Allow multi-line input (#438)

### 🪲 Bug Fixes

- `full-auto` support in quiet mode (#374)
- Enable shell option for child process execution (#391)
- Configure husky and lint-staged for pnpm monorepo (#384)
- Command pipe execution by improving shell detection (#437)
- Name of the file not matching the name of the component (#354)
- Allow proper exit from new Switch approval mode dialog (#453)
- Ensure /clear resets context and exclude system messages from approximateTokenUsed count (#443)
- `/clear` now clears terminal screen and resets context left indicator (#425)
- Correct fish completion function name in CLI script (#485)
- Auto-open model-selector when model is not found (#448)
- Remove unnecessary isLoggingEnabled() checks (#420)
- Improve test reliability for `raw-exec` (#434)
- Unintended tear down of agent loop (#483)
- Remove extraneous type casts (#462)

## `0.1.2504181820`

### 🚀 Features

- Add `/bug` report command (#312)
- Notify when a newer version is available (#333)

### 🪲 Bug Fixes

- Update context left display logic in TerminalChatInput component (#307)
- Improper spawn of sh on Windows Powershell (#318)
- `/bug` report command, thinking indicator (#381)
- Include pnpm lock file (#377)

## `0.1.2504172351`

### 🚀 Features

- Add Nix flake for reproducible development environments (#225)

### 🪲 Bug Fixes

- Handle invalid commands (#304)
- Raw-exec-process-group.test improve reliability and error handling (#280)
- Canonicalize the writeable paths used in seatbelt policy (#275)

## `0.1.2504172304`

### 🚀 Features

- Add shell completion subcommand (#138)
- Add command history persistence (#152)
- Shell command explanation option (#173)
- Support bun fallback runtime for codex CLI (#282)
- Add notifications for MacOS using Applescript (#160)
- Enhance image path detection in input processing (#189)
- `--config`/ `-c` flag to open global instructions in nvim (#158)
- Update position of cursor when navigating input history with arrow keys to the end of the text (#255)

### 🪲 Bug Fixes

- Correct word deletion logic for trailing spaces (Ctrl+Backspace) (#131)
- Improve Windows compatibility for CLI commands and sandbox (#261)
- Correct typos in thinking texts (transcendent & parroting) (#108)
- Add empty vite config file to prevent resolving to parent (#273)
- Update regex to better match the retry error messages (#266)
- Add missing "as" in prompt prefix in agent loop (#186)
- Allow continuing after interrupting assistant (#178)
- Standardize filename to kebab-case 🐍➡️🥙 (#302)
- Small update to bug report template (#288)
- Duplicated message on model change (#276)
- Typos in prompts and comments (#195)
- Check workdir before spawn (#221)

---
---

# 4. PNPM.md

[openai](https://github.com/openai)/ **[codex](https://github.com/openai/codex)** Public

- [Notifications](https://github.com/login?return_to=%2Fopenai%2Fcodex) You must be signed in to change notification settings
- [Fork\
3k](https://github.com/login?return_to=%2Fopenai%2Fcodex)
- [Star\
28.4k](https://github.com/login?return_to=%2Fopenai%2Fcodex)

# Migration to pnpm

This project has been migrated from npm to pnpm to improve dependency management and developer experience.

## Why pnpm?

- **Faster installation**: pnpm is significantly faster than npm and yarn
- **Disk space savings**: pnpm uses a content-addressable store to avoid duplication
- **Phantom dependency prevention**: pnpm creates a strict node\_modules structure
- **Native workspaces support**: simplified monorepo management

## How to use pnpm

### Installation

`
# Global installation of pnpm
npm install -g pnpm@10.8.1

# Or with corepack (available with Node.js 22+)
corepack enable
corepack prepare pnpm@10.8.1 --activate
`

### Common commands

| npm command | pnpm equivalent |
| --- | --- |
| `npm install` | `pnpm install` |
| `npm run build` | `pnpm run build` |
| `npm test` | `pnpm test` |
| `npm run lint` | `pnpm run lint` |

### Workspace-specific commands

| Action | Command |
| --- | --- |
| Run a command in a specific package | `pnpm --filter @openai/codex run build` |
| Install a dependency in a specific package | `pnpm --filter @openai/codex add lodash` |
| Run a command in all packages | `pnpm -r run test` |

## Monorepo structure

`
codex/
├── pnpm-workspace.yaml    # Workspace configuration
├── .npmrc                 # pnpm configuration
├── package.json           # Root dependencies and scripts
├── codex-cli/             # Main package
│   └── package.json       # codex-cli specific dependencies
└── docs/                  # Documentation (future package)
`

## Configuration files

- **pnpm-workspace.yaml**: Defines the packages included in the monorepo
- **.npmrc**: Configures pnpm behavior
- **Root package.json**: Contains shared scripts and dependencies

## CI/CD

CI/CD workflows have been updated to use pnpm instead of npm. Make sure your CI environments use pnpm 10.8.1 or higher.

## Known issues

If you encounter issues with pnpm, try the following solutions:

1. Remove the `node_modules` folder and `pnpm-lock.yaml` file, then run `pnpm install`
2. Make sure you're using pnpm 10.8.1 or higher
3. Verify that Node.js 22 or higher is installed

---
---

# 5. docs/CLA.md

[openai](https://github.com/openai)/ **[codex](https://github.com/openai/codex)** Public

- [Notifications](https://github.com/login?return_to=%2Fopenai%2Fcodex) You must be signed in to change notification settings
- [Fork\
3k](https://github.com/login?return_to=%2Fopenai%2Fcodex)
- [Star\
28.4k](https://github.com/login?return_to=%2Fopenai%2Fcodex)

# Individual Contributor License Agreement (v1.0, OpenAI)

_Based on the Apache Software Foundation Individual CLA v 2.2._

By commenting **"I have read the CLA Document and I hereby sign the CLA"**
on a Pull Request, **you (“Contributor”) agree to the following terms** for any
past and future "Contributions" submitted to the **OpenAI Codex CLI project**
**(the "Project")**.

* * *

## 1. Definitions

- **"Contribution"** – any original work of authorship submitted to the Project
(code, documentation, designs, etc.).
- **"You" / "Your"** – the individual (or legal entity) posting the acceptance
comment.

## 2. Copyright License

You grant **OpenAI, Inc.** and all recipients of software distributed by the
Project a perpetual, worldwide, non‑exclusive, royalty‑free, irrevocable
license to reproduce, prepare derivative works of, publicly display, publicly
perform, sublicense, and distribute Your Contributions and derivative works.

## 3. Patent License

You grant **OpenAI, Inc.** and all recipients of the Project a perpetual,
worldwide, non‑exclusive, royalty‑free, irrevocable (except as below) patent
license to make, have made, use, sell, offer to sell, import, and otherwise
transfer Your Contributions alone or in combination with the Project.

If any entity brings patent litigation alleging that the Project or a
Contribution infringes a patent, the patent licenses granted by You to that
entity under this CLA terminate.

## 4. Representations

1. You are legally entitled to grant the licenses above.
2. Each Contribution is either Your original creation or You have authority to
submit it under this CLA.
3. Your Contributions are provided **"AS IS"** without warranties of any kind.
4. You will notify the Project if any statement above becomes inaccurate.

## 5. Miscellany

This Agreement is governed by the laws of the **State of California**, USA,
excluding its conflict‑of‑laws rules. If any provision is held unenforceable,
the remaining provisions remain in force. 