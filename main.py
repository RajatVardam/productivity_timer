def main():
    print("Hello from productivity-timer!")


if __name__ == "__main__":
    main()
import tkinter as tk
from tkinter import ttk
from time import perf_counter

class Stopwatch:
    INACTIVE_BG = '#f8f9fa'
    FG_COLOR    = '#0f5132'

    def __init__(self, parent, title, active_bg, click_callback):
        self.start_time = 0.0
        self.elapsed    = 0.0
        self.running    = False
        self.active_bg  = active_bg

        self.frame = tk.Frame(
            parent,
            bg=self.INACTIVE_BG,
            bd=2,
            relief='groove',
            padx=20,
            pady=20
        )
        self.frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)

        self.label = tk.Label(
            self.frame,
            text=title,
            font=('Helvetica', 16, 'bold'),
            bg=self.INACTIVE_BG,
            fg=self.FG_COLOR
        )
        self.label.pack(pady=(0, 10))

        self.time_display = tk.Label(
            self.frame,
            text="00:00:00.00",
            font=('Courier', 36),
            bg=self.INACTIVE_BG,
            fg=self.FG_COLOR,
            width=10
        )
        self.time_display.pack(expand=True, fill=tk.BOTH)
        # bind click to toggle
        self.time_display.bind("<Button-1>", lambda e: click_callback())

    def _format(self, seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return f"{int(h):02}:{int(m):02}:{s:05.2f}"

    def highlight(self, active: bool):
        bg = self.active_bg if active else self.INACTIVE_BG
        for widget in (self.frame, self.label, self.time_display):
            widget.config(bg=bg)

    def start(self):
        if not self.running:
            self.start_time = perf_counter() - self.elapsed
            self.running    = True
            self.highlight(True)
            self._update()

    def stop(self):
        if self.running:
            self.elapsed = perf_counter() - self.start_time
            self.running = False
            self.highlight(False)

    def reset(self):
        self.stop()
        self.elapsed = 0.0
        self.time_display.config(text=self._format(0.0))

    def _update(self):
        if self.running:
            self.elapsed = perf_counter() - self.start_time
            self.time_display.config(text=self._format(self.elapsed))
            self.time_display.after(50, self._update)


class DualStopwatchApp:
    def __init__(self, root):
        root.title("Productivity Timer")
        root.geometry("960x400")
        root.minsize(700, 350)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Helvetica', 12), padding=6)

        container = tk.Frame(root)
        for i in range(3):
            container.columnconfigure(i, weight=1)
        container.pack(expand=True, fill=tk.BOTH)

        # Pass the toggle handlers instead of plain start
        self.sw_a = Stopwatch(
            container,
            title='Productive',
            active_bg='#d1e7dd',
            click_callback=self.toggle_a
        )

        control_frame = tk.Frame(container)
        control_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)
        control_frame.rowconfigure(0, weight=1)
        control_frame.rowconfigure(1, weight=1)
        control_frame.columnconfigure(0, weight=1)

        ttk.Button(
            control_frame,
            text="Reset Both",
            command=self.reset_both
        ).grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        ttk.Button(
            control_frame,
            text="Pause",
            command=self.pause_active
        ).grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        self.sw_b = Stopwatch(
            container,
            title='Idle',
            active_bg='#f8d7da',
            click_callback=self.toggle_b
        )

    def toggle_a(self):
        if self.sw_a.running:
            self.sw_a.stop()
        else:
            self.sw_b.stop()
            self.sw_a.start()

    def toggle_b(self):
        if self.sw_b.running:
            self.sw_b.stop()
        else:
            self.sw_a.stop()
            self.sw_b.start()

    def reset_both(self):
        self.sw_a.reset()
        self.sw_b.reset()

    def pause_active(self):
        if self.sw_a.running:
            self.sw_a.stop()
        elif self.sw_b.running:
            self.sw_b.stop()


if __name__ == "__main__":
    root = tk.Tk()
    DualStopwatchApp(root)
    root.mainloop()