from LabControl.GUI.ExperimentUI import PCspectroscopyGUI
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = PCspectroscopyGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
