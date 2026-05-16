from __future__ import annotations

from pathlib import Path
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from .runtime import ClassifierRuntime


APP_TITLE = "AI GUI Keras Classifier - Reconstructed Skeleton"


class ClassifierGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("860x620")
        self.root.minsize(780, 560)

        project_root = Path(__file__).resolve().parents[1]
        self.runtime = ClassifierRuntime(project_root / "data" / "synthetic_profiles.csv")

        self.age_var = tk.StringVar(value="32")
        self.salary_var = tk.StringVar(value="52000")
        self.experience_var = tk.StringVar(value="8")
        self.prefer_keras_var = tk.BooleanVar(value=True)

        self.status_var = tk.StringVar(value="Dataset loaded. Train the model or run a prediction.")
        self.result_var = tk.StringVar(value="No prediction yet.")
        self.metrics_var = tk.StringVar(value=self.dataset_summary_text())

        self.build_ui()

    def dataset_summary_text(self) -> str:
        dataset = self.runtime.dataset
        return (
            f"Dataset size: {dataset.size}\n"
            f"Positive rate: {dataset.positive_rate:.3f}\n"
            f"Features: {', '.join(dataset.feature_names)}"
        )

    def build_ui(self) -> None:
        outer = ttk.Frame(self.root, padding=18)
        outer.pack(fill=tk.BOTH, expand=True)

        title = ttk.Label(outer, text="AI GUI Keras Classifier", font=("Arial", 22, "bold"))
        title.pack(anchor="w")

        subtitle = ttk.Label(
            outer,
            text="Synthetic age/salary/experience classifier with optional Keras backend and NumPy fallback.",
        )
        subtitle.pack(anchor="w", pady=(4, 16))

        body = ttk.Frame(outer)
        body.pack(fill=tk.BOTH, expand=True)

        left = ttk.LabelFrame(body, text="Input profile", padding=14)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        right = ttk.LabelFrame(body, text="Model status", padding=14)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        self.add_entry(left, "Age", self.age_var, 0)
        self.add_entry(left, "Salary", self.salary_var, 1)
        self.add_entry(left, "Experience", self.experience_var, 2)

        prefer_keras = ttk.Checkbutton(
            left,
            text="Prefer Keras if TensorFlow is installed",
            variable=self.prefer_keras_var,
        )
        prefer_keras.grid(row=3, column=0, columnspan=2, sticky="w", pady=(14, 8))

        train_button = ttk.Button(left, text="Train model", command=self.train_model)
        train_button.grid(row=4, column=0, sticky="ew", pady=(10, 4))

        predict_button = ttk.Button(left, text="Predict", command=self.predict)
        predict_button.grid(row=4, column=1, sticky="ew", pady=(10, 4), padx=(8, 0))

        regenerate_button = ttk.Button(left, text="Regenerate synthetic dataset", command=self.regenerate_dataset)
        regenerate_button.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(8, 4))

        result_label = ttk.Label(left, textvariable=self.result_var, wraplength=360, font=("Arial", 13, "bold"))
        result_label.grid(row=6, column=0, columnspan=2, sticky="w", pady=(20, 8))

        note = (
            "Important: this is synthetic educational data. "
            "Do not use this model for real hiring, salary, financial or eligibility decisions."
        )
        note_label = ttk.Label(left, text=note, wraplength=360)
        note_label.grid(row=7, column=0, columnspan=2, sticky="w", pady=(8, 0))

        metrics_title = ttk.Label(right, text="Dataset and training metrics", font=("Arial", 14, "bold"))
        metrics_title.pack(anchor="w")

        metrics = ttk.Label(right, textvariable=self.metrics_var, justify=tk.LEFT, wraplength=360)
        metrics.pack(anchor="w", pady=(10, 18))

        status_title = ttk.Label(right, text="Status log", font=("Arial", 14, "bold"))
        status_title.pack(anchor="w")

        status = ttk.Label(right, textvariable=self.status_var, justify=tk.LEFT, wraplength=360)
        status.pack(anchor="w", pady=(10, 18))

        explanation_title = ttk.Label(right, text="What this demonstrates", font=("Arial", 14, "bold"))
        explanation_title.pack(anchor="w")

        explanation = ttk.Label(
            right,
            text=(
                "This GUI demonstrates a small end-to-end ML workflow: dataset generation, "
                "feature scaling, training, prediction, validation warnings and responsible documentation."
            ),
            wraplength=360,
            justify=tk.LEFT,
        )
        explanation.pack(anchor="w", pady=(10, 0))

        left.columnconfigure(0, weight=1)
        left.columnconfigure(1, weight=1)

    def add_entry(self, parent: ttk.Frame, label: str, variable: tk.StringVar, row: int) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=7)
        entry = ttk.Entry(parent, textvariable=variable)
        entry.grid(row=row, column=1, sticky="ew", pady=7, padx=(8, 0))

    def train_model(self) -> None:
        try:
            result = self.runtime.train(prefer_keras=self.prefer_keras_var.get())
        except Exception as exc:
            messagebox.showerror("Training error", str(exc))
            return

        self.metrics_var.set(
            f"Backend: {result.backend}\n"
            f"Accuracy: {result.accuracy:.3f}\n"
            f"Loss: {result.loss:.4f}\n"
            f"Dataset size: {result.dataset_size}\n"
            f"Positive rate: {result.positive_rate:.3f}"
        )
        self.status_var.set("Model trained successfully.")

    def regenerate_dataset(self) -> None:
        dataset = self.runtime.regenerate_dataset(samples=600, seed=42)
        self.metrics_var.set(self.dataset_summary_text())
        self.status_var.set(f"Dataset regenerated with {dataset.size} synthetic rows. Model reset.")
        self.result_var.set("No prediction yet.")

    def parse_inputs(self) -> tuple[float, float, float] | None:
        try:
            age = float(self.age_var.get())
            salary = float(self.salary_var.get())
            experience = float(self.experience_var.get())
            return age, salary, experience
        except ValueError:
            messagebox.showerror("Input error", "Age, salary and experience must be numeric values.")
            return None

    def predict(self) -> None:
        values = self.parse_inputs()
        if values is None:
            return

        age, salary, experience = values

        try:
            prediction = self.runtime.predict(age, salary, experience)
        except Exception as exc:
            messagebox.showerror("Prediction error", str(exc))
            return

        probability = float(prediction["probability"])
        label = int(prediction["label"])
        backend = str(prediction["backend"])
        warnings = prediction["warnings"]

        class_text = "positive synthetic class" if label == 1 else "negative synthetic class"
        warning_text = ""
        if warnings:
            warning_text = "\nWarnings: " + "; ".join(str(item) for item in warnings)

        self.result_var.set(
            f"Prediction: {class_text}\n"
            f"Confidence: {probability:.3f}\n"
            f"Backend: {backend}"
            f"{warning_text}"
        )
        self.status_var.set("Prediction completed.")


def run_app() -> None:
    root = tk.Tk()
    app = ClassifierGUI(root)
    root.mainloop()
