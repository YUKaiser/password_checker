import re
import secrets
import string
import tkinter as tk
from tkinter import messagebox, ttk


COMMON_PASSWORDS = {
    "123456",
    "123456789",
    "12345678",
    "admin",
    "iloveyou",
    "letmein",
    "password",
    "password1",
    "qwerty",
    "qwerty123",
}

SEQUENCES = ("1234", "abcd", "qwerty", "asdf")


def check_password_strength(password):
    score = 0
    feedback = []
    lowered = password.lower()

    if len(password) >= 16:
        score += 45
    elif len(password) >= 12:
        score += 35
    elif len(password) >= 8:
        score += 25
    else:
        feedback.append("Use at least 8 characters; 16 or more is better.")

    character_groups = (
        (r"[a-z]", "Add lowercase letters."),
        (r"[A-Z]", "Add uppercase letters."),
        (r"\d", "Add numbers."),
        (r"[^A-Za-z0-9\s]", "Add symbols."),
    )
    for pattern, suggestion in character_groups:
        if re.search(pattern, password):
            score += 10
        else:
            feedback.append(suggestion)

    if password:
        unique_ratio = len(set(password)) / len(password)
        if unique_ratio >= 0.65:
            score += 15
        elif unique_ratio >= 0.45:
            score += 8
        else:
            feedback.append("Avoid repeating the same characters.")

    if lowered in COMMON_PASSWORDS or any(
        common in lowered for common in ("password", "qwerty", "letmein", "admin")
    ):
        score = min(score, 10)
        feedback.insert(0, "This is a commonly used password. Choose a different one.")
    else:
        if any(sequence in lowered for sequence in SEQUENCES):
            score = max(0, score - 15)
            feedback.append("Avoid predictable keyboard or number sequences.")
        if re.search(r"(.)\1{2,}", password):
            score = max(0, score - 15)
            feedback.append("Avoid repeating a character three or more times in a row.")

    score = min(score, 100)
    if score < 30:
        strength, color = "Weak", "#D93025"
    elif score < 55:
        strength, color = "Fair", "#E37400"
    elif score < 75:
        strength, color = "Good", "#188038"
    else:
        strength, color = "Excellent", "#137333"

    if not feedback:
        feedback.append("Good work. Use a unique password for every account.")
    return strength, color, score, feedback


def generate_password(length):
    groups = (
        string.ascii_lowercase,
        string.ascii_uppercase,
        string.digits,
        string.punctuation,
    )
    if length < len(groups):
        raise ValueError("Password length must be at least 4.")

    characters = [secrets.choice(group) for group in groups]
    all_characters = "".join(groups)
    characters.extend(
        secrets.choice(all_characters) for _ in range(length - len(characters))
    )
    secrets.SystemRandom().shuffle(characters)
    return "".join(characters)


