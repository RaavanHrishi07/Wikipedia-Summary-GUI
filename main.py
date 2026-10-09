import json
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from mediawiki import MediaWiki


HISTORY_FILE = Path(__file__).resolve().parent / "search_history.json"


class WikipediaSummaryApp:
    """GUI application for searching Wikipedia summaries."""

    MAX_HISTORY = 10

    def __init__(self, root):
        self.root = root
        self.root.title("Wikipedia Summary")
        self.root.geometry("850x700")
        self.root.minsize(700, 550)
        self.root.configure(bg="#202124")

        self.wikipedia = MediaWiki()
        self.suggestion_job = None
        self.search_history = self._load_history()

        self._configure_style()
        self._build_interface()
        self._refresh_history()
        self._bind_events()

    def _configure_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Search.TButton",
            font=("Arial", 12, "bold"),
            padding=(18, 8),
        )

    def _build_interface(self):
        header = tk.Frame(self.root, bg="#202124")
        header.pack(fill="x", padx=30, pady=(20, 10))

        tk.Label(
            header,
            text="Wikipedia Summary",
            font=("Arial", 24, "bold"),
            bg="#202124",
            fg="white",
        ).pack()

        tk.Label(
            header,
            text="Search a topic and explore Wikipedia",
            font=("Arial", 11),
            bg="#202124",
            fg="#b8b8b8",
        ).pack(pady=(5, 0))

        search_frame = tk.Frame(self.root, bg="#202124")
        search_frame.pack(fill="x", padx=30, pady=15)

        self.topic_var = tk.StringVar()

        self.topic_entry = tk.Entry(
            search_frame,
            textvariable=self.topic_var,
            font=("Arial", 14),
            bg="white",
            fg="#202124",
            relief="flat",
            insertbackground="#202124",
        )
        self.topic_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=9,
            padx=(0, 10),
        )

        self.search_button = ttk.Button(
            search_frame,
            text="Get Summary",
            style="Search.TButton",
            command=self.get_summary,
        )
        self.search_button.pack(side="right")

        self.suggestion_box = tk.Listbox(
            self.root,
            font=("Arial", 11),
            height=5,
            bg="white",
            fg="#202124",
            selectbackground="#3b78e7",
            selectforeground="white",
            activestyle="none",
        )

        history_frame = tk.Frame(self.root, bg="#202124")
        history_frame.pack(fill="x", padx=30, pady=(0, 12))

        history_header = tk.Frame(history_frame, bg="#202124")
        history_header.pack(fill="x")

        tk.Label(
            history_header,
            text="Recent Searches",
            font=("Arial", 11, "bold"),
            bg="#202124",
            fg="white",
        ).pack(side="left")

        self.clear_history_button = ttk.Button(
            history_header,
            text="Clear History",
            command=self.clear_history,
        )
        self.clear_history_button.pack(side="right")

        self.history_box = tk.Listbox(
            history_frame,
            height=3,
            font=("Arial", 10),
            bg="#303134",
            fg="white",
            selectbackground="#3b78e7",
            selectforeground="white",
            activestyle="none",
            relief="flat",
        )
        self.history_box.pack(fill="x", pady=(6, 0))

        tk.Label(
            history_frame,
            text="Double-click a topic to search it again.",
            font=("Arial", 9),
            bg="#202124",
            fg="#b8b8b8",
            anchor="w",
        ).pack(fill="x", pady=(4, 0))

        content_frame = tk.Frame(self.root, bg="#202124")
        content_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 12),
        )

        self.summary_text = tk.Text(
            content_frame,
            wrap="word",
            font=("Arial", 12),
            bg="#f5f5f5",
            fg="#202124",
            relief="flat",
            padx=15,
            pady=15,
            state="disabled",
        )
        self.summary_text.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            content_frame,
            orient="vertical",
            command=self.summary_text.yview,
        )
        scrollbar.pack(side="right", fill="y")
        self.summary_text.configure(yscrollcommand=scrollbar.set)

        self.status_label = tk.Label(
            self.root,
            text="Enter a topic to begin.",
            font=("Arial", 10),
            bg="#202124",
            fg="#b8b8b8",
            anchor="w",
        )
        self.status_label.pack(fill="x", padx=30, pady=(0, 12))

    def _bind_events(self):
        self.topic_entry.bind("<KeyRelease>", self._schedule_suggestions)
        self.topic_entry.bind("<Return>", self._handle_enter)
        self.topic_entry.bind("<Down>", self._focus_suggestions)

        self.suggestion_box.bind(
            "<Double-Button-1>",
            self._select_suggestion,
        )
        self.suggestion_box.bind(
            "<Return>",
            self._select_suggestion,
        )

        self.history_box.bind(
            "<Double-Button-1>",
            self._select_history,
        )
        self.root.bind("<Escape>", self._hide_suggestions)

    def _load_history(self):
        """Load saved search history safely."""
        try:
            if not HISTORY_FILE.exists():
                return []

            with HISTORY_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                return []

            history = []
            seen = set()

            for item in data:
                if not isinstance(item, str) or not item.strip():
                    continue

                topic = item.strip()
                key = topic.casefold()

                if key not in seen:
                    history.append(topic)
                    seen.add(key)

                if len(history) >= self.MAX_HISTORY:
                    break

            return history

        except (OSError, json.JSONDecodeError):
            return []

    def _save_history(self):
        """Persist the current search history to JSON."""
        try:
            with HISTORY_FILE.open("w", encoding="utf-8") as file:
                json.dump(
                    self.search_history,
                    file,
                    indent=4,
                    ensure_ascii=False,
                )
        except OSError as error:
            messagebox.showwarning(
                "History Save Error",
                f"Could not save search history:\n{error}",
            )

    def _schedule_suggestions(self, event=None):
        if event and event.keysym in (
            "Up", "Down", "Return", "Escape"
        ):
            return

        if self.suggestion_job is not None:
            self.root.after_cancel(self.suggestion_job)
            self.suggestion_job = None

        self.suggestion_job = self.root.after(
            350,
            self._fetch_suggestions,
        )

    def _fetch_suggestions(self):
        self.suggestion_job = None
        query = self.topic_var.get().strip()

        if len(query) < 2:
            self._hide_suggestions()
            return

        try:
            titles = self.wikipedia.search(query, results=6)
            self.suggestion_box.delete(0, tk.END)

            for title in titles:
                self.suggestion_box.insert(tk.END, title)

            if titles:
                self._show_suggestions()
                self.status_label.config(
                    text="Choose a suggestion or continue typing."
                )
            else:
                self._hide_suggestions()

        except Exception:
            self._hide_suggestions()

    def _show_suggestions(self):
        if not self.suggestion_box.winfo_ismapped():
            self.suggestion_box.pack(
                fill="x",
                padx=30,
                pady=(0, 10),
                before=self.root.winfo_children()[3],
            )

    def _hide_suggestions(self, event=None):
        if self.suggestion_box.winfo_ismapped():
            self.suggestion_box.pack_forget()

    def _focus_suggestions(self, event=None):
        if self.suggestion_box.size() > 0:
            self.suggestion_box.focus_set()
            self.suggestion_box.selection_clear(0, tk.END)
            self.suggestion_box.selection_set(0)
            self.suggestion_box.activate(0)
            return "break"

    def _select_suggestion(self, event=None):
        selection = self.suggestion_box.curselection()

        if not selection:
            return "break"

        selected_title = self.suggestion_box.get(selection[0])
        self.topic_var.set(selected_title)
        self._hide_suggestions()
        self.get_summary()
        return "break"

    def _handle_enter(self, event=None):
        if self.suggestion_box.winfo_ismapped():
            selection = self.suggestion_box.curselection()
            if selection:
                self._select_suggestion()
                return "break"

        self._hide_suggestions()
        self.get_summary()
        return "break"

    def _add_to_history(self, topic):
        self.search_history = [
            item
            for item in self.search_history
            if item.casefold() != topic.casefold()
        ]

        self.search_history.insert(0, topic)
        self.search_history = self.search_history[:self.MAX_HISTORY]

        self._refresh_history()
        self._save_history()

    def _refresh_history(self):
        self.history_box.delete(0, tk.END)

        for topic in self.search_history:
            self.history_box.insert(tk.END, topic)

    def _select_history(self, event=None):
        selection = self.history_box.curselection()

        if not selection:
            return

        topic = self.history_box.get(selection[0])
        self.topic_var.set(topic)
        self._hide_suggestions()
        self.get_summary()

    def clear_history(self):
        if not self.search_history:
            self.status_label.config(text="Search history is already empty.")
            return

        self.search_history.clear()
        self._refresh_history()
        self._save_history()
        self.status_label.config(text="Search history cleared.")

    def _set_summary(self, text):
        self.summary_text.configure(state="normal")
        self.summary_text.delete("1.0", tk.END)
        self.summary_text.insert("1.0", text)
        self.summary_text.configure(state="disabled")

    def get_summary(self):
        topic = self.topic_var.get().strip()

        if not topic:
            messagebox.showwarning(
                "Missing Topic",
                "Please enter a topic to search.",
            )
            self.status_label.config(text="Please enter a topic.")
            return

        self._hide_suggestions()
        self.search_button.config(state="disabled")
        self.status_label.config(text=f"Searching for '{topic}'...")
        self.root.update_idletasks()

        try:
            page = self.wikipedia.page(topic)
            summary = page.summary.strip()

            if not summary:
                raise ValueError("No summary was available.")

            self._set_summary(summary)
            self._add_to_history(page.title)
            self.status_label.config(
                text=f"Showing summary for '{page.title}'."
            )

        except Exception:
            self._set_summary("")
            self.status_label.config(
                text="Unable to retrieve the requested article."
            )
            messagebox.showerror(
                "Search Error",
                "Could not retrieve this Wikipedia article.\n\n"
                "Try selecting a suggestion or using a more specific topic.",
            )

        finally:
            self.search_button.config(state="normal")
            self.topic_entry.focus_set()


def main():
    root = tk.Tk()
    WikipediaSummaryApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
    