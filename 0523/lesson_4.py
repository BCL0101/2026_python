import tkinter as tk
from tkinter import ttk, messagebox
import random

class GuessNumberGame:
    def __init__(self, root):
        self.root = root
        self.root.title("猜數字遊戲")
        self.root.geometry("420x560")
        self.root.minsize(380, 520)
        self.root.configure(bg="#f5f7fb")
        self.root.resizable(False, False)

        self.target = 0
        self.attempts = 0
        self.low = 1
        self.high = 100

        self._style()
        self._build_ui()
        self.new_game()

    def _style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#f5f7fb")
        style.configure("Card.TFrame", background="#ffffff")
        style.configure("Title.TLabel", background="#f5f7fb", foreground="#1f2937", font=("Helvetica", 22, "bold"))
        style.configure("Sub.TLabel", background="#f5f7fb", foreground="#6b7280", font=("Helvetica", 10))
        style.configure("Info.TLabel", background="#ffffff", foreground="#374151", font=("Helvetica", 12))
        style.configure("Hint.TLabel", background="#ffffff", foreground="#2563eb", font=("Helvetica", 14, "bold"))
        style.configure("Count.TLabel", background="#ffffff", foreground="#6b7280", font=("Helvetica", 10))
        style.configure("TEntry", padding=8, font=("Helvetica", 14))
        style.configure("Accent.TButton", font=("Helvetica", 11, "bold"), padding=(12, 10), background="#2563eb", foreground="#ffffff")
        style.map("Accent.TButton", background=[("active", "#1d4ed8")])
        style.configure("Ghost.TButton", font=("Helvetica", 10), padding=(10, 8), background="#e5e7eb", foreground="#111827")
        style.map("Ghost.TButton", background=[("active", "#d1d5db")])
        style.configure("TProgressbar", troughcolor="#e5e7eb", background="#2563eb", thickness=12)

    def _build_ui(self):
        outer = ttk.Frame(self.root)
        outer.pack(fill="both", expand=True, padx=18, pady=18)

        header = ttk.Frame(outer)
        header.pack(fill="x", pady=(6, 14))
        ttk.Label(header, text="猜數字", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="在 1 到 100 之間猜出正確答案", style="Sub.TLabel").pack(anchor="w", pady=(4, 0))

        card = ttk.Frame(outer, style="Card.TFrame")
        card.pack(fill="both", expand=True)
        card.configure(padding=18)

        self.status_label = ttk.Label(card, text="請輸入一個數字開始遊戲", style="Info.TLabel", wraplength=340, justify="center")
        self.status_label.pack(fill="x", pady=(6, 14))

        self.range_label = ttk.Label(card, text="目前範圍：1 - 100", style="Info.TLabel", anchor="center")
        self.range_label.pack(fill="x", pady=(0, 10))

        self.entry = ttk.Entry(card, justify="center")
        self.entry.pack(fill="x", pady=(6, 10))
        self.entry.bind("<Return>", lambda e: self.check_guess())

        btn_row = ttk.Frame(card)
        btn_row.pack(fill="x", pady=(4, 10))
        ttk.Button(btn_row, text="送出", style="Accent.TButton", command=self.check_guess).pack(side="left", expand=True, fill="x", padx=(0, 6))
        ttk.Button(btn_row, text="重新開始", style="Ghost.TButton", command=self.new_game).pack(side="left", expand=True, fill="x", padx=(6, 0))

        self.hint_label = ttk.Label(card, text="", style="Hint.TLabel", anchor="center", justify="center", wraplength=320)
        self.hint_label.pack(fill="x", pady=(12, 8))

        self.progress = ttk.Progressbar(card, maximum=10, mode="determinate")
        self.progress.pack(fill="x", pady=(10, 6))

        self.count_label = ttk.Label(card, text="已猜次數：0", style="Count.TLabel", anchor="center")
        self.count_label.pack(fill="x", pady=(4, 0))

        tip = ttk.Label(outer, text="小提示：答對後可以直接按重新開始再玩一次。", style="Sub.TLabel")
        tip.pack(pady=(12, 0))

    def new_game(self):
        self.target = random.randint(1, 100)
        self.attempts = 0
        self.low = 1
        self.high = 100
        self.entry.delete(0, tk.END)
        self.entry.config(state="normal")
        self.status_label.config(text="新遊戲已開始，請輸入 1 到 100 的數字")
        self.range_label.config(text="目前範圍：1 - 100")
        self.hint_label.config(text="")
        self.count_label.config(text="已猜次數：0")
        self.progress["value"] = 0
        self.entry.focus_set()

    def check_guess(self):
        value = self.entry.get().strip()
        if not value.isdigit():
            messagebox.showwarning("輸入錯誤", "請輸入整數數字。")
            return

        guess = int(value)
        if guess < 1 or guess > 100:
            messagebox.showwarning("超出範圍", "請輸入 1 到 100 之間的數字。")
            return

        self.attempts += 1
        self.count_label.config(text=f"已猜次數：{self.attempts}")
        self.progress["value"] = min(self.attempts, 10)

        if guess < self.target:
            self.low = max(self.low, guess + 1)
            self.status_label.config(text="再大一點！")
            self.hint_label.config(text=f"提示：答案在 {self.low} 到 {self.high} 之間")
        elif guess > self.target:
            self.high = min(self.high, guess - 1)
            self.status_label.config(text="再小一點！")
            self.hint_label.config(text=f"提示：答案在 {self.low} 到 {self.high} 之間")
        else:
            self.status_label.config(text="恭喜你猜中了！")
            self.hint_label.config(text=f"正確答案是 {self.target}，你總共猜了 {self.attempts} 次")
            messagebox.showinfo("完成", f"答對了！答案是 {self.target}，共猜了 {self.attempts} 次。")
            self.entry.delete(0, tk.END)
            self.entry.config(state="disabled")
            return

        self.entry.delete(0, tk.END)
        self.entry.focus_set()
        self.range_label.config(text=f"目前範圍：{self.low} - {self.high}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GuessNumberGame(root)
    root.mainloop()