import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Import your existing class implementation
from LabControl.Devices.PCspectroscopy import PCspectroscopy


class PCspectroscopyGUI:

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("PC Spectroscopy Measurement Control")
        self.root.geometry("1100x700")

        self.spectroscopy: PCspectroscopy | None = None
        self.is_running = False

        self._build_ui()

    def _build_ui(self) -> None:
        # Main layout container
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left control panel / Right plot view
        control_panel = ttk.Frame(main_frame, width=320)
        control_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        plot_panel = ttk.Frame(main_frame)
        plot_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- 1. File Selection Group ---
        file_frame = ttk.LabelFrame(control_panel, text="Data Storage", padding=10)
        file_frame.pack(fill=tk.X, pady=(0, 10))

        self.hdf5_path_var = tk.StringVar(value="measurement.h5")
        ttk.Entry(file_frame, textvariable=self.hdf5_path_var).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5)
        )
        ttk.Button(file_frame, text="Browse", command=self._browse_file).pack(
            side=tk.RIGHT
        )

        # --- 2. Hardware Connection Group ---
        hw_frame = ttk.LabelFrame(
            control_panel, text="Hardware Ports", padding=10
        )
        hw_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(hw_frame, text="Lock-in Port:").grid(
            row=0, column=0, sticky=tk.W, pady=2
        )
        self.lockin_port_var = tk.StringVar(value="COM3")
        ttk.Entry(hw_frame, textvariable=self.lockin_port_var, width=12).grid(
            row=0, column=1, sticky=tk.E, pady=2
        )

        ttk.Label(hw_frame, text="Delay Stage Port:").grid(
            row=1, column=0, sticky=tk.W, pady=2
        )
        self.stage_port_var = tk.StringVar(value="COM4")
        ttk.Entry(hw_frame, textvariable=self.stage_port_var, width=12).grid(
            row=1, column=1, sticky=tk.E, pady=2
        )

        self.btn_connect = ttk.Button(
            hw_frame, text="Connect Hardware", command=self._connect_hardware
        )
        self.btn_connect.grid(row=2, column=0, columnspan=2, pady=(8, 0), sticky=tk.EW)

        # --- 3. Scan & Lock-in Settings ---
        param_frame = ttk.LabelFrame(
            control_panel, text="Scan Parameters", padding=10
        )
        param_frame.pack(fill=tk.X, pady=(0, 10))

        # Sweep range
        ttk.Label(param_frame, text="Start (ps/mm):").grid(
            row=0, column=0, sticky=tk.W, pady=2
        )
        self.start_var = tk.DoubleVar(value=-5.0)
        ttk.Entry(param_frame, textvariable=self.start_var, width=10).grid(
            row=0, column=1, sticky=tk.E, pady=2
        )

        ttk.Label(param_frame, text="Stop (ps/mm):").grid(
            row=1, column=0, sticky=tk.W, pady=2
        )
        self.stop_var = tk.DoubleVar(value=15.0)
        ttk.Entry(param_frame, textvariable=self.stop_var, width=10).grid(
            row=1, column=1, sticky=tk.E, pady=2
        )

        ttk.Label(param_frame, text="Step Size:").grid(
            row=2, column=0, sticky=tk.W, pady=2
        )
        self.step_var = tk.DoubleVar(value=0.1)
        ttk.Entry(param_frame, textvariable=self.step_var, width=10).grid(
            row=2, column=1, sticky=tk.E, pady=2
        )

        ttk.Label(param_frame, text="Cycles:").grid(
            row=3, column=0, sticky=tk.W, pady=2
        )
        self.cycles_var = tk.IntVar(value=2)
        ttk.Entry(param_frame, textvariable=self.cycles_var, width=10).grid(
            row=3, column=1, sticky=tk.E, pady=2
        )

        ttk.Label(param_frame, text="Time Zero (mm):").grid(
            row=4, column=0, sticky=tk.W, pady=2
        )
        self.tzero_var = tk.DoubleVar(value=0.0)
        ttk.Entry(param_frame, textvariable=self.tzero_var, width=10).grid(
            row=4, column=1, sticky=tk.E, pady=2
        )

        # --- 4. Controls & Progress ---
        action_frame = ttk.Frame(control_panel, padding=5)
        action_frame.pack(fill=tk.X, pady=(10, 0))

        self.btn_start = ttk.Button(
            action_frame,
            text="Start Scan",
            state=tk.DISABLED,
            command=self._start_scan_thread,
        )
        self.btn_start.pack(fill=tk.X, pady=(0, 10))

        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            action_frame, variable=self.progress_var, maximum=100
        )
        self.progress_bar.pack(fill=tk.X)

        self.status_label = ttk.Label(
            action_frame, text="Status: Disconnected", foreground="gray"
        )
        self.status_label.pack(anchor=tk.W, pady=(5, 0))

        # --- 5. Matplotlib Live Plot ---
        self.fig, self.ax = plt.subplots(figsize=(6, 4), dpi=100)
        self.ax.set_title("Live Measurement Current")
        self.ax.set_xlabel("Position / Delay")
        self.ax.set_ylabel("Signal (V / A)")
        self.ax.grid(True)

        (self.line_x,) = self.ax.plot([], [], "b.-", label="Channel X")
        (self.line_y,) = self.ax.plot([], [], "r.-", label="Channel Y")
        self.ax.legend(loc="upper right")

        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_panel)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _browse_file() -> None:
        filepath = filedialog.asksaveasfilename(
            defaultextension=".h5",
            filetypes=[("HDF5 Files", "*.h5 *.hdf5"), ("All Files", "*.*")],
        )
        if filepath:
            self.hdf5_path_var.set(filepath)

    def _connect_hardware() -> None:
        h5_path = self.hdf5_path_var.get()
        if not h5_path:
            messagebox.showerror("Error", "Please select a valid HDF5 file path.")
            return

        try:
            # Instantiate spectroscopy engine and connect
            self.spectroscopy = PCspectroscopy(h5_path)
            self.spectroscopy.connect_devices(
                lockin_port=self.lockin_port_var.get(),
                stage_port=self.stage_port_var.get(),
            )
            self.status_label.config(
                text="Status: Connected", foreground="green"
            )
            self.btn_start.config(state=tk.NORMAL)
            self.btn_connect.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {e}")
            self.status_label.config(
                text="Status: Connection Failed", foreground="red"
            )

    def _start_scan_thread() -> None:
        if self.is_running or not self.spectroscopy:
            return

        # Pass GUI parameters to class
        params = {
            "N_cycles": self.cycles_var.get(),
            "stage": {"time_zero_mm": self.tzero_var.get()},
            "lockin": {"internal_ref": False, "time_constant": 1, "gain": 16},
        }

        self.spectroscopy.set_parameters(params)
        self.spectroscopy.add_delay_steps(
            self.start_var.get(), self.stop_var.get(), self.step_var.get()
        )

        # UI state lock
        self.is_running = True
        self.btn_start.config(state=tk.DISABLED)
        self.status_label.config(
            text="Status: Running Scan...", foreground="blue"
        )

        # Clear plots
        self.line_x.set_data([], [])
        self.line_y.set_data([], [])
        self.canvas.draw()

        # Run acquisition in background thread to keep GUI responsive
        threading.Thread(target=self._run_measurement, daemon=True).start()

    def _run_measurement() -> None:
        try:
            # Override start_measurement loop or call directly
            self.spectroscopy.start_measurement()

            self.root.after(
                0,
                self._scan_finished,
                True,
                "Measurement completed successfully.",
            )
        except Exception as e:
            self.root.after(0, self._scan_finished, False, str(e))

    def _scan_finished(self, success: bool, message: str) -> None:
        self.is_running = False
        self.btn_start.config(state=tk.NORMAL)

        if success:
            self.status_label.config(
                text="Status: Finished", foreground="green"
            )
            messagebox.showinfo("Success", message)
        else:
            self.status_label.config(
                text="Status: Error during scan", foreground="red"
            )
            messagebox.showerror("Scan Error", f"Error occurred: {message}")

    def on_close(self) -> None:
        if self.spectroscopy:
            try:
                self.spectroscopy.close()
            except Exception:
                pass
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = PCspectroscopyGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
