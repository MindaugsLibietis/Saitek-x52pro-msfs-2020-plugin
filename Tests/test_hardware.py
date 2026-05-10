import X52_pro_driver
import time
import random

def run_stress_test():
    print("--- X52 PRO MULTI-THREADED STRESS TEST ---")

    if not X52_pro_driver.initialize_mfd(page_count=3):
        print("Hardware not found.")
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
        pass

    print("\nTest Complete. Cleaning up...")
    X52_pro_driver.cleanup()

if __name__ == "__main__":
    run_stress_test()