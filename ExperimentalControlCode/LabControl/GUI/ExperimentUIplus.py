import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import List

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial.tools.list_ports

from LabControl.Devices.PCspectroscopy import PCspectroscopy


class PCspectroscopyGUI:

    OFLT_MAP = {
        "10us": 0, "30us": 1, "100us": 2, "300us": 3, "1ms": 4,
        "3ms": 5, "10ms": 6, "30ms": 7, "100ms": 8, "300ms": 9,
        "1s": 10, "3s": 11, "10s": 12, "30s": 13, "100s": 14,
        "300s": 15, "1ks": 16, "3ks": 17, "10ks": 18, "30ks": 19
    }

    SENS_MAP = {
        "2fA": 0, "10fA": 1, "20fA": 2, "50fA": 3, "100fA": 4,
        "200fA": 6, "500fA": 7, "1pA": 8, "2pA": 9, "5pA": 10,
        "10pA": 11, "20pA": 12, "50pA": 13, "100pA": 14,
        "200pA": 15, "500pA": 16, "1nA": 17, "2nA": 18,
        "5nA": 19, "10nA": 20, "20nA": 21, "50nA": 22,
        "100nA": 23, "200nA": 24, "500nA": 25, "1uA": 26
    }

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("PC Spectroscopy Measurement Control")
        self.root.geometry("1100x750")

        self.spectroscopy: PCspectroscopy | None = None
        self.is_running = False
        self._section_added = False

        self._build_ui()

    @staticmethod
    def _get_available_ports() -> List[str]:
        ports = [port.device for port in serial.tools.list_ports.comports()]
        return ports if ports else ["/dev/ttyUSB0", "/dev/AMCtty0"]

    def _refresh_ports(self, event=None) -> None:
        available = self._get_available_ports()
        self.lockin_port_cb['values'] = available
        self.stage_port_cb['values'] = available

    def _build_ui(self) -> None:
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        control_panel = ttk.Frame(main_frame, width=340)
        control_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        plot_panel = ttk.Frame(main_frame)
        plot_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- Data Storage ---
        file_frame = ttk.LabelFrame(control_panel, text="Data Storage", padding=10)
        file_frame.pack(fill=tk.X, pady=(0, 10))

        self.hdf5_path_var = tk.StringVar(value="measurement.h5")
        ttk.Entry(file_frame, textvariable=self.hdf5_path_var).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5)
        )
        ttk.Button(file_frame, text="Browse", command=self._browse_file).pack(side=tk.RIGHT)

        # --- Hardware Ports ---
        hw_frame = ttk.LabelFrame(control_panel, text="Hardware Ports", padding=10)
        hw_frame.pack(fill=tk.X, pady=(0, 10))

        ports_list = self._get_available_ports()

        ttk.Label(hw_frame, text="Lock-in Port:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.lockin_port_var = tk.StringVar(value=ports_list[0])
        self.lockin_port_cb = ttk.Combobox(
            hw_frame, textvariable=self.lockin_port_var, values=ports_list, width=15
        )
        self.lockin_port_cb.grid(row=0, column=1, sticky=tk.E, pady=2)
        self.lockin_port_cb.bind("<Button-1>", self._refresh_ports)

        ttk.Label(hw_frame, text="Delay Stage Port:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.stage_port_var = tk.StringVar(
            value=ports_list[1] if len(ports_list) > 1 else ports_list[0]
        )
        self.stage_port_cb = ttk.Combobox(
            hw_frame, textvariable=self.stage_port_var, values=ports_list, width=15
        )
        self.stage_port_cb.grid(row=1, column=1, sticky=tk.E, pady=2)
        self.stage_port_cb.bind("<Button-1>", self._refresh_ports)

        self.btn_connect = ttk.Button(
            hw_frame, text="Connect Hardware", command=self._connect_hardware
        )
        self.btn_connect.grid(row=2, column=0, columnspan=2, pady=(8, 0), sticky=tk.EW)

        # --- Delay Program ---
        delay_frame = ttk.LabelFrame(control_panel, text="Delay Program", padding=10)
        delay_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(delay_frame, text="Start (ps):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.start_var = tk.DoubleVar(value=-5.0)
        ttk.Entry(delay_frame, textvariable=self.start_var, width=12).grid(row=0, column=1, sticky=tk.E, pady=2)

        ttk.Label(delay_frame, text="Stop (ps):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.stop_var = tk.DoubleVar(value=15.0)
        ttk.Entry(delay_frame, textvariable=self.stop_var, width=12).grid(row=1, column=1, sticky=tk.E, pady=2)

        ttk.Label(delay_frame, text="Step Size (ps):").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.step_var = tk.DoubleVar(value=0.1)
        ttk.Entry(delay_frame, textvariable=self.step_var, width=12).grid(row=2, column=1, sticky=tk.E, pady=2)

        self.btn_add_section = ttk.Button(
            delay_frame, text="Add Section", state=tk.DISABLED, command=self._add_delay_program
        )
        self.btn_add_section.grid(row=3, column=0, columnspan=2, pady=(8, 0), sticky=tk.EW)

        # --- Scan Parameters ---
        param_frame = ttk.LabelFrame(control_panel, text="Scan Parameters", padding=10)
        param_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(param_frame, text="Cycles:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.cycles_var = tk.IntVar(value=2)
        ttk.Entry(param_frame, textvariable=self.cycles_var, width=12).grid(row=0, column=1, sticky=tk.E, pady=2)

        ttk.Label(param_frame, text="Time Zero (mm):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.tzero_var = tk.DoubleVar(value=100.0)
        ttk.Entry(param_frame, textvariable=self.tzero_var, width=12).grid(row=1, column=1, sticky=tk.E, pady=2)

        ttk.Label(param_frame, text="Tau:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.tau_var = tk.StringVar(value="100ms")
        self.tau_cb = ttk.Combobox(
            param_frame, textvariable=self.tau_var, values=list(self.OFLT_MAP.keys()), width=10, state="readonly"
        )
        self.tau_cb.grid(row=2, column=1, sticky=tk.E, pady=2)

        ttk.Label(param_frame, text="Gain:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.gain_var = tk.StringVar(value="500nA")
        self.gain_cb = ttk.Combobox(
            param_frame, textvariable=self.gain_var, values=list(self.SENS_MAP.keys()), width=10, state="readonly"
        )
        self.gain_cb.grid(row=3, column=1, sticky=tk.E, pady=2)

        # --- Action Controls ---
        action_frame = ttk.Frame(control_panel, padding=5)
        action_frame.pack(fill=tk.X, pady=(10, 0))

        self.btn_start = ttk.Button(
            action_frame, text="Start Scan", state=tk.DISABLED, command=self._start_scan_thread
        )
        self.btn_start.pack(fill=tk.X, pady=(0, 10))

        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(action_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X)

        self.status_label = ttk.Label(action_frame, text="Status: Disconnected", foreground="gray")
        self.status_label.pack(anchor=tk.W, pady=(5, 0))

        # --- Matplotlib Plot ---
        self.fig, self.ax = plt.subplots(figsize=(6, 4), dpi=100)
        self.ax.set_title("Live Measurement Current")
        self.ax.set_xlabel("Position / Delay (mm)")
        self.ax.set_ylabel("Signal (V / A)")
        self.ax.grid(True)

        (self.line_x,) = self.ax.plot([], [], "b.-", label="Channel X")
        (self.line_y,) = self.ax.plot([], [], "r.-", label="Channel Y")
        self.ax.legend(loc="upper right")

        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_panel)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _browse_file(self) -> None:
        filepath = filedialog.asksaveasfilename(
            defaultextension=".h5",
            filetypes=[("HDF5 Files", "*.h5 *.hdf5"), ("All Files", "*.*")],
        )
        if filepath:
            self.hdf5_path_var.set(filepath)

    def _connect_hardware(self) -> None:
        h5_path = self.hdf5_path_var.get()
        if not h5_path:
            messagebox.showerror("Error", "Please select a valid HDF5 file path.")
            return

        try:
            self.spectroscopy = PCspectroscopy(h5_path)
            self.spectroscopy.connect_devices(
                lockin_port=self.lockin_port_var.get(),
                stage_port=self.stage_port_var.get(),
            )
            self.status_label.config(text="Status: Connected", foreground="green")
            self.btn_start.config(state=tk.NORMAL)
            self.btn_add_section.config(state=tk.NORMAL)
            self.btn_connect.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {e}")
            self.status_label.config(text="Status: Connection Failed", foreground="red")

    def _start_scan_thread(self) -> None:
        if self.is_running or not self.spectroscopy:
            return

        # 1. Update parameters in backend
        tau_idx = self.OFLT_MAP.get(self.tau_var.get(), 8)
        gain_idx = self.SENS_MAP.get(self.gain_var.get(), 25)

        params = {
            "N_cycles": self.cycles_var.get(),
            "stage": {"time_zero_mm": self.tzero_var.get()},
            "lockin": {
                "internal_ref": False,
                "time_constant": tau_idx,
                "gain": gain_idx
            },
        }
        self.spectroscopy.set_parameters(params)

        # 2. Add delay steps if not already queued
        if not self._section_added:
            try:
                self.spectroscopy.add_delay_steps(
                    self.start_var.get(), self.stop_var.get(), self.step_var.get()
                )
                self._section_added = True
            except Exception as e:
                messagebox.showerror("Error", f"Failed to calculate scan steps: {e}")
                return

        # 3. Clear plot canvas before starting
        self.line_x.set_data([], [])
        self.line_y.set_data([], [])
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()

        # UI state lock
        self.is_running = True
        self.btn_start.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Running Scan...", foreground="blue")

        # 4. Launch background worker thread
        threading.Thread(target=self._run_measurement, daemon=True).start()

    def _run_measurement(self) -> None:
        """Executes scan in background thread and passes point callback to backend."""
        try:
            self.spectroscopy.start_measurement(update_callback=self._on_point_recorded)

            self.root.after(
                0, self._scan_finished, True, "Measurement completed successfully."
            )
        except Exception as e:
            self.root.after(0, self._scan_finished, False, str(e))

    def _on_point_recorded(self, pos: float, x_val: float, y_val: float, progress: float) -> None:
        """Background worker delegates GUI thread updates securely via root.after."""
        self.root.after(0, self._update_plot_ui, pos, x_val, y_val, progress)

    def _update_plot_ui(self, pos: float, x_val: float, y_val: float, progress: float) -> None:
        """Runs safely on Tkinter main thread to append points and redraw canvas."""
        self.progress_var.set(progress)

        x_data = list(self.line_x.get_xdata())
        y_data_x = list(self.line_x.get_ydata())
        y_data_y = list(self.line_y.get_ydata())

        x_data.append(pos)
        y_data_x.append(x_val)
        y_data_y.append(y_val)

        self.line_x.set_data(x_data, y_data_x)
        self.line_y.set_data(x_data, y_data_y)

        self.ax.relim()
        self.ax.autoscale_view()

        self.canvas.draw_idle()

    def _scan_finished(self, success: bool, message: str) -> None:
        self.is_running = False
        self.btn_start.config(state=tk.NORMAL)

        if success:
            self.status_label.config(text="Status: Finished", foreground="green")
            messagebox.showinfo("Success", message)
        else:
            self.status_label.config(text="Status: Error during scan", foreground="red")
            messagebox.showerror("Scan Error", f"Error occurred: {message}")

    def _add_delay_program(self) -> None:
        if not self.spectroscopy:
            messagebox.showwarning("Warning", "Connect hardware before adding delay steps.")
            return

        self.spectroscopy.set_parameters({
            "stage": {"time_zero_mm": self.tzero_var.get()}
        })

        try:
            self.spectroscopy.add_delay_steps(
                self.start_var.get(), self.stop_var.get(), self.step_var.get()
            )
            self._section_added = True
            messagebox.showinfo(
                "Delay Step Added",
                f"Added section: {self.start_var.get()} to {self.stop_var.get()} ps (Time Zero: {self.tzero_var.get()} mm)"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Could not add steps: {e}")

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
