import time
import sys
# Make sure your imports match your project structure:
# from LabControl.Devices.SR830 import SR830
from LabControl.DeviceDrivers.SR830 import SR830

PORT = "/dev/ttyUSB0"  # Replace with your serial port (e.g., 'COM3' on Windows)
BAUDRATE = 9600

def test_live_sr830():
    print(f"Connecting to SR830 on {PORT} at {BAUDRATE} baud...")
    sr = SR830(port=PORT, baudrate=BAUDRATE, timeout=2.0)
    
    if not sr.connect():
        print("ERROR: Failed to connect to SR830.")
        sys.exit(1)
        
    try:
        print(" Connected successfully.")
        
        # 1. Query Identification
        device_id = sr.get_id()
        print(f"[*] Device ID (*IDN?): {device_id.strip()}")
        
        # 2. Reference & Frequency Settings
        print("[*] Setting Reference Source to Internal...")
        sr.set_ref_source(internal=True)
        
        test_freq = 1000.0  # 1 kHz
        print(f"[*] Setting Frequency to {test_freq} Hz...")
        sr.set_frequency(test_freq)
        
        read_freq = sr.get_frequency()
        print(f"    Current Frequency: {read_freq} Hz")
        
        # 3. Time Constant & Gain Settings
        print("[*] Setting Time Constant to index 8 (100 ms)...")
        sr.set_time_constant(tau_setting=8, wait_for_settle=True)
        
        print("[*] Setting Sensitivity / Gain to index 18...")
        sr.set_gain(18)
        
        # 4. Phase & Auto Routines
        print("[*] Setting Phase to 0 degrees...")
        sr.set_phase(0.0)
        print(f"    Current Phase: {sr.get_phase()} degrees")
        
        # 5. Read Channel Measurements
        print("\n--- Live Data Readings ---")
        ch1 = sr.read_ch1()
        ch2 = sr.read_ch2()
        mag = sr.read_magnitude()
        print(f"Ch 1 (X): {ch1} V")
        print(f"Ch 2 (Y): {ch2} V")
        print(f"Magnitude (R): {mag} V")
        
        # 6. Read SNAP Data
        snapshot = sr.get_snapshot()
        print("\n--- Snapshot Data (SNAP? 1,2,3,4) ---")
        for key, val in snapshot.items():
            print(f"  {key}: {val}")

    finally:
        print("\nDisconnecting device...")
        sr.disconnect()
        print("Done.")

if __name__ == "__main__":
    test_live_sr830()