def main():
    background = "#F5F7FB"
    root = tk.Tk()
    root.title("CyberSafe | Password Lab")
    root.geometry("520x570")
    root.configure(bg=background)
    root.resizable(False, False)

    style = ttk.Style(root)
    style.configure(
        "Strength.Horizontal.TProgressbar",
        troughcolor="#E3E8EF",
        background="#188038",
        thickness=12,
    )

    tk.Label(
        root,
        text="Password Lab",
        font=("Segoe UI", 21, "bold"),
        bg=background,
        fg="#172B4D",
    ).pack(pady=(22, 2))
    tk.Label(
        root,
        text="Check password habits and create a stronger password",
        font=("Segoe UI", 10),
        bg=background,
        fg="#5E6C84",
    ).pack(pady=(0, 18))

    content = tk.Frame(root, bg="white", padx=22, pady=20)
    content.pack(fill="x", padx=24)

    tk.Label(
        content,
        text="Your password",
        font=("Segoe UI", 10, "bold"),
        bg="white",
        fg="#344563",
    ).pack(anchor="w")
    password_entry = tk.Entry(
        content,
        font=("Consolas", 13),
        show="*",
        relief="solid",
        bd=1,
        insertwidth=2,
    )
    password_entry.pack(fill="x", pady=(7, 5), ipady=7)

    show_password = tk.BooleanVar(value=False)

    def toggle_password_visibility():
        password_entry.configure(show="" if show_password.get() else "*")

    tk.Checkbutton(
        content,
        text="Show password",
        variable=show_password,
        command=toggle_password_visibility,
        bg="white",
        activebackground="white",
        fg="#5E6C84",
        font=("Segoe UI", 9),
    ).pack(anchor="w")

    strength_label = tk.Label(
        content,
        text="Strength: Ready",
        font=("Segoe UI", 13, "bold"),
        bg="white",
        fg="#5E6C84",
    )
    strength_label.pack(anchor="w", pady=(12, 4))
    progress = ttk.Progressbar(
        content,
        maximum=100,
        style="Strength.Horizontal.TProgressbar",
    )
    progress.pack(fill="x", pady=(0, 10))
    feedback_label = tk.Label(
        content,
        text="Start typing to get private, on-device feedback.",
        font=("Segoe UI", 9),
        bg="white",
        fg="#344563",
        justify="left",
        wraplength=420,
    )
    feedback_label.pack(anchor="w")

    def analyze_password(event=None):
        if event is not None:
            copy_status.config(text="")

        password = password_entry.get()
        if not password:
            strength_label.config(text="Strength: Ready", fg="#5E6C84")
            progress["value"] = 0
            feedback_label.config(
                text="Start typing to get private, on-device feedback."
            )
            return

        strength, color, score, feedback = check_password_strength(password)
        strength_label.config(text=f"Strength: {strength} ({score}/100)", fg=color)
        progress["value"] = score
        style.configure("Strength.Horizontal.TProgressbar", background=color)
        feedback_label.config(text="\n".join(f"• {item}" for item in feedback))

    def generate_and_analyze():
        try:
            length = length_var.get()
        except tk.TclError:
            messagebox.showwarning("Invalid length", "Enter a whole number from 12 to 64.")
            return
        if not 12 <= length <= 64:
            messagebox.showwarning("Invalid length", "Choose a length from 12 to 64.")
            return

        generated = generate_password(length)
        password_entry.delete(0, tk.END)
        password_entry.insert(0, generated)
        analyze_password()

    def copy_password():
        password = password_entry.get()
        if not password:
            messagebox.showwarning("Nothing to copy", "Enter or generate a password first.")
            return
        root.clipboard_clear()
        root.clipboard_append(password)
        copy_status.config(text="Copied. Clear your clipboard when you are done.")

    password_entry.bind("<KeyRelease>", analyze_password)

    buttons = tk.Frame(content, bg="white")
    buttons.pack(fill="x", pady=(17, 0))
    tk.Button(
        buttons,
        text="Generate secure password",
        command=generate_and_analyze,
        font=("Segoe UI", 10, "bold"),
        bg="#1769E0",
        fg="white",
        activebackground="#0D55B8",
        activeforeground="white",
        relief="flat",
        padx=12,
        pady=8,
    ).pack(side="left")
    tk.Button(
        buttons,
        text="Copy",
        command=copy_password,
        font=("Segoe UI", 10),
        bg="#EAF0F6",
        fg="#172B4D",
        activebackground="#DCE5EF",
        relief="flat",
        padx=15,
        pady=8,
    ).pack(side="left", padx=(8, 0))

    generator = tk.Frame(root, bg=background)
    generator.pack(fill="x", padx=27, pady=(16, 0))
    tk.Label(
        generator,
        text="Generated password length:",
        font=("Segoe UI", 10),
        bg=background,
        fg="#344563",
    ).pack(side="left")
    length_var = tk.IntVar(value=20)
    tk.Spinbox(
        generator,
        from_=12,
        to=64,
        width=5,
        textvariable=length_var,
        font=("Segoe UI", 10),
        justify="center",
    ).pack(side="left", padx=9)

    copy_status = tk.Label(
        root,
        text="",
        font=("Segoe UI", 9),
        bg=background,
        fg="#5E6C84",
    )
    copy_status.pack(pady=(10, 0))
    tk.Label(
        root,
        text="Analysis stays on this device. Avoid reusing passwords across accounts.",
        font=("Segoe UI", 9),
        bg=background,
        fg="#5E6C84",
    ).pack(side="bottom", pady=16)

    root.mainloop()


if __name__ == "__main__":
    main()
