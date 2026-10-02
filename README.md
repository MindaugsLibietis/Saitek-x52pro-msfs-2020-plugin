# ✈️ MSFS 2020 Saitek X52 Pro Bridge Plugin

A modular, multi-threaded hardware-to-simulator bridge for Microsoft Flight Simulator 2020. This tool establishes an active data link using the MSFS SimConnect API and maps live flight telemetry directly onto the physical MFD screens and LED registers of the Saitek/Logitech X52 Pro HOTAS.

---

## 🛑 Step 1: Pre-requisites & Driver Stack

Before running the binaries, your Windows system must expose the low-level DirectOutput API architecture.

1. Visit the official [Saitek Support Page](https://www.saitek.com/).
2. Navigate to **Downloads** -> **Drivers** and search for the **X52 Flight Control System**.
3. You will be redirected directly to the [Logitech Support Ecosystem](https://support.logi.com/).
4. Download and install the latest (**Software Version: 8.0.213.0, Last Update: 2018-09-24**) driver package for your Windows version.
    * *Note: This driver installation drops the critical unmanaged library `DirectOutput.dll` into your filesystem at `C:\Program Files\Logitech\DirectOutput\DirectOutput.dll`, which this plugin targets using Python `ctypes` bindings.*

---

## 🚀 Step 2: How to Download & Run

You do **not** need an IDE or a Python runtime environment to run the production binaries.

1. Navigate to the **Releases** tab on the right side of this GitHub page.
2. Download both `X52_MSFS_Plugin.exe` (The core simulator link) and `test_hardware.exe` (The localized hardware debug tool).
3. Connect your X52 Pro HOTAS to an active USB interface.
4. Execute **`test_hardware.exe`** first to verify that your system architecture is correctly allocating and reading data to your joystick without initializing the simulator.
5. Once confirmed, initiate **`X52_MSFS_Plugin.exe`** and launch Microsoft Flight Simulator 2020.

---

## 🏗️ Architecture & Data Workflow

The application acts as a middleman, translating telemetry frames from the game environment directly into driver commands.

---

## Demonstration and Reddit article

I posted a small insights video demonstration on Reddit r/MicrosoftFlightSim with the title "x52 pro msfs". Users with the same hardware and MSFS 2020 simulator are invited to collaborate on this project. Even if you have no experience or free time to develop, but have flight knowledge and experience, any ideas for telemetry to display, ways of interacting with this interface, or button leds actions are appreciated on this topic.
Link to Reddit article: [x52 pro msfs](https://www.reddit.com/r/MicrosoftFlightSim/s/zWq0cKZdoC)

https://github.com/user-attachments/assets/06a9b3c8-e5e8-44ef-b70b-066c70e944f0
