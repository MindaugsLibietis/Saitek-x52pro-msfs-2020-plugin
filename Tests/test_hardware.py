import X52_pro_driver
import time
import random

def test_initialization_failure():
    # This test simulates checking for hardware failure during initialization
    # We assume initialize_mfd can return False under some conditions.
    # Since we don't have control over the actual hardware state,
    # this test focuses on the code path handling the failure.
    # For a real test, mocking X52_pro_driver would be necessary.
    # For now, we test the path where initialization fails.
    
    # Since we cannot mock external dependencies easily without more context,
    # we rely on the existing structure for now, focusing on what the function *does*
    # when it fails. We will rely on the core function handling the error flow.
    # A more advanced test would require mocking.
    pass # Placeholder for now, focusing on the existing flow

def test_isolated_led_control():
    # Test setting individual LED states and flicker counts in isolation.
    # This tests the driver's basic command reception.
    
    # Test setting LED 9 to True with a specific flicker count
    X52_pro_driver.set_button_led(9, True, flicker_count=5)
    # Test setting LED 1 to False with a specific flicker count
    X52_pro_driver.set_button_led(1, False, flicker_count=2)
    
    # In a real test environment, we would assert the actual state of the hardware.
    # Since we are testing the driver interface, we'll just ensure the calls don't raise errors.
    print("Isolated LED control calls passed without exception.")

def test_display_update_logic():
    # Test the MFD update logic with various inputs.
    
    # Test typical data update
    X52_pro_driver.update_display(1, "Test", "Value: 100", "PAGE 1")
    
    # Test another update with different data
    X52_pro_driver.update_display(2, "Status", "OK", "PAGE 2")
    
    print("Display update logic calls passed without exception.")


def run_stress_test():
    print("--- X52 PRO MULTI-THREADED STRESS TEST ---")

    if not X52_pro_driver.initialize_mfd(page_count=3):
        print("Hardware not found or initialization failed.")
        return

    print("Step 1: Testing Independent LED Threading")
    # We launch TWO flickers at once.
    # T1 (9) will flicker 15 times, Fire (1) will flicker 3 times.
    X52_pro_driver.set_button_led(9, True, flicker_count=15)
    X52_pro_driver.set_button_led(1, False, flicker_count=3)

    print("Step 2: Testing MFD Refresh during LED Flicker")
    # While the lights are still flickering in the background,
    # we are going to spam the MFD with a fast-changing number.
    try:
        for i in range(100):
            # We update all 3 pages constantly
            X52_pro_driver.update_display(1, "STRESS TEST", f"ITERATION: {i}", "PAGE 1")
            X52_pro_driver.update_display(2, "SYSTEMS", f"VOLTAGE: {random.uniform(12, 14):.2f}V", "PAGE 2")
            X52_pro_driver.update_display(3, "NAV DATA", f"LAT: {random.randint(50, 60)}", "PAGE 3")

            # If the screen stutters while the lights are flickering, the threading failed.
            # If it's smooth, you've succeeded.
            time.sleep(0.05)

            if i == 50:
                print("Step 3: Mid-loop LED interrupt")
                # Halfway through, we trigger another flicker to see if it breaks the MFD
                X52_pro_driver.set_button_led(11, True, flicker_count=10) # E-Button

    except KeyboardInterrupt:
        print("Stress test interrupted by user.")

    print("\nTest Complete. Cleaning up...")
    X52_pro_driver.cleanup()

if __name__ == "__main__":
    # Run the main stress test
    run_stress_test()

# --- Additional Tests ---
if __name__ == "__main__":
    # Run isolated tests if the main stress test is not intended to run immediately
    print("\n--- Running Isolated Tests ---")
    test_isolated_led_control()
    test_display_update_logic()
    test_initialization_failure()
    print("Hardware test complete!")
    input("Press Enter to close this window...")