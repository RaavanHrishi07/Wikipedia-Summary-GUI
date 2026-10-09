import tkinter as tk
from tkinter import messagebox, ttk

from mediawiki import MediaWiki


class WikipediaSummaryApp:
    """GUI application for retrieving Wikipedia article summaries."""

    def __init__(self, root):
        self.root = root
        self.root.title("Wikipedia Summary")
        self.root.geometry("800x650")
        self.root.minsize(650, 500)
        self.root.configure(bg="#202124")

        self.wikipedia = MediaWiki()

        self._configure_style()
        self._build_interface()
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
        header.pack(fill="x", padx=30, pady=(25, 10))

        title = tk.Label(
            header,
            text="Wikipedia Summary",
            font=("Arial", 24, "bold"),
            bg="#202124",
            fg="white",
        )
        title.pack()

        subtitle = tk.Label(
            header,
            text="Search for a topic and read its Wikipedia summary",
            font=("Arial", 11),
            bg="#202124",
            fg="#b8b8b8",
        )
        subtitle.pack(pady=(5, 0))

        search_frame = tk.Frame(self.root, bg="#202124")
        search_frame.pack(fill="x", padx=30, pady=20)

        self.topic_entry = tk.Entry(
            search_frame,
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

        content_frame = tk.Frame(self.root, bg="#202124")
        content_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 15),
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

        self.summary_text.configure(
            yscrollcommand=scrollbar.set
        )

        self.status_label = tk.Label(
            self.root,
            text="Enter a topic to begin.",
            font=("Arial", 10),
            bg="#202124",
            fg="#b8b8b8",
            anchor="w",
        )
        self.status_label.pack(
            fill="x",
            padx=30,
            pady=(0, 15),
        )

    def _bind_events(self):
        self.topic_entry.bind("<Return>", lambda event: self.get_summary())

    def _set_summary(self, text):
        self.summary_text.configure(state="normal")
        self.summary_text.delete("1.0", tk.END)
        self.summary_text.insert("1.0", text)
        self.summary_text.configure(state="disabled")

    def get_summary(self):
        topic = self.topic_entry.get().strip()

        if not topic:
            messagebox.showwarning(
                "Missing Topic",
                "Please enter a topic to search.",
            )
            self.status_label.config(text="Please enter a topic.")
            return

        self.search_button.config(state="disabled")
        self.status_label.config(text=f"Searching for '{topic}'...")
        self.root.update_idletasks()

        try:
            page = self.wikipedia.page(topic)
            summary = page.summary.strip()

            if not summary:
                raise ValueError(
                    "No summary was available for this article."
                )

            self._set_summary(summary)
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
                "Could not find a Wikipedia article for this topic.\n\n"
                "Try a different or more specific topic.",
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
    