import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import random
import socket
import time

# Kali-inspired LOCAL LAB terminal emulator.
# The built-in lab commands are simulated and do not perform network attacks.

THEMES = {
    "Kali Dark": {"bg": "#111318", "panel": "#181b22", "fg": "#e8e8e8", "green": "#39ff88",
                  "cyan": "#35d0ff", "purple": "#8f7cff", "red": "#ff5f6d", "select": "#2b3150"},
    "Midnight Blue": {"bg": "#07111f", "panel": "#0c1a2b", "fg": "#e4f0ff", "green": "#52ffa8",
                      "cyan": "#62c7ff", "purple": "#a78bfa", "red": "#ff7181", "select": "#173454"},
    "Matrix": {"bg": "#020702", "panel": "#061006", "fg": "#d8ffd8", "green": "#00ff66",
               "cyan": "#5cffaa", "purple": "#66ff99", "red": "#ff5555", "select": "#10351b"},
}

LAB_FILES = {
    "/home/kali/lab/readme.txt": "Welcome to the simulated cyber lab.\nTry: lab status, lab hosts, lab scan 10.10.10.0/24\n",
    "/home/kali/lab/notes.txt": "Training only. All lab output is simulated locally.\n",
    "/home/kali/lab/targets.txt": "10.10.10.10  web-lab\n10.10.10.20  ssh-lab\n10.10.10.30  dns-lab\n",
}

