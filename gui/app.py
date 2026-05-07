import os
import sys
import time
import cv2
import customtkinter as ctk

from PIL import Image, ImageTk
from tkinter import filedialog

# =========================
# FIX IMPORT PATH
# =========================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

# =========================
# IMPORT SYSTEM
# =========================
from inference.detector import detect
from processing.logic import DecisionSystem
from utils.video import open_source
from utils.logger import log

# =========================
# UI CONFIG
# =========================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# =========================
# APP
# =========================
class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        # =========================
        # WINDOW
        # =========================
        self.title("AI Vision Modern Control Room")
        self.geometry("1600x900")

        # =========================
        # SYSTEM
        # =========================
        self.cap = None
        self.running = False
        self.after_id = None

        self.logic = DecisionSystem()

        self.current_video = "No Source"
        self.frame_count = 0
        self.alert_count = 0
        self.start_time = time.time()

        # =========================
        # UI
        # =========================
        self.build_ui()

        # =========================
        # CLOCK
        # =========================
        self.update_clock()

    # =========================================================
    # UI
    # =========================================================
    def build_ui(self):

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # =====================================================
        # TOP BAR
        # =====================================================
        top = ctk.CTkFrame(self, height=70, corner_radius=0)
        top.grid(row=0, column=0, sticky="ew")

        top.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            top,
            text="🛡 AI Vision Modern Control Room",
            font=("Arial", 32, "bold")
        )
        title.grid(row=0, column=0, padx=20, pady=15, sticky="w")

        self.clock_label = ctk.CTkLabel(
            top,
            text="00:00:00",
            font=("Arial", 20)
        )
        self.clock_label.grid(row=0, column=1, padx=20)

        # =====================================================
        # MAIN
        # =====================================================
        main = ctk.CTkFrame(self)
        main.grid(row=1, column=0, sticky="nsew")

        main.grid_columnconfigure(0, weight=5)
        main.grid_columnconfigure(1, weight=1)

        main.grid_rowconfigure(0, weight=1)

        # =====================================================
        # LEFT
        # =====================================================
        left = ctk.CTkFrame(main)
        left.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        left.grid_rowconfigure(0, weight=1)
        left.grid_columnconfigure(0, weight=1)

        # VIDEO FRAME
        video_frame = ctk.CTkFrame(left, fg_color="#111111")
        video_frame.grid(row=0, column=0, sticky="nsew")

        video_frame.grid_rowconfigure(0, weight=1)
        video_frame.grid_columnconfigure(0, weight=1)

        self.video_label = ctk.CTkLabel(video_frame, text="")
        self.video_label.grid(row=0, column=0, sticky="nsew")

        # ==========================================
        # VIDEO CONTROLS
        # ==========================================
        controls = ctk.CTkFrame(left, height=80)
        controls.grid(row=1, column=0, sticky="ew", pady=10)

        self.load_btn = ctk.CTkButton(
            controls,
            text="📂 Load Video",
            command=self.load_video,
            width=150,
            height=40
        )
        self.load_btn.pack(side="left", padx=10, pady=15)

        self.camera_btn = ctk.CTkButton(
            controls,
            text="🌐 Open Stream",
            command=self.open_stream,
            width=150,
            height=40
        )
        self.camera_btn.pack(side="left", padx=10)

        self.start_btn = ctk.CTkButton(
            controls,
            text="▶ Start",
            command=self.start_video,
            width=120,
            height=40
        )
        self.start_btn.pack(side="left", padx=10)

        self.stop_btn = ctk.CTkButton(
            controls,
            text="⏹ Stop",
            command=self.stop_video,
            width=120,
            height=40,
            fg_color="red"
        )
        self.stop_btn.pack(side="left", padx=10)

        # ==========================================
        # BOTTOM STATS
        # ==========================================
        stats = ctk.CTkFrame(left, height=80)
        stats.grid(row=2, column=0, sticky="ew")

        self.fps_label = ctk.CTkLabel(stats, text="FPS: 0")
        self.fps_label.pack(side="left", padx=20, pady=15)

        self.object_label = ctk.CTkLabel(stats, text="Objects: 0")
        self.object_label.pack(side="left", padx=20)

        self.alerts_label = ctk.CTkLabel(stats, text="Alerts: 0")
        self.alerts_label.pack(side="left", padx=20)

        self.source_label = ctk.CTkLabel(stats, text="Source: None")
        self.source_label.pack(side="left", padx=20)

        # =====================================================
        # RIGHT PANEL
        # =====================================================
        right = ctk.CTkFrame(main, width=350)
        right.grid(row=0, column=1, sticky="ns", padx=15, pady=15)

        right.grid_propagate(False)

        # STATUS
        status_title = ctk.CTkLabel(
            right,
            text="🚨 SYSTEM STATUS",
            font=("Arial", 24, "bold")
        )
        status_title.pack(pady=15)

        self.alert_box = ctk.CTkLabel(
            right,
            text="SAFE",
            fg_color="green",
            height=80,
            corner_radius=15,
            font=("Arial", 28, "bold")
        )
        self.alert_box.pack(fill="x", padx=15)

        # INFO
        info_title = ctk.CTkLabel(
            right,
            text="📄 DETECTION INFO",
            font=("Arial", 20, "bold")
        )
        info_title.pack(pady=15)

        self.info_box = ctk.CTkTextbox(
            right,
            height=180,
            font=("Consolas", 15)
        )
        self.info_box.pack(fill="x", padx=15)

        # HISTORY
        history_title = ctk.CTkLabel(
            right,
            text="📜 ALERT HISTORY",
            font=("Arial", 20, "bold")
        )
        history_title.pack(pady=15)

        self.history_box = ctk.CTkTextbox(
            right,
            font=("Consolas", 14)
        )
        self.history_box.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

    # =========================================================
    # CLOCK
    # =========================================================
    def update_clock(self):
        self.clock_label.configure(
            text=time.strftime("%H:%M:%S")
        )
        self.after(1000, self.update_clock)

    # =========================================================
    # LOAD VIDEO
    # =========================================================
    def load_video(self):

        path = filedialog.askopenfilename(
            filetypes=[("Video Files", "*.mp4 *.avi *.mov")]
        )

        if not path:
            return

        self.cap = open_source(path)

        self.current_video = os.path.basename(path)

        self.source_label.configure(
            text=f"Source: {self.current_video}"
        )

    # =========================================================
    # STREAM
    # =========================================================
    def open_stream(self):

        url = ctk.CTkInputDialog(
            text="Enter RTSP / Stream URL",
            title="Open Stream"
        ).get_input()

        if not url:
            return

        self.cap = open_source(url)

        self.current_video = url

        self.source_label.configure(
            text="Source: Live Stream"
        )

    # =========================================================
    # START
    # =========================================================
    def start_video(self):

        if self.cap is None:
            return

        self.running = True

        self.loop()

    # =========================================================
    # STOP
    # =========================================================
    def stop_video(self):

        self.running = False

        if self.after_id:
            self.after_cancel(self.after_id)

    # =========================================================
    # LOOP
    # =========================================================
    def loop(self):

        if not self.running:
            return

        start = time.time()

        ret, frame = self.cap.read()

        if not ret:
            self.stop_video()
            return

        detections = detect(frame)

        detection_text = ""

        simple = []

        for name, conf, box in detections:

            simple.append((name, conf))

            x1, y1, x2, y2 = map(int, box)

            detection_text += (
                f"Type : {name}\n"
                f"Conf : {conf:.2f}\n"
                f"Time : {time.strftime('%H:%M:%S')}\n\n"
            )

        # ==========================================
        # DECISION LOGIC
        # ==========================================
        alert = self.logic.check(simple)

        # ==========================================
        # DRAW
        # ==========================================
        for name, conf, box in detections:

            x1, y1, x2, y2 = map(int, box)

            color = (0, 0, 255) if alert else (0, 255, 0)

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                color,
                3
            )

            cv2.putText(
                frame,
                f"{name} {conf:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2
            )

        # ==========================================
        # ALERT UI
        # ==========================================
        if alert:

            self.alert_box.configure(
                text="EMERGENCY DETECTED",
                fg_color="red"
            )

            self.alert_count += 1

            line = (
                f"[{time.strftime('%H:%M:%S')}] "
                f"Emergency Vehicle Detected\n"
            )

            self.history_box.insert("end", line)
            self.history_box.see("end")

            log(line)

        else:

            self.alert_box.configure(
                text="SAFE",
                fg_color="green"
            )

        # ==========================================
        # INFO
        # ==========================================
        self.info_box.delete("1.0", "end")
        self.info_box.insert(
            "end",
            detection_text if detection_text else "No Detection"
        )

        # ==========================================
        # VIDEO RESIZE
        # ==========================================
        h, w = frame.shape[:2]

        max_w = 1200
        max_h = 700

        scale = min(max_w / w, max_h / h)

        nw = int(w * scale)
        nh = int(h * scale)

        frame = cv2.resize(frame, (nw, nh))

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        img = Image.fromarray(frame)

        imgtk = ImageTk.PhotoImage(img)

        self.video_label.configure(image=imgtk)
        self.video_label.image = imgtk

        # ==========================================
        # FPS
        # ==========================================
        fps = 1 / (time.time() - start)

        self.fps_label.configure(
            text=f"FPS: {fps:.1f}"
        )

        self.object_label.configure(
            text=f"Objects: {len(detections)}"
        )

        self.alerts_label.configure(
            text=f"Alerts: {self.alert_count}"
        )

        self.after_id = self.after(30, self.loop)

# =============================================================
# RUN
# =============================================================
if __name__ == "__main__":

    app = App()

    app.mainloop()