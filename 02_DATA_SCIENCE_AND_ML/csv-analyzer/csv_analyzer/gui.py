from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from .core import read_csv_smart, analyze_dataframe, format_analysis_for_terminal
from .reporting import save_markdown_report
from .plotting import save_histograms


class CsvAnalyzerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("CSV Analyzer")
        self.geometry("1000x700")
        self.minsize(900, 600)

        self.current_result = None
        self.current_analysis = None

        self._build_ui()

    def _build_ui(self):
        toolbar = ttk.Frame(self, padding=8)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        ttk.Button(toolbar, text="Open CSV", command=self.open_csv).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(toolbar, text="Save Report", command=self.save_report).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(toolbar, text="Save Histograms", command=self.save_plots).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(toolbar, text="Clear", command=self.clear).pack(side=tk.LEFT)

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(toolbar, textvariable=self.status_var).pack(side=tk.RIGHT)

        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.summary_text = tk.Text(notebook, wrap=tk.NONE)
        self.summary_text.configure(font=("Menlo", 12))

        xscroll = ttk.Scrollbar(notebook, orient=tk.HORIZONTAL, command=self.summary_text.xview)
        yscroll = ttk.Scrollbar(notebook, orient=tk.VERTICAL, command=self.summary_text.yview)
        self.summary_text.configure(xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)

        frame = ttk.Frame(notebook)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        self.summary_text.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")

        notebook.add(frame, text="Summary")

    def open_csv(self):
        path = filedialog.askopenfilename(
            title="Open CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if not path:
            return

        try:
            result = read_csv_smart(path)
            analysis = analyze_dataframe(result.dataframe)
            self.current_result = result
            self.current_analysis = analysis

            text = format_analysis_for_terminal(result, analysis)
            self.summary_text.delete("1.0", tk.END)
            self.summary_text.insert(tk.END, text)

            self.status_var.set(f"Loaded: {Path(path).name}")
        except Exception as exc:
            messagebox.showerror("CSV Analyzer Error", str(exc))
            self.status_var.set("Error")

    def save_report(self):
        if not self.current_result or not self.current_analysis:
            messagebox.showinfo("CSV Analyzer", "Open a CSV file first.")
            return

        output_dir = Path("reports/generated")
        path = save_markdown_report(self.current_result, self.current_analysis, output_dir)
        messagebox.showinfo("CSV Analyzer", f"Report saved:\n{path}")
        self.status_var.set("Report saved")

    def save_plots(self):
        if not self.current_result:
            messagebox.showinfo("CSV Analyzer", "Open a CSV file first.")
            return

        output_dir = Path("reports/generated")
        paths = save_histograms(self.current_result.dataframe, output_dir)

        if paths:
            messagebox.showinfo("CSV Analyzer", f"Saved {len(paths)} histogram(s).")
        else:
            messagebox.showinfo("CSV Analyzer", "No numeric columns available.")

        self.status_var.set("Plots saved")

    def clear(self):
        self.current_result = None
        self.current_analysis = None
        self.summary_text.delete("1.0", tk.END)
        self.status_var.set("Ready")


def main():
    app = CsvAnalyzerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
