import X52_pro_driver
import sim_data
import time

def run():
    bridge = sim_data.SimBridge()
    print("Initializing Hardware...")
    if not X52_pro_driver.initialize_mfd(page_count=2):
        print("X52 not found.")
        return
    X52_pro_driver.update_display(1, "Waiting for MSFS", "   Crafted by", "     EsPats")
    print("Waiting for MSFS connection...")

    while not bridge.connect():
        time.sleep(5)

    print("Connected to Sim!")


    try:
        while True:
            data = bridge.get_telemetry()
            if data:
                # --- PAGE 1: NAVIGATION ---
                alt = int(data['alt'] or 0)
                spd = int(data['spd'] or 0)
                X52_pro_driver.update_display(1, "NAV DATA", f"ALT: {alt}ft", f"SPD: {spd}kt")
                # --- PAGE 2: SYSTEMS ---
            if data:
                raw_gear = data.get('gear')
                gear = float(raw_gear) if raw_gear is not None else 0.0

                if gear >= 0.99:
                    X52_pro_driver.set_button_led(10, True, flicker_count=0)
                elif gear <= 0.01:
                    X52_pro_driver.set_button_led(10, False, flicker_count=0)
                else:
                    X52_pro_driver.set_button_led(10, True, flicker_count=1)
                    gear_pct = gear * 100
                    X52_pro_driver.update_display(2, "SYSTEMS", f"GEAR: {gear_pct:.0f}%", "MOVING..." if 0 < gear < 1 else "LOCKED")
            time.sleep(0.1) # 10Hz refresh rate

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        X52_pro_driver.cleanup()

if __name__ == "__main__":
    run()