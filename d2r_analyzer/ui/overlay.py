import tkinter as tk
from typing import TypeAlias

from d2r_analyzer.llm.parser import EvaluationSchema

FontSpec: TypeAlias = tuple[str, int] | tuple[str, int, str]
PadOptions: TypeAlias = dict[str, int | tuple[int, int]]

# ── Grade colors ───────────────────────────────────────────
GRADE_COLORS: dict[str, str] = {
    "S": "#FFD700",  # gold
    "A": "#00FF00",  # green
    "B": "#4FC3F7",  # blue
    "C": "#FFA500",  # orange
    "D": "#FF4444",  # red
}

VERDICT_COLORS: dict[str, str] = {
    "KEEP": "#00FF00",
    "KEEP_FOR_ALT": "#4FC3F7",
    "TRASH": "#FF4444",
    "UNSURE": "#FFA500",
}


# ── Main overlay class ─────────────────────────────────────
class ItemOverlay:
    def __init__(self, auto_close_ms: int = 8000) -> None:
        self.auto_close_ms = auto_close_ms
        self._root = tk.Tk()
        self._root.withdraw()
        self._window: tk.Toplevel | None = None
        self._close_job: str | None = None

    @property
    def root(self) -> tk.Tk:
        return self._root

    def show(self, evaluation: EvaluationSchema, x: int, y: int) -> None:
        """Render the overlay near (x, y) without blocking the caller."""
        win = self._create_window()

        # ── Build content ──────────────────────────────────
        self._build_ui(win, evaluation)

        self._position_window(win, x, y)

        # ── Close on Escape or click ──────────────────────
        win.bind("<Escape>", lambda e: self.close())
        win.bind("<Button-1>", lambda e: self.close())
        win.focus_force()

        self._close_job = win.after(self.auto_close_ms, self.close)

    def show_status(
        self, text: str, x: int, y: int, auto_close_ms: int | None = None
    ) -> None:
        """Render a compact status overlay while background work is running."""
        win = self._create_window()
        bg = "#1A1008"

        container = tk.Frame(win, bg=bg)
        container.pack(fill="both", expand=True, padx=12, pady=10)

        tk.Label(
            container,
            text=text,
            fg="#C8A96E",
            bg=bg,
            font=("Palatino Linotype", 11, "bold"),
            justify="left",
            anchor="w",
        ).pack(fill="x")

        tk.Label(
            container,
            text="Please wait...",
            fg="#8E6A3A",
            bg=bg,
            font=("Palatino Linotype", 9),
            justify="left",
            anchor="w",
        ).pack(fill="x", pady=(4, 0))

        self._position_window(win, x, y)

        win.bind("<Escape>", lambda e: self.close())
        win.bind("<Button-1>", lambda e: self.close())
        win.focus_force()

        if auto_close_ms is not None:
            self._close_job = win.after(auto_close_ms, self.close)

    def close(self) -> None:
        if self._window:
            if self._close_job:
                try:
                    self._window.after_cancel(self._close_job)
                except tk.TclError:
                    pass
                self._close_job = None
            self._window.destroy()
            self._window = None

    def process_events(self) -> None:
        """Pump Tk events without entering a blocking mainloop."""
        self._root.update_idletasks()
        self._root.update()

    def _create_window(self) -> tk.Toplevel:
        if self._window:
            self.close()

        win = tk.Toplevel(self._root)
        self._window = win

        # Window setup shared by result and status overlays.
        win.overrideredirect(True)
        win.attributes("-topmost", True)
        win.attributes("-alpha", 0.93)
        win.configure(bg="#1A1008")
        return win

    def _position_window(self, win: tk.Toplevel, x: int, y: int) -> None:
        win.update_idletasks()
        w = win.winfo_width()
        h = win.winfo_height()
        sw = win.winfo_screenwidth()
        sh = win.winfo_screenheight()

        px = min(x + 20, sw - w - 10)
        py = min(y + 20, sh - h - 10)
        win.geometry(f"+{px}+{py}")

    def _build_ui(self, win: tk.Misc, ev: EvaluationSchema) -> None:
        FONT_TITLE: FontSpec = ("Palatino Linotype", 13, "bold")
        FONT_LABEL: FontSpec = ("Palatino Linotype", 10, "bold")
        FONT_BODY: FontSpec = ("Palatino Linotype", 9)
        BG: str = "#1A1008"
        DIVIDER: str = "#5C3D11"

        grade_color = GRADE_COLORS.get(ev.grade.upper(), "#FFFFFF")
        verdict_color = VERDICT_COLORS.get(ev.verdict.upper(), "#FFFFFF")

        pad: PadOptions = {"padx": 14, "pady": 3}

        # ── Grade + Verdict header ──────────────────────────
        header = tk.Frame(win, bg=BG)
        header.pack(fill="x", padx=14, pady=(12, 4))

        tk.Label(
            header,
            text=f"Grade: {ev.grade}",
            fg=grade_color,
            bg=BG,
            font=("Palatino Linotype", 18, "bold"),
        ).pack(side="left", padx=(0, 14))

        tk.Label(
            header,
            text=ev.verdict.replace("_", " "),
            fg=verdict_color,
            bg=BG,
            font=FONT_TITLE,
        ).pack(side="left")

        _divider(win, DIVIDER)

        # ── Best build ─────────────────────────────────────
        if ev.best_build:
            row(
                win,
                "Best for:",
                ev.best_build,
                "#C8A96E",
                BG,
                FONT_LABEL,
                FONT_BODY,
                pad,
            )
            _divider(win, DIVIDER)

        # ── Trade value + roll quality ──────────────────────
        row(
            win,
            "Trade value:",
            ev.trade_value.capitalize(),
            "#C8A96E",
            BG,
            FONT_LABEL,
            FONT_BODY,
            pad,
        )
        row(
            win,
            "Roll quality:",
            ev.roll_quality.capitalize(),
            "#C8A96E",
            BG,
            FONT_LABEL,
            FONT_BODY,
            pad,
        )
        _divider(win, DIVIDER)

        # ── Good affixes ───────────────────────────────────
        if ev.good_affixes:
            tk.Label(
                win,
                text="✔ Good affixes",
                fg="#00FF00",
                bg=BG,
                font=FONT_LABEL,
                anchor="w",
            ).pack(fill="x", **pad)
            for affix in ev.good_affixes:
                tk.Label(
                    win,
                    text=f"  {affix}",
                    fg="#A8D8A8",
                    bg=BG,
                    font=FONT_BODY,
                    anchor="w",
                ).pack(fill="x", padx=14)

        # ── Wasted slots ────────────────────────────────────
        if ev.wasted_slots:
            tk.Label(
                win,
                text="✘ Wasted slots",
                fg="#FF4444",
                bg=BG,
                font=FONT_LABEL,
                anchor="w",
            ).pack(fill="x", **pad)
            for slot in ev.wasted_slots:
                tk.Label(
                    win,
                    text=f"  {slot}",
                    fg="#D08080",
                    bg=BG,
                    font=FONT_BODY,
                    anchor="w",
                ).pack(fill="x", padx=14)

        _divider(win, DIVIDER)

        # ── Reasoning ──────────────────────────────────────
        tk.Label(
            win,
            text=ev.reasoning,
            fg="#C8A96E",
            bg=BG,
            font=FONT_BODY,
            wraplength=280,
            justify="left",
            anchor="w",
        ).pack(fill="x", padx=14, pady=(4, 10))

        # ── Dismiss hint ───────────────────────────────────
        tk.Label(
            win,
            text="ESC or click to dismiss",
            fg="#5C3D11",
            bg=BG,
            font=("Palatino Linotype", 7),
        ).pack(pady=(0, 6))


# ── Helpers ────────────────────────────────────────────────


def _divider(parent: tk.Misc, color: str) -> None:
    tk.Frame(parent, bg=color, height=1).pack(fill="x", padx=10, pady=2)


def row(
    parent: tk.Misc,
    label: str,
    value: str,
    label_color: str,
    bg: str,
    label_font: FontSpec,
    val_font: FontSpec,
    pad: PadOptions,
) -> None:
    f = tk.Frame(parent, bg=bg)
    f.pack(fill="x", **pad)
    tk.Label(f, text=label, fg=label_color, bg=bg, font=label_font).pack(side="left")
    tk.Label(f, text=f"  {value}", fg="#FFFFFF", bg=bg, font=val_font).pack(side="left")
