import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk

# Import corrected Stage class from your module
from stage_module import Stage


class StageGUI:

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Motorized Stage Controller")
        self.root.geometry("450x520")
        self.root.resizable(False, False)

        self.stage = Stage()
        self.is_connected = False
        self.is_polling = False

        self._build_ui()

    def _build_ui(self) -> None:
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- 1. Serial Connection Frame ---
        conn_frame = ttk.LabelFrame(main_frame, text="Connection", padding=10)
        conn_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(conn_frame, text="Port Name:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.port_var = tk.StringVar(value="COM4")
        ttk.Entry(conn_frame, textvariable=self.port_var, width=15).grid(
            row=0, column=1, padx=(5, 5), pady=2
        )

        self.btn_connect = ttk.Button(
            conn_frame, text="Connect", command=self._toggle_connection
        )
        self.btn_connect.grid(row=0, column=2, padx=(5, 0), pady=2)

        # --- 2. Live Position Display ---
        pos_frame = ttk.LabelFrame(main_frame, text="Current Position", padding=15)
        pos_frame.pack(fill=tk.X, pady=(0, 10))

        self.lbl_position = tk.Label(
            pos_frame,
            text="0.0000 mm",
            font=("Consolas", 26, "bold"),
            bg="#1e1e1e",
            fg="#00ffcc",
            pady=10,
        )
        self.lbl_position.pack(fill=tk.X)

        # --- 3. Jog / Relative Movement ---
        jog_frame = ttk.LabelFrame(main_frame, text="Relative Movement (Jog)", padding=10)
        jog_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(jog_frame, text="Step Size (mm):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.step_var = tk.DoubleVar(value=1.0)
        step_combo = ttk.Combobox(
            jog_frame,
            textvariable=self.step_var,
            values=[0.001, 0.01, 0.1, 1.0, 5.0, 10.0],
            width=8,
            state="readonly",
        )
        step_combo.grid(row=0, column=1, columnspan=2, sticky=tk.W, padx=5, pady=5)

        self.btn_jog_neg = ttk.Button(
            jog_frame, text="◀ Jog -", command=lambda: self._move_stage("-"), state=tk.DISABLED
        )
        self.btn_jog_neg.grid(row=1, column=0, sticky=tk.EW, padx=2, pady=5)

        self.btn_jog_pos = ttk.Button(
            jog_frame, text="Jog + ▶", command=lambda: self._move_stage("+"), state=tk.DISABLED
        )
        self.btn_jog_pos.grid(row=1, column=2, sticky=tk.EW, padx=2, pady=5)

        # --- 4. Absolute Movement ---
        abs_frame = ttk.LabelFrame(main_frame, text="Absolute Movement", padding=10)
        abs_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(abs_frame, text="Target (mm):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.abs_target_var = tk.DoubleVar(value=0.0)
        ttk.Entry(abs_frame, textvariable=self.abs_target_var, width=12).grid(
            row=0, column=1, padx=5, pady=2
        )

        self.btn_move_abs = ttk.Button(
            abs_frame, text="Move Absolute", command=lambda: self._move_stage("="), state=tk.DISABLED
        )
        self.btn_move_abs.grid(row=0, column=2, padx=5, pady=2)

        # --- 5. Controls & E-Stop ---
        ctrl_frame = ttk.Frame(main_frame)
        ctrl_frame.pack(fill=tk.X, pady=(5, 0))

        self.btn_home = ttk.Button(
            ctrl_frame, text="Home Stage", command=self._home_stage, state=tk.DISABLED
        )
        self.btn_home.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        self.btn_stop = tk.Button(
            ctrl_frame,
            text="STOP",
            bg="#cc0000",
            fg="white",
            font=("Helvetica", 10, "bold"),
            command=self._stop_stage,
            state=tk.DISABLED,
        )
        self.btn_stop.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))

    def _toggle_connection(self) -> None:
        if not self.is_connected:
            port = self.port_var.get()
            try:
                self.stage.connect(port)
                self.is_connected = True
                self.btn_connect.config(text="Disconnect")
                self._set_controls_state(tk.NORMAL)

                # Start continuous position polling thread
                self.is_polling = True
                threading.Thread(target=self._poll_position, daemon=True).start()
            except Exception as e:
                messagebox.showerror("Connection Error", f"Failed to connect to port {port}:\n{e}")
        else:
            self.is_polling = False
            try:
                self.stage.disconnect()
            except Exception:
                pass
            self.is_connected = False
            self.btn_connect.config(text="Connect")
            self._set_controls_state(tk.DISABLED)
            self.lbl_position.config(text="0.0000 mm")

    def _set_controls_state(self, state: str) -> None:
        self.btn_jog_neg.config(state=state)
        self.btn_jog_pos.config(state=state)
        self.btn_move_abs.config(state=state)
        self.btn_home.config(state=state)
        self.btn_stop.config(state=state)

    def _move_stage(self, mode: str) -> None:
        if not self.is_connected:
            return

        threading.Thread(
            target=self._exec_move, args=(mode,), daemon=True
        ).start()

    def _exec_move(self, mode: str) -> None:
        try:
            if mode == "+":
                cmd = f"+{self.step_var.get()}"
            elif mode == "-":
                cmd = f"-{self.step_var.get()}"
            elif mode == "=":
                cmd = f"={self.abs_target_var.get()}"
            else:
                return

            self.stage.move(cmd)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Movement Error", str(e)))

    def _home_stage(self) -> None:
        threading.Thread(target=self.stage.home, daemon=True).start()

    def _stop_stage(self) -> None:
        self.stage.stop()

    def _poll_position(self) -> None:
        while self.is_polling and self.is_connected:
            try:
                pos = self.stage.get_position()
                self.root.after(0, lambda p=pos: self.lbl_position.config(text=f"{p:.4f} mm"))
                time.sleep(0.1)
            except Exception:
                break

    def on_close(self) -> None:
        self.is_polling = False
        if self.is_connected:
            try:
                self.stage.disconnect()
            except Exception:
                pass
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = StageGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
