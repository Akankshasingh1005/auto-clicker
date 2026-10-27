import os
import threading
import time
import tkinter as tk
from tkinter import filedialog
import pyautogui
from PIL import Image, ImageTk

# PyAutoGUI safety configuration
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05


class RetroAutoClicker(tk.Tk):

    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("Auto Clicker")
        self.geometry("740x840")
        self.resizable(False, False)
        # Deep muted lavender-slate base
        self.configure(bg="#2D2738")

        # Operational states
        self.running_detection = False
        self.running_interval = False
        self.target_image_path = None
        self.preview_image_ref = None

        self._build_ui()

    def _build_ui(self):
        # Outer arcade chassis border (Slate violet frame)
        outer_frame = tk.Frame(
            self,
            bg="#3B344A",
            relief="raised",
            bd=6,
            highlightbackground="#B8A8D8",
            highlightthickness=2,
        )
        outer_frame.pack(fill="both", expand=True, padx=8, pady=8)

        # --- ARCADE BANNER ---
        banner = tk.Frame(
            outer_frame,
            bg="#1E1926",
            relief="sunken",
            bd=4,
            height=54,
        )
        banner.pack(fill="x", padx=10, pady=(10, 8))
        banner.pack_propagate(False)

        title_lbl = tk.Label(
            banner,
            text="★ AUTO CLICKER ★",
            font=("Courier New", 18, "bold"),
            fg="#D9CEF2",
            bg="#1E1926",
        )
        title_lbl.pack(pady=4)

        sub_title = tk.Label(
            banner,
            text="[COMMAND AUTOMATION ENGINE ]",
            font=("Courier New", 8, "bold"),
            fg="#A799C7",
            bg="#1E1926",
        )
        sub_title.pack()

        # --- SECTION 1: TARGET MATCHER ---
        box_detect = tk.LabelFrame(
            outer_frame,
            text=" [ 01: SCREEN PATTERN LOCK ] ",
            font=("Courier New", 10, "bold"),
            bg="#3B344A",
            fg="#E4DBFA",
            relief="ridge",
            bd=4,
            labelanchor="nw",
        )
        box_detect.pack(fill="x", padx=10, pady=6)

        row_detect = tk.Frame(box_detect, bg="#3B344A")
        row_detect.pack(fill="x", padx=10, pady=8)

        # Target image preview screen
        preview_border = tk.Frame(
            row_detect,
            relief="sunken",
            bd=3,
            bg="#1E1926",
            width=150,
            height=84,
            highlightbackground="#9687B8",
            highlightthickness=1,
        )
        preview_border.pack(side="left", padx=(0, 12))
        preview_border.pack_propagate(False)

        self.preview_canvas = tk.Label(
            preview_border,
            text="NO TARGET\nDATA LOADED",
            bg="#1E1926",
            fg="#A799C7",
            font=("Courier New", 7, "bold"),
        )
        self.preview_canvas.pack(fill="both", expand=True)

        # File actions panel
        file_actions = tk.Frame(row_detect, bg="#3B344A")
        file_actions.pack(side="left", fill="both", expand=True)

        self.btn_browse = tk.Button(
            file_actions,
            text="[ LOAD TARGET IMG ]",
            font=("Courier New", 9, "bold"),
            fg="#1E1926",
            bg="#C4B5E6",
            activebackground="#D9CEF2",
            activeforeground="#1E1926",
            relief="raised",
            bd=3,
            command=self.select_image,
        )
        self.btn_browse.pack(anchor="w", pady=(0, 6))

        self.lbl_selected_file = tk.Label(
            file_actions,
            text="FILE: NONE",
            font=("Courier New", 8, "bold"),
            fg="#D9CEF2",
            bg="#3B344A",
            wraplength=340,
            justify="left",
        )
        self.lbl_selected_file.pack(anchor="w")

        # Start Detection Button
        self.btn_detect_toggle = tk.Button(
            box_detect,
            text="START PATTERN SCANNER",
            font=("Courier New", 11, "bold"),
            fg="#1E1926",
            bg="#D9CEF2",
            activebackground="#C4B5E6",
            activeforeground="#1E1926",
            relief="raised",
            bd=4,
            command=self.toggle_detection,
        )
        self.btn_detect_toggle.pack(fill="x", padx=10, pady=(4, 10))

        # --- SECTION 2: INTERVAL TIMER ---
        box_timer = tk.LabelFrame(
            outer_frame,
            text=" [ 02: AUTO TRIGGER PULSE ] ",
            font=("Courier New", 10, "bold"),
            bg="#3B344A",
            fg="#E4DBFA",
            relief="ridge",
            bd=4,
            labelanchor="nw",
        )
        box_timer.pack(fill="x", padx=10, pady=6)

        int_row = tk.Frame(box_timer, bg="#3B344A")
        int_row.pack(fill="x", padx=10, pady=8)

        lbl_pulse = tk.Label(
            int_row,
            text="PULSE ENTER EVERY:",
            font=("Courier New", 9, "bold"),
            fg="#D9CEF2",
            bg="#3B344A",
        )
        lbl_pulse.pack(side="left", padx=(0, 8))

        self.entry_interval = tk.Entry(
            int_row,
            width=8,
            font=("Courier New", 11, "bold"),
            relief="sunken",
            bd=3,
            bg="#1E1926",
            fg="#D9CEF2",
            insertbackground="#D9CEF2",
        )
        self.entry_interval.insert(0, "5")
        self.entry_interval.pack(side="left", padx=(0, 8))

        self.unit_var = tk.StringVar(value="Seconds")
        self.unit_menu = tk.OptionMenu(
            int_row, self.unit_var, "Seconds", "Minutes"
        )
        self.unit_menu.config(
            font=("Courier New", 9, "bold"),
            bg="#C4B5E6",
            fg="#1E1926",
            activebackground="#D9CEF2",
            relief="raised",
            bd=3,
            highlightthickness=0,
        )
        self.unit_menu["menu"].config(
            font=("Courier New", 9, "bold"),
            bg="#2D2738",
            fg="#E4DBFA",
            activebackground="#C4B5E6",
            activeforeground="#1E1926",
        )
        self.unit_menu.pack(side="left")

        self.btn_interval_toggle = tk.Button(
            box_timer,
            text="START INTERVAL PULSE",
            font=("Courier New", 11, "bold"),
            fg="#1E1926",
            bg="#D9CEF2",
            activebackground="#C4B5E6",
            activeforeground="#1E1926",
            relief="raised",
            bd=4,
            command=self.toggle_interval,
        )
        self.btn_interval_toggle.pack(fill="x", padx=10, pady=(4, 10))

        # --- SECTION 3: ARCADE MISSION HUD / INSTRUCTIONS ---
        box_hud = tk.LabelFrame(
            outer_frame,
            text=" [ 03: MISSION MANUAL & OVERRIDE ] ",
            font=("Courier New", 9, "bold"),
            bg="#3B344A",
            fg="#E4DBFA",
            relief="ridge",
            bd=4,
            labelanchor="nw",
        )
        box_hud.pack(fill="both", expand=True, padx=10, pady=6)

        hud_text = (
            "PRESSES 'ENTER' WHENEVER A TARGET OR TICK OCCURS.\n"
        )

        lbl_hud = tk.Label(
            box_hud,
            text=hud_text,
            font=("Courier New", 8, "bold"),
            fg="#B8A8D8",
            bg="#3B344A",
            justify="left",
        )
        lbl_hud.pack(anchor="w", padx=10, pady=8)

        # --- SECTION 4: RETRO FOOTER HUD ---
        footer = tk.Frame(outer_frame, bg="#1E1926", relief="sunken", bd=4)
        footer.pack(side="bottom", fill="x", padx=10, pady=(4, 8))

        # Left status pane
        self.lbl_status = tk.Label(
            footer,
            text="SYSTEM READY >> SELECT IMAGE TARGET",
            font=("Courier New", 8, "bold"),
            fg="#D9CEF2",
            bg="#1E1926",
            anchor="w",
        )
        self.lbl_status.pack(side="left", fill="x", expand=True, padx=8, pady=4)

        # Right status pane
        self.lbl_mode_state = tk.Label(
            footer,
            text="[ IDLE ]",
            font=("Courier New", 8, "bold"),
            fg="#A799C7",
            bg="#1E1926",
            anchor="e",
        )
        self.lbl_mode_state.pack(side="right", padx=8, pady=4)

    # --- File Selection & Preview Handling ---
    def select_image(self):
        filetypes = [
            ("Image files", "*.png *.jpg *.jpeg *.bmp"),
            ("PNG Files", "*.png"),
            ("JPEG Files", "*.jpg;*.jpeg"),
            ("All Files", "*.*"),
        ]
        chosen_path = filedialog.askopenfilename(
            title="SELECT TARGET MATRIX SNIPPET", filetypes=filetypes
        )
        if not chosen_path:
            return

        self.target_image_path = chosen_path
        filename = os.path.basename(chosen_path)
        self.lbl_selected_file.configure(text=f"FILE: {filename}")

        try:
            pil_img = Image.open(chosen_path)
            pil_img.thumbnail((124, 64))
            self.preview_image_ref = ImageTk.PhotoImage(pil_img)
            self.preview_canvas.configure(image=self.preview_image_ref, text="")
            self.set_status(f"LOADED >> {filename}")
        except Exception as e:
            self.set_status(f"ERR >> {str(e)}")

    # --- Screen Detection Thread ---
    def detection_loop(self):
        while self.running_detection:
            if not self.target_image_path or not os.path.exists(
                self.target_image_path
            ):
                self.set_status("ERR >> TARGET IMAGE LOST")
                self.toggle_detection()
                break

            try:
                match_pos = pyautogui.locateCenterOnScreen(
                    self.target_image_path, confidence=0.8
                )
                if match_pos is not None:
                    pyautogui.press("enter")
                    t_str = time.strftime("%H:%M:%S")
                    self.set_status(f"LOCK FOUND [{t_str}] >> ENTER")
                    time.sleep(1.8)
            except Exception:
                pass

            time.sleep(0.4)

    def toggle_detection(self):
        if not self.running_detection:
            if not self.target_image_path:
                self.set_status("ERR >> SELECT A TARGET IMAGE FIRST")
                return

            self.running_detection = True
            self.btn_detect_toggle.configure(
                text="STOP PATTERN SCANNER",
                bg="#8C7CA6",
                fg="#FFFFFF",
                relief="sunken",
            )
            self.lbl_mode_state.configure(text="[ SCANNING ]")
            self.set_status("SCANNER ENGAGED >> MONITORING DISPLAY")
            threading.Thread(target=self.detection_loop, daemon=True).start()
        else:
            self.running_detection = False
            self.btn_detect_toggle.configure(
                text="START PATTERN SCANNER",
                bg="#D9CEF2",
                fg="#1E1926",
                relief="raised",
            )
            self.lbl_mode_state.configure(
                text="[ PULSING ]" if self.running_interval else "[ IDLE ]"
            )
            self.set_status("SCANNER DISENGAGED")

    # --- Interval Pulse Thread ---
    def interval_loop(self, delay_sec):
        while self.running_interval:
            time.sleep(delay_sec)
            if not self.running_interval:
                break
            pyautogui.press("enter")
            t_str = time.strftime("%H:%M:%S")
            self.set_status(f"INTERVAL HIT [{t_str}] >> ENTER TRIGGERED")

    def toggle_interval(self):
        if not self.running_interval:
            try:
                val = float(self.entry_interval.get().strip())
                if val <= 0:
                    raise ValueError
            except ValueError:
                self.set_status("ERR >> PULSE VALUE MUST BE POSITIVE NUMBER")
                return

            unit = self.unit_var.get()
            delay = val * 60.0 if unit == "Minutes" else val

            self.running_interval = True
            self.btn_interval_toggle.configure(
                text="STOP INTERVAL PULSE",
                bg="#8C7CA6",
                fg="#FFFFFF",
                relief="sunken",
            )
            self.lbl_mode_state.configure(text="[ PULSING ]")
            self.set_status(f"PULSE ACTIVE >> TICK: {val} {unit.upper()}")
            threading.Thread(
                target=self.interval_loop, args=(delay,), daemon=True
            ).start()
        else:
            self.running_interval = False
            self.btn_interval_toggle.configure(
                text="START INTERVAL PULSE",
                bg="#D9CEF2",
                fg="#1E1926",
                relief="raised",
            )
            self.lbl_mode_state.configure(
                text="[ SCANNING ]" if self.running_detection else "[ IDLE ]"
            )
            self.set_status("INTERVAL PULSE STOPPED")

    def set_status(self, msg):
        self.lbl_status.configure(text=msg)


if __name__ == "__main__":
    app = RetroAutoClicker()
    app.mainloop()