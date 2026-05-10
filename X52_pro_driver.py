import ctypes
import threading
import time
from ctypes import wintypes, create_unicode_buffer

# =========================================================
# CONSTANTS & TYPES
# =========================================================
# These match the Saitek/Logitech DirectOutput C++ Header definitions.
HRESULT = ctypes.c_long
DEVICE_HANDLE = ctypes.c_void_p

# Function pointer types for the DLL callbacks
ENUM_CALLBACK_TYPE = ctypes.WINFUNCTYPE(None, DEVICE_HANDLE, ctypes.c_void_p)
PAGE_CHANGE_CALLBACK = ctypes.WINFUNCTYPE(None, DEVICE_HANDLE, wintypes.DWORD, ctypes.c_bool, ctypes.c_void_p)

# =========================================================
# DLL INITIALIZATION
# =========================================================
DLL_PATH = r"C:\Program Files\Logitech\DirectOutput\DirectOutput.dll"
try:
    do = ctypes.windll.LoadLibrary(DLL_PATH)
except Exception as e:
    # Crucial for QA: provide a clear error if the driver is missing
    print(f"FATAL ERROR: DirectOutput.dll not found at {DLL_PATH}")
    raise e

# Define argument and return types for the DLL functions to prevent memory corruption
do.DirectOutput_Initialize.argtypes = [ctypes.c_wchar_p]
do.DirectOutput_RegisterPageCallback.argtypes = [DEVICE_HANDLE, PAGE_CHANGE_CALLBACK, ctypes.c_void_p]
do.DirectOutput_AddPage.argtypes = [DEVICE_HANDLE, wintypes.DWORD, ctypes.c_bool]
do.DirectOutput_SetString.argtypes = [DEVICE_HANDLE, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, ctypes.c_wchar_p]
do.DirectOutput_SetLed.argtypes = [DEVICE_HANDLE, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD]

# =========================================================
# GLOBAL STATE
# =========================================================
found_devices = []

def _device_callback(device_handle, context):
    """Internal callback triggered by the DLL when a joystick is found."""
    found_devices.append(ctypes.c_void_p(device_handle))

def _page_callback(handle, page, active, ctx):
    """Triggered when the user scrolls the MFD wheel. Kept empty for stability."""
    pass

# Create persistent pointers to the callbacks so they aren't garbage collected
callback_ptr = ENUM_CALLBACK_TYPE(_device_callback)
page_cb_ptr = PAGE_CHANGE_CALLBACK(_page_callback)

# =========================================================
# PUBLIC API FUNCTIONS
# =========================================================

def initialize_mfd(page_count=2):
    """
    Initializes the DLL, scans for hardware, and prepares MFD pages.
    :param page_count: Number of virtual screens to create.
    """
    do.DirectOutput_Initialize("X52_Bridge")
    do.DirectOutput_Enumerate(callback_ptr, None)

    import time
    time.sleep(1.0) # Hardware needs a breather to respond to enumeration

    for h_dev in found_devices:
        # Registering the callback allows the hardware to handle scrolling events
        do.DirectOutput_RegisterPageCallback(h_dev, page_cb_ptr, None)
        for p in range(1, page_count + 1):
            # bActivate=True (1) only for the first page
            do.DirectOutput_AddPage(h_dev, p, (1 if p == 1 else 0))

    return len(found_devices) > 0

def update_display(page_num, line0="", line1="", line2=""):
    """Sends text strings to a specific MFD page."""
    for h_dev in found_devices:
        set_mfd_line(h_dev, page_num, 0, line0)
        set_mfd_line(h_dev, page_num, 1, line1)
        set_mfd_line(h_dev, page_num, 2, line2)

def set_mfd_line(handle, page, line, text):
    """Low-level helper to convert Python strings to C-style Wide Characters."""
    text = str(text)[:16] # Hardware limit is 16 chars
    buf = create_unicode_buffer(text)
    do.DirectOutput_SetString(handle, page, line, len(text), buf)

def set_button_led(button_index, is_green, flicker_count=0):
    if flicker_count > 0:
        # Launch the flicker logic in a separate background thread
        thread = threading.Thread(
            target=_flicker_logic,
            args=(button_index, is_green, flicker_count),
            daemon=True # Daemon means the thread closes automatically when the main app closes
        )
        thread.start()
    else:
        _set_led_solid(button_index, is_green)

def _set_led_solid(button_index, is_green):
    """Internal helper to set the solid color without a loop."""
    red_id = button_index
    green_id = button_index + 1
    final_id = green_id if is_green else red_id
    other_id = red_id if is_green else green_id

    for h_dev in found_devices:
        do.DirectOutput_SetLed(h_dev, 1, final_id, 1)
        do.DirectOutput_SetLed(h_dev, 1, other_id, 0)

def _flicker_logic(button_index, is_green, count):
    """The actual loop that runs in the background."""
    red_id = button_index
    green_id = button_index + 1
    final_id = green_id if is_green else red_id
    other_id = red_id if is_green else green_id

    for _ in range(count):
        for h_dev in found_devices:
            do.DirectOutput_SetLed(h_dev, 1, final_id, 1)
            do.DirectOutput_SetLed(h_dev, 1, other_id, 0)
        time.sleep(0.08) # Slightly faster flicker for 'premium' feel
        for h_dev in found_devices:
            do.DirectOutput_SetLed(h_dev, 1, final_id, 0)
        time.sleep(0.08)

    # Ensure it ends on the correct solid state
    _set_led_solid(button_index, is_green)

def cleanup():
    """Shuts down the DLL link. Failure to call this can lock the driver."""
    do.DirectOutput_Deinitialize()