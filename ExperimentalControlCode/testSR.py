import asyncio
import logging
from LabControl.devices.SR830Control import SR830

# Configure logging to see low-level communication
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


async def test_sr830_driver():
    port = "/dev/ttyUSB0"
    baudrate = 19200

    print("==================================================")
    print(f"Starting SR830 Driver Functionality Test on {port}")
    print("==================================================\n")

    lockIn = SR830(port=port, baudrate=baudrate, timeout=5.0)

    # 1. Connection Test
    print("[TEST 1/8] Connecting to device and forcing OUTX 0...")
    connected = await lockIn.connect()
    if not connected:
        print("❌ FAIL: Could not connect to SR830. Aborting test.")
        return
    print("✓ PASS: Connected and output directed to RS-232.\n")

    try:
        # 2. Identification Test
        print("[TEST 2/8] Testing get_id()...")
        device_id = await lockIn.get_id()
        print(f"  Device ID: {device_id}")
        assert "SR830" in device_id, "Device ID string did not contain 'SR830'"
        print("✓ PASS: ID query successful.\n")

        # 3. Reference & Oscillator Settings
        print("[TEST 3/8] Testing Reference & Oscillator commands...")
        print("  Setting Internal Reference Mode (FMOD 1)...")
        await lockIn.set_ref_source(internal=True)

        print("  Setting Frequency to 1000.0 Hz (FREQ 1000.0)...")
        await lockIn.set_frequency(1000.0)
        freq = await lockIn.get_frequency()
        print(f"  Queried Frequency: {freq} Hz")

        print("  Setting Amplitude to 0.5 Vrms (SLVL 0.5)...")
        await lockIn.set_amplitude(0.5)

        print("  Setting Phase to 45.0° (PHAS 45.0)...")
        await lockIn.set_phase(45.0)
        phase = await lockIn.get_phase()
        print(f"  Queried Phase: {phase}°")
        print("✓ PASS: Reference & Oscillator settings completed.\n")

        # 4. Gain and Time Constant Settings (with settling delay)
        print("[TEST 4/8] Testing Gain & Time Constant settings...")
        print("  Setting Gain/Sensitivity code to 15 (10 uA / 10 mV)...")
        await lockIn.set_gain(15)

        print("  Setting Time Constant code to 4 (1 ms) with automatic settling delay...")
        # OFLT code 4 = 1ms. The method will pause 5 * 1ms = 5ms internally
        await lockIn.set_time_constant(tau_setting=4, wait_for_settle=True)
        print("✓ PASS: Gain and Time Constant settings applied.\n")

        # 5. Status Register Polling Test
        print("[TEST 5/8] Testing wait_until_ready() status polling...")
        ready = await lockIn.wait_until_ready()
        print(f"  Is device ready: {ready}")
        assert ready, "Device reported busy before auto-routines"
        print("✓ PASS: Status register polling functional.\n")

        # 6. Auto Functions (Blocking)
        print("[TEST 6/8] Testing blocking auto_gain() and auto_phase()...")
        print("  Executing auto_gain() (will block until hardware is done)...")
        await lockIn.auto_gain()
        print("  Auto-gain finished!")

        print("  Executing auto_phase() (will block until hardware is done)...")
        await lockIn.auto_phase()
        print("  Auto-phase finished!")
        print("✓ PASS: Blocking auto routines executed successfully.\n")

        # 7. Single Channel Data Retrieval
        print("[TEST 7/8] Testing individual Channel readout queries...")
        ch1 = await lockIn.read_ch1()
        ch2 = await lockIn.read_ch2()
        mag = await lockIn.read_magnitude()
        print(f"  Channel 1 Output (OUTP? 1) : {ch1:.6e}")
        print(f"  Channel 2 Output (OUTP? 2) : {ch2:.6e}")
        print(f"  Magnitude R      (OUTP? 3) : {mag:.6e}")
        print("✓ PASS: Single channel queries returned data.\n")

        # 8. Synchronous Snapshot Data Retrieval
        print("[TEST 8/8] Testing get_snapshot() (SNAP? 1,2,3,4)...")
        snap = await lockIn.get_snapshot()
        print("  --- SR830 Snapshot ---")
        print(f"  X Output  : {snap['X']:.6e}")
        print(f"  Y Output  : {snap['Y']:.6e}")
        print(f"  Magnitude : {snap['R']:.6e}")
        print(f"  Phase (θ) : {snap['Theta']:.2f}°")

        # Verify snapshot dictionary structure
        assert all(key in snap for key in ("X", "Y", "R", "Theta")), "Missing key in snapshot return"
        print("✓ PASS: Synchronous snapshot retrieved.\n")

        print("==================================================")
        print("🎉 ALL TESTS PASSED SUCCESSFULLY!")
        print("==================================================")

    except Exception as e:
        print(f"\n❌ TEST FAILED with error: {e}")
        raise e

    finally:
        print("\nDisconnecting device...")
        await lockIn.disconnect()
        print("Connection closed.")


if __name__ == "__main__":
    asyncio.run(test_sr830_driver())
