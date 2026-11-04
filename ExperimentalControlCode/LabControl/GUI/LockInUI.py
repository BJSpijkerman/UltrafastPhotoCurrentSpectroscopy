import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Import the updated LockIn class from your module
from lockin_module import LockIn


class LockInGUI:

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("SR830 Lock-In Amplifier Control")
        self.root.geometry("1000x650")

        self.lockin = LockIn()
        self.is_monitoring = False

        self._build_ui()

    def _build_ui(self) -> None:
        # Main layout container
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left controls panel / Right live plots & readouts
        control_panel = ttk.Frame(main_frame, width=340)
        control_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        display_panel = ttk.Frame(main_frame)
        display_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- 1. Connection Panel ---
        conn_frame = ttk.LabelFrame(control_panel, text="Serial Connection", padding=10)
        conn_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(conn_frame, text="Port:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.port_var = tk.StringVar(value="COM3")
        ttk.Entry(conn_frame, textvariable=self.port_var, width=12).grid(
            row=0, column=1, sticky=tk.E, pady=2
        )

        ttk.Label(conn_frame, text="Baud Rate:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.baud_var = tk.IntVar(value=9600)
        ttk.Combobox(
            conn_frame,
            textvariable=self.baud_var,
            values=[2400, 4800, 9600, 19200],
            width=10,
            state="readonly",
        ).grid(row=1, column=1, sticky=tk.E, pady=2)

        self.btn_connect = ttk.Button(
            conn_frame, text="Connect Device", command=self._connect_device
        )
        self.btn_connect.grid(row=2, column=0, columnspan=2, pady=(8, 0), sticky=tk.EW)

        # --- 2. Reference & Signal Settings ---
        settings_frame = ttk.LabelFrame(
            control_panel, text="Device Settings", padding=10
        )
        settings_frame.pack(fill=tk.X, pady=(0, 10))

        # Internal vs External Reference
        self.ref_internal_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            settings_frame,
            text="Internal Reference",
            variable=self.ref_internal_var,
            command=self._on_ref_toggle,
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=2)

        # Reference Frequency (Hz)
        ttk.Label(settings_frame, text="Frequency (Hz):").grid(
            row=1, column=0, sticky=tk.W, pady=2
        )
        self.freq_var = tk.DoubleVar(value=500.0)
        self.ent_freq = ttk.Entry(settings_frame, textvariable=self.freq_var, width=10)
        self.ent_freq.grid(row=1, column=1, sticky=tk.E, pady=2)

        # Amplitude (V)
        ttk.Label(settings_frame, text="Amplitude (V):").grid(
            row=2, column=0, sticky=tk.W, pady=2
        )
        self.amp_var = tk.DoubleVar(value=1.0)
        self.ent_amp = ttk.Entry(settings_frame, textvariable=self.amp_var, width=10)
        self.ent_amp.grid(row=2, column=1, sticky=tk.E, pady=2)

        # Time Constant (tau index)
        ttk.Label(settings_frame, text="Time Constant (tau):").grid(
            row=3, column=0, sticky=tk.W, pady=2
        )
        self.tau_var = tk.IntVar(value=4)
        ttk.Spinbox(
            settings_frame, from_=0, to=19, textvariable=self.tau_var, width=8
        ).grid(row=3, column=1, sticky=tk.E, pady=2)

        # Sensitivity Gain
        ttk.Label(settings_frame, text="Gain Index:").grid(
            row=4, column=0, sticky=tk.W, pady=2
        )
        self.gain_var = tk.IntVar(value=26)
        ttk.Spinbox(
            settings_frame, from_=0, to=26, textvariable=self.gain_var, width=8
        ).grid(row=4, column=1, sticky=tk.E, pady=2)

        self.btn_apply = ttk.Button(
            settings_frame, text="Apply Configuration", command=self._apply_config, state=tk.DISABLED
        )
        self.btn_apply.grid(row=5, column=0, columnspan=2, pady=(10, 0), sticky=tk.EW)

        # --- 3. Live Readings Box ---
        readout_frame = ttk.LabelFrame(control_panel, text="Live Readings", padding=10)
        readout_frame.pack(fill=tk.X, pady=(0, 10))

        self.lbl_x = ttk.Label(readout_frame, text="X:  --- V", font=("Monospace", 11))
        self.lbl_x.pack(anchor=tk.W, pady=2)
        self.lbl_y = ttk.Label(readout_frame, text="Y:  --- V", font=("Monospace", 11))
        self.lbl_y.pack(anchor=tk.W, pady=2)
        self.lbl_r = ttk.Label(readout_frame, text="R:  --- V", font=("Monospace", 11))
        self.lbl_r.pack(anchor=tk.W, pady=2)
        self.lbl_theta = ttk.Label(readout_frame, text="θ:  --- deg", font=("Monospace", 11))
        self.lbl_theta.pack(anchor=tk.W, pady=2)

        self.btn_monitor = ttk.Button(
            readout_frame,
            text="Start Streaming",
            state=tk.DISABLED,
            command=self._toggle_monitoring,
        )
        self.btn_monitor.pack(fill=tk.X, pady=(8, 0))

        # --- 4. Live Plot Panel ---
        self.fig, (self.ax_mag, self.ax_phase) = plt.subplots(2, 1, figsize=(6, 5), dpi=100)
        self.fig.tight_layout(pad=3.0)

        self.ax_mag.set_title("Magnitude (R)")
        self.ax_mag.set_ylabel("Voltage (V)")
        self.ax_mag.grid(True)
        (self.line_r,) = self.ax_mag.plot([], [], "b-")

        self.ax_phase.set_title("Phase (Theta)")
        self.ax_phase.set_xlabel("Sample Count")
        self.ax_phase.set_ylabel("Degrees (°)")
        self.ax_phase.grid(True)
        (self.line_theta,) = self.ax_phase.plot([], [], "r-")

        self.canvas = FigureCanvasTkAgg(self.fig, master=display_panel)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.r_history = []
        self.theta_history = []

    def _on_ref_toggle(self) -> None:
        state = tk.NORMAL if self.ref_internal_var.get() else tk.DISABLED
        self.ent_freq.config(state=state)
        self.ent_amp.config(state=state)

    def _connect_device(self) -> None:
        self.lockin.set_baudrate(self.baud_var.get())
        port = self.port_var.get()

        try:
            if self.lockin.register(port):
                messagebox.showinfo("Success", f"Connected to Lock-In on {port}")
                self.btn_apply.config(state=tk.NORMAL)
                self.btn_monitor.config(state=tk.NORMAL)
                self.btn_connect.config(state=tk.DISABLED)
            else:
                messagebox.showerror("Error", f"Failed to connect on port {port}")
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))

    def _apply_config(self) -> None:
        try:
            self.lockin.set_reference(self.ref_internal_var.get())
            self.lockin.set_frequency(self.freq_var.get())
            self.lockin.set_amplitude(self.amp_var.get())
            self.lockin.set_tau(self.tau_var.get())
            self.lockin.set_gain(self.gain_var.get())

            self.lockin.configure()
            messagebox.showinfo("Success", "Lock-in settings updated.")
        except Exception as e:
            messagebox.showerror("Configuration Error", f"Failed to apply settings: {e}")

    def _toggle_monitoring(self) -> None:
        if self.is_monitoring:
            self.is_monitoring = False
            self.btn_monitor.config(text="Start Streaming")
        else:
            self.is_monitoring = True
            self.btn_monitor.config(text="Stop Streaming")
            threading.Thread(target=self._stream_readings, daemon=True).start()

    def _stream_readings(self) -> None:
        while self.is_monitoring:
            try:
                snap = self.lockin.acquire_snap()
                self.root.after(0, self._update_ui_readings, snap)
                time.sleep(0.1)
            except Exception as e:
                self.is_monitoring = False
                self.root.after(
                    0, lambda: messagebox.showerror("Readout Error", str(e))
                )
                break

    def _update_ui_readings(self, snap: dict) -> None:
        x, y = snap.get("X", 0.0), snap.get("Y", 0.0)
        r, theta = snap.get("R", 0.0), snap.get("Theta", 0.0)

        self.lbl_x.config(text=f"X:  {x:+.6f} V")
        self.lbl_y.config(text=f"Y:  {y:+.6f} V")
        self.lbl_r.config(text=f"R:  {r:+.6f} V")
        self.lbl_theta.config(text=f"θ:  {theta:+.2f} deg")

        # Keep last 100 data points for live streaming plots
        self.r_history.append(r)
        self.theta_history.append(theta)
        if len(self.r_history) > 100:
            self.r_history.pop(0)
            self.theta_history.pop(0)

        self.line_r.set_data(range(len(self.r_history)), self.r_history)
        self.line_theta.set_data(range(len(self.theta_history)), self.theta_history)

        self.ax_mag.relim()
        self.ax_mag.autoscale_view()
        self.ax_phase.relim()
        self.ax_phase.autoscale_view()

        self.canvas.draw_idle()

    def on_close(self) -> None:
        self.is_monitoring = False
        try:
            self.lockin.disconnect()
        except Exception:
            pass
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = LockInGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
