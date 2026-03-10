## Local AI Agent

Website URL: https://deepsync.streamlit.app/

This project is a **local, privacy-friendly AI helper** that lets you control your machine using **natural language**, through both **text and voice**.

It is designed to be:

- **Local-first**: all logic runs on your machine.
- **Practical**: focused on everyday helper tasks (open folders, search web, list files, run commands).
- **Transparent**: every action is logged with the exact command that was executed.

---

### Main Features

- **GUI desktop app**
  - Conversation history (user, assistant, and system messages).
  - Separate command log that shows **every shell command** the helper runs.
  - Toggle to **enable/disable shell execution** at any time.

- **Natural language commands**
  - Examples:
    - `open browser`
    - `search for python decorators`
    - `list files`
    - `run git status`
  - The agent interprets your request, decides which tool to use, and then runs a concrete command when allowed.

- **Voice support**
  - Optional **speech recognition** (convert voice → text).
  - Optional **text-to-speech** (assistant responses spoken aloud).
  - Non‑blocking background listener with safe error handling.

---

### Project Structure

- `gui_app.py`  
  The main Tkinter application:
  - Builds the window layout: conversation pane, command log pane, input bar.
  - Wires together the `LocalHelperAgent` and `VoiceModule`.
  - Keeps the UI responsive by running agent work on background threads.
  - Shows a live list of all executed commands with timestamps and success status.

- `agent.py`  
  The “brain” of the helper:
  - `LocalHelperAgent`:
    - Accepts natural language text via `handle_request(text)`.
    - Routes the text to simple tools (open browser, web search, list files, run shell).
    - Translates each request into a concrete shell command when appropriate.
    - Runs the command (if allowed) and returns a user‑friendly result string.
  - `AgentConfig`:
    - `shell`: which shell to use (powershell on Windows, bash otherwise).
    - `allow_shell_commands`: global flag to enable/disable execution.
    - `working_directory`: where shell commands are run.
  - Command logging:
    - Each request produces a `CommandLogEntry` with:
      - timestamp
      - natural language input
      - exact command
      - result text
      - success flag

- `voice_module.py`  
  A robust wrapper around optional voice libraries:
  - `VoiceModule`:
    - Background listening via callbacks (no blocking on the main thread).
    - Optional speech recognition using `speech_recognition`.
    - Optional text‑to‑speech using `pyttsx3`.
    - Gracefully degrades to a text‑only experience if audio dependencies or devices are missing.
  - `VoiceConfig`:
    - Enable/disable input and output.
    - Language (e.g. `en-US`).
    - Ambient noise adjustment time and phrase timeout.

---

### Installation

1. **Clone or copy** this project into a folder, then open a terminal in that folder.

2. (Recommended) Create and activate a virtual environment:

```bash
python -m venv .venv
.\.venv\Scripts\activate  # on Windows (PowerShell)
# source .venv/bin/activate  # on macOS / Linux
```

3. **Install Python dependencies** (voice is optional but recommended):

```bash
pip install speechrecognition pyttsx3 pyaudio
```

If `pyaudio` is difficult to install on your platform, you can:

- Skip it and use the app in **text-only mode**, or
- Install a precompiled wheel for your OS and Python version.

---

### Running the App

From the project folder:

```bash
python gui_app.py
```

You should see a window titled **“Local AI Helper”** with:

- Left: conversation history.
- Right: executed command log.
- Bottom: input bar + `Send` button + `Start Voice` button + shell toggle.

---

### Using the Helper

- **Text input**
  - Type into the bottom input field and press **Enter** or click **Send**.
  - Example prompts:
    - `open browser`
    - `search for how to use git cherry-pick`
    - `list files`
    - `run git status`

- **Voice input**
  - Click **“Start Voice”** to begin listening.
  - Speak a command: “search for Python list comprehension”.
  - The recognized text appears as `user (voice)` in the conversation.
  - Click **“Stop Voice”** to stop listening.

- **Shell execution safety**
  - The **“Allow shell execution”** checkbox controls whether commands are actually run.
  - When disabled:
    - The agent still interprets your request.
    - It shows **what it would run**, but does **not** execute the command.

- **Command log**
  - The right panel shows:
    - Time, status (`OK` / `ERR`), and the exact command executed.
    - The natural language that produced that command.
  - This gives you full visibility into what the helper is doing.

---

### Extending the Helper

To add new capabilities:

1. Open `agent.py`.
2. In `_route`, add conditions that detect your new intent from natural language.
3. Implement a new `_tool_*` method that:
   - Accepts the original text.
   - Returns `(description, shell_command_or_None)`.
4. The GUI will automatically:
   - Show the new command in the command log.
   - Display the result in the conversation pane.

You can also evolve `voice_module.py` to use different TTS engines or recognition services as long as you keep the same `VoiceModule` interface.

---

### Notes

- This project is intentionally **simple and explicit**:
  - No background network calls.
  - No external remote AI services.
  - Clear separation between GUI, agent logic, and voice handling.
- It is a solid base for a more advanced local assistant if you want to:
  - Plug in an on‑device LLM.
  - Add custom workflows (e.g. coding helpers, project‑specific scripts).
  - Persist command history to disk.