class TerminalTab(ttk.Frame):
    def __init__(self, parent, app, name):
        super().__init__(parent)
        self.app = app
        self.name = name
        self.history = []
        self.history_index = 0

        self.output = tk.Text(
            self, wrap="word", font=("Consolas", 11), padx=12, pady=10,
            undo=False, relief="flat", borderwidth=0
        )
        self.output.pack(fill="both", expand=True, padx=1, pady=(1, 0))

        bottom = tk.Frame(self, bd=0)
        bottom.pack(fill="x")

        self.prompt_label = tk.Label(bottom, text="kali@lab:~$ ", font=("Consolas", 11, "bold"))
        self.prompt_label.pack(side="left", padx=(12, 0), pady=10)

        self.entry = tk.Entry(bottom, font=("Consolas", 11), relief="flat")
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 12), pady=10)
        self.entry.bind("<Return>", self.execute)
        self.entry.bind("<Up>", self.prev_history)
        self.entry.bind("<Down>", self.next_history)
        self.entry.bind("<Tab>", self.autocomplete)
        self.entry.bind("<Control-l>", lambda e: self.clear())

        self.cwd = "/home/kali"
        self.write("KALI LAB TERMINAL v2\nType 'help' for commands. This is a simulated lab.\n\n")

    def configure_colors(self, t):
        self.output.configure(bg=t["bg"], fg=t["fg"], insertbackground=t["fg"],
                               selectbackground=t["select"])
        self.prompt_label.configure(bg=t["panel"], fg=t["green"])
        self.entry.configure(bg=t["panel"], fg=t["fg"], insertbackground=t["fg"],
                             selectbackground=t["select"])
        self.configure(style="Terminal.TFrame")

    def write(self, text, color=None):
        tag = color or "normal"
        self.output.insert("end", text, tag)
        self.output.see("end")

    def prompt(self):
        return f"kali@lab:{'~' if self.cwd == '/home/kali' else self.cwd}$ "

    def execute(self, _=None):
        cmd = self.entry.get().strip()
        self.entry.delete(0, "end")
        if not cmd:
            return
        self.history.append(cmd)
        self.history_index = len(self.history)
        self.write(self.prompt() + cmd + "\n", "prompt")
        result = self.app.run_command(self, cmd)
        if result:
            self.write(result + ("\n" if not result.endswith("\n") else ""))
        self.write("\n")
        return "break"

    def prev_history(self, _=None):
        if self.history:
            self.history_index = max(0, self.history_index - 1)
            self.entry.delete(0, "end")
            self.entry.insert(0, self.history[self.history_index])
        return "break"

    def next_history(self, _=None):
        if self.history:
            self.history_index = min(len(self.history), self.history_index + 1)
            self.entry.delete(0, "end")
            if self.history_index < len(self.history):
                self.entry.insert(0, self.history[self.history_index])
        return "break"

    def autocomplete(self, _=None):
        current = self.entry.get().strip()
        commands = self.app.commands
        matches = [c for c in commands if c.startswith(current)]
        if len(matches) == 1:
            self.entry.delete(0, "end")
            self.entry.insert(0, matches[0] + " ")
        elif len(matches) > 1:
            self.write("\n" + "  ".join(matches) + "\n", "cyan")
        return "break"

    def clear(self):
        self.output.delete("1.0", "end")

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Kali Lab Terminal v2")
        self.root.geometry("1050x680")
        self.root.minsize(780, 500)

        self.commands = [
            "help", "clear", "history", "pwd", "ls", "cd", "cat", "whoami",
            "hostname", "uname", "date", "echo", "ifconfig", "ip", "lab",
            "lab status", "lab hosts", "lab scan", "theme", "newtab", "exit"
        ]

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Terminal.TFrame", background="#181b22")
        style.configure("TNotebook", background="#111318", borderwidth=0)
        style.configure("TNotebook.Tab", padding=(14, 8))

        top = tk.Frame(root, height=46)
        top.pack(fill="x")

        tk.Label(top, text="  KALI LAB", font=("Segoe UI", 12, "bold")).pack(side="left", padx=8)

        self.theme_var = tk.StringVar(value="Kali Dark")
        theme_box = ttk.Combobox(top, textvariable=self.theme_var, values=list(THEMES),
                                 state="readonly", width=16)
        theme_box.pack(side="right", padx=8, pady=8)
        theme_box.bind("<<ComboboxSelected>>", lambda e: self.apply_theme())

        tk.Button(top, text="+ New Tab", command=self.new_tab, relief="flat").pack(side="right", padx=4)
        tk.Button(top, text="Lab Help", command=self.show_lab_help, relief="flat").pack(side="right", padx=4)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        self.tabs = []
        self.new_tab()
        self.apply_theme()

    def current_tab(self):
        idx = self.notebook.index("current")
        return self.tabs[idx]

    def new_tab(self):
        n = len(self.tabs) + 1
        tab = TerminalTab(self.notebook, self, f"Terminal {n}")
        self.tabs.append(tab)
        self.notebook.add(tab, text=f"  {n}  ")
        self.notebook.select(tab)
        self.apply_theme()
        tab.entry.focus_set()

    def apply_theme(self):
        t = THEMES[self.theme_var.get()]
        self.root.configure(bg=t["bg"])
        for child in self.root.winfo_children():
            if isinstance(child, tk.Frame):
                child.configure(bg=t["panel"])
        for tab in self.tabs:
            tab.configure(style="Terminal.TFrame")
            tab.configure_colors(t)
            tab.output.tag_configure("normal", foreground=t["fg"])
            tab.output.tag_configure("prompt", foreground=t["green"])
            tab.output.tag_configure("cyan", foreground=t["cyan"])
            tab.output.tag_configure("error", foreground=t["red"])

    def run_command(self, tab, cmd):
        parts = cmd.split()
        base = parts[0].lower()

        if base == "help":
            return (
                "Built-ins:\n"
                "  help              command list\n"
                "  clear             clear screen\n"
                "  history           command history\n"
                "  pwd / ls / cd     simulated filesystem\n"
                "  cat <file>        read simulated lab file\n"
                "  whoami            current lab user\n"
                "  hostname          simulated host\n"
                "  uname             simulated OS info\n"
                "  ip / ifconfig     simulated network info\n"
                "  lab status        lab status\n"
                "  lab hosts         simulated hosts\n"
                "  lab scan <range>  simulated scan output\n"
                "  theme             show theme\n"
                "  newtab            open a new tab\n"
                "  exit              close this tab\n\n"
                "Tip: press ↑/↓ for history and Tab for autocomplete."
            )

        if base == "clear":
            tab.clear()
            return ""

        if base == "history":
            return "\n".join(f"{i+1:>3}  {c}" for i, c in enumerate(tab.history)) or "(empty)"

        if base == "pwd":
            return tab.cwd

        if base == "ls":
            if tab.cwd == "/home/kali":
                return "lab  notes.txt  tools"
            if tab.cwd == "/home/kali/lab":
                return "notes.txt  readme.txt  targets.txt"
            return "(empty)"

        if base == "cd":
            target = parts[1] if len(parts) > 1 else "/home/kali"
            if target in ("~", "/home/kali"):
                tab.cwd = "/home/kali"
            elif target in ("lab", "/home/kali/lab"):
                tab.cwd = "/home/kali/lab"
            elif target == "..":
                tab.cwd = "/home/kali"
            else:
                return f"cd: {target}: No such directory"
            return ""

        if base == "cat":
            if len(parts) < 2:
                return "cat: missing file operand"
            target = parts[1]
            path = target if target.startswith("/") else tab.cwd.rstrip("/") + "/" + target
            return LAB_FILES.get(path, f"cat: {target}: No such file")

        if base == "whoami":
            return "kali"

        if base == "hostname":
            return "kali-lab"

        if base == "uname":
            return "Linux kali-lab 6.1.0-kali-amd64 x86_64 GNU/Linux (simulated)"

        if base == "date":
            return time.ctime()

        if base == "echo":
            return cmd[5:] if len(cmd) > 5 else ""

        if base in ("ip", "ifconfig"):
            return (
                "eth0: 10.10.10.5/24\n"
                "lo:   127.0.0.1/8\n"
                "gateway: 10.10.10.1\n"
                "(simulated lab network)"
            )

        if base == "lab":
            sub = parts[1].lower() if len(parts) > 1 else ""
            if sub == "status":
                return "LAB STATUS: ONLINE\nMode: SIMULATION\nNetwork: 10.10.10.0/24\nTargets: 3"
            if sub == "hosts":
                return "10.10.10.10  web-lab\n10.10.10.20  ssh-lab\n10.10.10.30  dns-lab"
            if sub == "scan":
                target = parts[2] if len(parts) > 2 else "10.10.10.0/24"
                return self.simulated_scan(target)
            return "Usage: lab status | lab hosts | lab scan <range>"

        if base == "theme":
            return f"Current theme: {self.theme_var.get()}"

        if base == "newtab":
            self.new_tab()
            return ""

        if base == "exit":
            if len(self.tabs) == 1:
                self.root.destroy()
            else:
                idx = self.notebook.index(tab)
                self.notebook.forget(idx)
                self.tabs.pop(idx)
            return ""

        # Safe simulated responses for common shell/network commands.
        if base in ("nmap", "netstat", "ss", "ping", "curl", "wget", "ssh"):
            return "This command is disabled in the emulator. Use the built-in 'lab' commands for the simulated environment."

        return f"{base}: command not found. Type 'help'."

    def simulated_scan(self, target):
        return (
            f"Starting simulated scan of {target}\n"
            "Host 10.10.10.10 is up\n"
            "  22/tcp  closed  ssh\n"
            "  80/tcp  open    http\n"
            " 443/tcp  open    https\n"
            "Host 10.10.10.20 is up\n"
            "  22/tcp  open    ssh\n"
            "Host 10.10.10.30 is up\n"
            "  53/tcp  open    dns\n"
            "Scan complete — SIMULATED RESULTS"
        )

    def show_lab_help(self):
        messagebox.showinfo(
            "Built-in Cyber Lab",
            "Everything under 'lab' is simulated.\n\n"
            "Try:\n"
            "  lab status\n"
            "  lab hosts\n"
            "  lab scan 10.10.10.0/24\n\n"
            "No packets are sent and no external systems are touched."
        )

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
