from __future__ import annotations

import os
import shlex
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Dict, List, Optional, Tuple




@dataclass
class CommandLogEntry:
    timestamp: datetime
    natural_language: str
    command: str
    result: str
    success: bool


@dataclass
class AgentConfig:
    shell: str = "powershell" if os.name == "nt" else "bash"
    allow_shell_commands: bool = True
    working_directory: str = field(default_factory=lambda: os.getcwd())


class LocalHelperAgent:
    """
    A small but production-oriented local agent.

    Responsibilities:
    - Turn natural language into concrete actions / shell commands
    - Execute those commands (if allowed) in a controlled way
    - Return human-readable responses
    - Keep a detailed log of every command that was run
    """

    def __init__(self, config: Optional[AgentConfig] = None) -> None:
        self.config = config or AgentConfig()
        self._tools: Dict[str, Callable[[str], Tuple[str, Optional[str]]]] = {}
        self._command_log: List[CommandLogEntry] = []
        self._register_builtin_tools()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    @property
    def command_log(self) -> List[CommandLogEntry]:
        return list(self._command_log)

    def handle_request(self, text: str) -> str:
        """
        Main entry-point used by the GUI.
        Returns a human-readable response string.
        """
        text = (text or "").strip()
        if not text:
            return "I did not receive any text to work with."

        tool_name, arg = self._route(text)
        tool = self._tools.get(tool_name)
        if not tool:
            return "I understood the request but do not have a tool to handle it yet."

        shell_command_description, maybe_shell_command = tool(arg)
        result, success = self._execute_if_applicable(
            natural_language=text,
            shell_command_description=shell_command_description,
            shell_command=maybe_shell_command,
        )
        return result

    # ------------------------------------------------------------------
    # Routing / parsing
    # ------------------------------------------------------------------
    def _route(self, text: str) -> Tuple[str, str]:
        lower = text.lower()

        # Very lightweight intent classification; this keeps things
        # understandable and safe for a local helper.
        if any(word in lower for word in ["open browser", "open chrome", "open edge"]):
            return "open_browser", text
        if lower.startswith("search ") or " search for " in lower:
            return "web_search", text
        if any(word in lower for word in ["list files", "show files", "show folder"]):
            return "list_files", text
        if any(
            phrase in lower
            for phrase in ["create folder", "make folder", "new folder", "mkdir "]
        ):
            return "create_folder", text
        if any(
            phrase in lower
            for phrase in ["open folder", "open current folder", "open project folder"]
        ):
            return "open_folder", text
        if any(phrase in lower for phrase in ["system info", "system information"]):
            return "system_info", text
        if any(phrase in lower for phrase in ["show ip", "my ip", "ip address"]):
            return "show_ip", text
        if any(phrase in lower for phrase in ["disk usage", "free space"]):
            return "disk_usage", text
        if any(
            phrase in lower
            for phrase in ["show processes", "list processes", "running tasks"]
        ):
            return "process_list", text
        if "weather" in lower:
            return "weather", text
        if any(word in lower for word in ["time", "what time is it", "current time", "tell me the time"]):
            return "time_inquiry", text
        if any(word in lower for word in ["date", "what's the date today", "current date", "what date is it"]):
            return "date_inquiry", text
        if any(phrase in lower for phrase in ["delete file", "remove file", "del"]):
            return "delete_file", text
        if lower.startswith("run ") or lower.startswith("execute "):
            return "run_shell", text
        if any(word in lower for word in ["help", "what can you do"]):
            return "help", text

        # Fallback: treat as a generic shell-like request in dry-run mode
        return "interpret", text

    # ------------------------------------------------------------------
    # Tool registration
    # ------------------------------------------------------------------
    def _register_builtin_tools(self) -> None:
        self._tools["help"] = self._tool_help
        self._tools["list_files"] = self._tool_list_files
        self._tools["open_browser"] = self._tool_open_browser
        self._tools["web_search"] = self._tool_web_search
        self._tools["create_folder"] = self._tool_create_folder
        self._tools["open_folder"] = self._tool_open_folder
        self._tools["system_info"] = self._tool_system_info
        self._tools["show_ip"] = self._tool_show_ip
        self._tools["disk_usage"] = self._tool_disk_usage
        self._tools["process_list"] = self._tool_process_list
        self._tools["weather"] = self._tool_weather
        self._tools["time_inquiry"] = self._tool_time_inquiry
        self._tools["date_inquiry"] = self._tool_date_inquiry
        self._tools["delete_file"] = self._tool_delete_file
        self._tools["run_shell"] = self._tool_run_shell
        self._tools["interpret"] = self._tool_interpret

    # ------------------------------------------------------------------
    # Tools
    # ------------------------------------------------------------------
    def _tool_help(self, _: str) -> Tuple[str, Optional[str]]:
        description = "Display list of available capabilities (no shell command)."
        return description, None

    def _tool_list_files(self, text: str) -> Tuple[str, Optional[str]]:
        path = self.config.working_directory
        return f"List files in {path}", f"ls {shlex.quote(path)}"

    def _tool_create_folder(self, text: str) -> Tuple[str, Optional[str]]:
        # Try to extract a folder name from the text; fall back to 'NewFolder'
        folder_name = "NewFolder"
        for prefix in ["create folder", "make folder", "new folder", "mkdir"]:
            if prefix in text.lower():
                # naive split: take everything after the prefix
                parts = text.lower().split(prefix, 1)
                if len(parts) == 2 and parts[1].strip():
                    folder_name = parts[1].strip().strip("\"'")
                break
        cmd = f'mkdir "{folder_name}"'
        return f"Create a folder named '{folder_name}'", cmd

    def _tool_open_folder(self, _: str) -> Tuple[str, Optional[str]]:
        path = self.config.working_directory
        if os.name == "nt":
            cmd = f'start "" "{path}"'
        elif sys.platform == "darwin":
            cmd = f'open "{path}"'
        else:
            cmd = f'xdg-open "{path}"'
        return f"Open folder {path} in file explorer", cmd

    def _tool_system_info(self, _: str) -> Tuple[str, Optional[str]]:
        if os.name == "nt":
            cmd = "systeminfo"
        else:
            cmd = "uname -a"
        return "Show basic system information", cmd

    def _tool_show_ip(self, _: str) -> Tuple[str, Optional[str]]:
        if os.name == "nt":
            cmd = "ipconfig"
        else:
            cmd = "ip addr || ifconfig"
        return "Show network IP configuration", cmd

    def _tool_disk_usage(self, _: str) -> Tuple[str, Optional[str]]:
        if os.name == "nt":
            cmd = "Get-PSDrive"
        else:
            cmd = "df -h"
        return "Show disk usage information", cmd

    def _tool_process_list(self, _: str) -> Tuple[str, Optional[str]]:
        if os.name == "nt":
            cmd = "Get-Process | Sort-Object CPU -Descending | Select-Object -First 20"
        else:
            cmd = "ps aux | head -n 20"
        return "Show a short list of running processes", cmd

    def _tool_open_browser(self, _: str) -> Tuple[str, Optional[str]]:
        # On Windows the `start` command needs to be invoked via shell=True;
        # we keep it simple and rely on the configured shell.
        return "Open the default web browser", "start http://www.google.com" if os.name == "nt" else "xdg-open ."

    def _tool_web_search(self, text: str) -> Tuple[str, Optional[str]]:
        keyword = text
        for prefix in ["search ", "search for "]:
            if text.lower().startswith(prefix):
                keyword = text[len(prefix) :]
                break
        keyword = keyword.strip() or "cursor"
        url = f"https://www.google.com/search?q={shlex.quote(keyword)}"
        if os.name == "nt":
            cmd = f'start "{url}"'
        else:
            cmd = f'xdg-open "{url}"'
        return f"Search the web for '{keyword}'", cmd

    def _tool_weather(self, text: str) -> Tuple[str, Optional[str]]:
        location = ""
        if "in" in text.lower():
            location = text.lower().split("in", 1)[1].strip()
        url = f"https://wttr.in/{location}?format=3"
        if os.name == 'nt':
            cmd = f"Invoke-WebRequest -Uri {url} | Select-Object -ExpandProperty Content"
        else:
            cmd = f"curl -s {url}"
        return f"Get weather forecast for {location or 'your location'}", cmd

    def _tool_time_inquiry(self, _: str) -> Tuple[str, Optional[str]]:
        now = datetime.now()
        return "Get the current time", f"echo 'The current time is {now.strftime('%H:%M:%S')}'"

    def _tool_date_inquiry(self, _: str) -> Tuple[str, Optional[str]]:
        today = datetime.now()
        return "Get the current date", f"echo 'Today is {today.strftime('%Y-%m-%d')}'"

    def _tool_delete_file(self, text: str) -> Tuple[str, Optional[str]]:
        # Try to extract a file name from the text
        file_name = ""
        for prefix in ["delete file", "remove file", "delete"]:
            if prefix in text.lower():
                # naive split: take everything after the prefix
                parts = text.lower().split(prefix, 1)
                if len(parts) == 2 and parts[1].strip():
                    file_name = parts[1].strip().strip("\"'")
                break
        
        if not file_name:
            return "Could not determine the file to delete.", None

        if os.name == "nt":
            cmd = f'del "{file_name}"'
        else:
            cmd = f'rm "{file_name}"'
        return f"Delete a file named '{file_name}'", cmd

    def _tool_run_shell(self, text: str) -> Tuple[str, Optional[str]]:
        raw = text
        for prefix in ["run ", "execute "]:
            if raw.lower().startswith(prefix):
                raw = raw[len(prefix) :]
                break
        raw = raw.strip()
        return f"Run custom shell command: {raw}", raw or None

    def _tool_interpret(self, text: str) -> Tuple[str, Optional[str]]:
        # Very small heuristic: if it looks like a path or a command, pass through
        return f"Interpret text as shell-like instruction: {text}", text

    # ------------------------------------------------------------------
    # Execution / logging
    # ------------------------------------------------------------------
    def _execute_if_applicable(
        self,
        natural_language: str,
        shell_command_description: str,
        shell_command: Optional[str],
    ) -> Tuple[str, bool]:
        if not shell_command:
            # Purely descriptive tool (e.g. help)
            result = self._handle_non_shell_tool(shell_command_description)
            self._append_log(
                natural_language=natural_language,
                command=shell_command_description,
                result=result,
                success=True,
            )
            return result, True

        if not self.config.allow_shell_commands:
            msg = (
                f"I would run this command, but shell execution is disabled:\n"
                f"{shell_command}"
            )
            self._append_log(
                natural_language=natural_language,
                command=shell_command,
                result=msg,
                success=False,
            )
            return msg, False

        completed = self._run_subprocess(shell_command)
        success = completed.returncode == 0
        stdout = (completed.stdout or "").strip()
        stderr = (completed.stderr or "").strip()

        if success:
            if stdout:
                msg = f"Command completed successfully.\n\n{stdout}"
            else:
                msg = "Command completed successfully (no output)."
        else:
            msg_parts = [f"Command failed with code {completed.returncode}."]
            if stderr:
                msg_parts.append(stderr)
            msg = "\n".join(msg_parts)

        self._append_log(
            natural_language=natural_language,
            command=shell_command,
            result=msg,
            success=success,
        )
        return msg, success

    def _run_subprocess(self, command: str) -> subprocess.CompletedProcess:
        """
        Run the given command using the configured shell.
        All output is captured so that the GUI can display it.
        """
        if os.name == "nt":
            # On Windows we rely on powershell / cmd as needed.
            full_cmd = [self.config.shell, "-Command", command]
        else:
            full_cmd = [self.config.shell, "-lc", command]

        return subprocess.run(
            full_cmd,
            cwd=self.config.working_directory,
            capture_output=True,
            text=True,
        )

    def _handle_non_shell_tool(self, description: str) -> str:
        if description.startswith("Display list of available capabilities"):
            return (
                "I can help you with tasks such as:\n"
                "- Open the current folder in your default file browser.\n"
                "- Search the web (e.g. 'search for python decorators').\n"
                "- List files in the current working directory.\n"
                "- Create folders using natural language.\n"
                "- Show system information, IP configuration, disk usage, and a short process list.\n"
                "- Get the current weather (e.g. 'weather in London').\n"
                "- Run custom shell commands (e.g. 'run git status').\n\n"
                "You can speak or type natural language instructions and I will "
                "translate them into concrete actions and show you exactly what "
                "commands were executed."
            )
        return description

    def _append_log(
        self,
        natural_language: str,
        command: str,
        result: str,
        success: bool,
    ) -> None:
        self._command_log.append(
            CommandLogEntry(
                timestamp=datetime.utcnow(),
                natural_language=natural_language,
                command=command,
                result=result,
                success=success,
            )
        )

