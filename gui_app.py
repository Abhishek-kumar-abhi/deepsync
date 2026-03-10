import threading
import tkinter as tk
from tkinter import scrolledtext, ttk
from typing import Optional

from ttkthemes import ThemedTk

from agent import AgentConfig, LocalHelperAgent
from voice_module import VoiceConfig, VoiceModule


class LocalHelperGUI(ThemedTk):
    """
    A small production-ready desktop UI for the local helper.

    Key characteristics:
    - Text and voice input
    - Scrollable conversation pane
    - Dedicated pane showing every concrete command that was run
    - Safe-by-default; you can disable shell execution from the UI
    """

    def __init__(self) -> None:
        super().__init__()
        self.set_theme("black")
        self.title("DeepSync: Local AI Agent")
        self.geometry("1000x650")

        # Core components
        self.agent = LocalHelperAgent(AgentConfig())
        self.voice = VoiceModule(VoiceConfig())

        self._build_ui()
        self._setup_voice()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _build_ui(self) -> None:
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        # Conversation panel
        convo_frame = ttk.LabelFrame(self, text="Conversation")
        convo_frame.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")
        convo_frame.rowconfigure(0, weight=1)
        convo_frame.columnconfigure(0, weight=1)

        self.conversation = scrolledtext.ScrolledText(
            convo_frame,
            state="disabled",
            wrap=tk.WORD,
            font=("Consolas", 10),
        )
        self.conversation.grid(row=0, column=0, sticky="nsew")

        # Command log panel
        cmd_frame = ttk.LabelFrame(self, text="Executed commands")
        cmd_frame.grid(row=0, column=1, padx=8, pady=8, sticky="nsew")
        cmd_frame.rowconfigure(0, weight=1)
        cmd_frame.columnconfigure(0, weight=1)

        self.command_log = scrolledtext.ScrolledText(
            cmd_frame,
            state="disabled",
            wrap=tk.NONE,
            font=("Consolas", 9),
        )
        self.command_log.grid(row=0, column=0, sticky="nsew")

        # Button panel
        button_frame = ttk.Frame(self)
        button_frame.grid(row=1, column=1, padx=8, pady=(0, 8), sticky="ew")
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)

        copy_log_btn = ttk.Button(button_frame, text="Copy Log", command=self._copy_log_to_clipboard)
        copy_log_btn.grid(row=0, column=0, padx=(0, 4), sticky="ew")

        clear_convo_btn = ttk.Button(button_frame, text="Clear Conversation", command=self._clear_conversation)
        clear_convo_btn.grid(row=0, column=1, padx=(0, 4), sticky="ew")

        

        # Input area
        input_frame = ttk.Frame(self)
        input_frame.grid(row=1, column=0, padx=8, pady=(0, 8), sticky="ew")
        input_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=0)
        input_frame.columnconfigure(2, weight=0)
        input_frame.columnconfigure(3, weight=0)
        input_frame.columnconfigure(4, weight=0)

        self.input_var = tk.StringVar()
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_var)
        self.input_entry.grid(row=0, column=0, padx=(0, 8), sticky="ew")
        self.input_entry.bind("<Return>", self._on_send)

        send_btn = ttk.Button(input_frame, text="Send", command=self._on_send)
        send_btn.grid(row=0, column=1, padx=(0, 4))

        self.voice_button = ttk.Button(
            input_frame,
            text="Start Voice",
            command=self._toggle_voice,
        )
        self.voice_button.grid(row=0, column=2, padx=(0, 4))

        self.shell_enabled = tk.BooleanVar(value=self.agent.config.allow_shell_commands)
        shell_check = ttk.Checkbutton(
            input_frame,
            text="Allow shell execution",
            variable=self.shell_enabled,
            command=self._on_shell_toggle,
        )
        shell_check.grid(row=0, column=3, padx=(0, 4))

        

        # Initial message
        self._append_conversation(
            "system",
            "Local helper ready. Type something like:\n"
            "- 'open browser'\n"
            "- 'search for python decorators'\n"
            "- 'list files'\n"
            "- 'run git status'\n",
        )

    def _setup_voice(self) -> None:
        # We do not auto-start voice to avoid surprises in production.
        pass

    # ------------------------------------------------------------------
    # UI helpers
    # ------------------------------------------------------------------
    

    def _append_conversation(self, role: str, text: str) -> None:
        self.conversation.configure(state="normal")
        self.conversation.insert(tk.END, f"[{role.upper()}] {text}\n\n")
        self.conversation.configure(state="disabled")
        self.conversation.see(tk.END)

    def _refresh_command_log(self) -> None:
        self.command_log.configure(state="normal")
        self.command_log.delete("1.0", tk.END)
        for entry in self.agent.command_log:
            status = "OK" if entry.success else "ERR"
            ts = entry.timestamp.strftime("%H:%M:%S")
            self.command_log.insert(
                tk.END,
                f"[{ts}] [{status}] {entry.command}\n"
                f"  from: {entry.natural_language}\n\n",
            )
        self.command_log.configure(state="disabled")
        self.command_log.see(tk.END)

    def _copy_log_to_clipboard(self) -> None:
        self.clipboard_clear()
        self.clipboard_append(self.command_log.get("1.0", tk.END))
        self._append_conversation("system", "Command log copied to clipboard.")

    def _clear_conversation(self) -> None:
        self.conversation.configure(state="normal")
        self.conversation.delete("1.0", tk.END)
        self.conversation.configure(state="disabled")
        self._append_conversation("system", "Conversation cleared.")

    

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------
    def _on_send(self, event: Optional[tk.Event] = None) -> None:  # type: ignore[override]
        text = self.input_var.get().strip()
        if not text:
            return
        self.input_var.set("")
        self._append_conversation("user", text)
        self._run_agent_async(text)

    def _on_shell_toggle(self) -> None:
        self.agent.config.allow_shell_commands = bool(self.shell_enabled.get())
        state = "enabled" if self.agent.config.allow_shell_commands else "disabled"
        self._append_conversation("system", f"Shell execution {state} for this session.")

    def _toggle_voice(self) -> None:
        if self.voice_button["text"] == "Start Voice":
            if not self.voice.input_available:
                self._append_conversation(
                    "system",
                    "Voice input is not available (missing microphone or audio dependencies). "
                    "You can still use text input.",
                )
                return
            self.voice.start_listening(self._on_voice_text)
            self.voice_button.configure(text="Stop Voice")
            self._append_conversation("system", "Voice listening started.")
        else:
            self.voice.stop_listening()
            self.voice_button.configure(text="Start Voice")
            self._append_conversation("system", "Voice listening stopped.")

    def _on_voice_text(self, text: str) -> None:
        # Called from background voice thread; marshal to main thread
        def _handle():
            self._append_conversation("user (voice)", text)
            self._run_agent_async(text)

        self.after(0, _handle)

    # ------------------------------------------------------------------
    # Agent interaction
    # ------------------------------------------------------------------
    def _run_agent_async(self, text: str) -> None:
        def _worker() -> None:
            response = self.agent.handle_request(text)
            self.after(0, lambda: self._on_agent_response(text, response))

        threading.Thread(target=_worker, daemon=True).start()

    def _on_agent_response(self, original_text: str, response: str) -> None:
        self._append_conversation("assistant", response)
        self._refresh_command_log()
        # Optional: voice feedback
        # self.voice.speak(response)


def main() -> None:
    app = LocalHelperGUI()
    app.mainloop()


if __name__ == "__main__":
    main()

