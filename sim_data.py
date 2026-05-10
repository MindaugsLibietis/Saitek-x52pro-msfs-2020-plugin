from SimConnect import SimConnect, AircraftRequests
import math

class SimBridge:
    def __init__(self):
        self.sm = None
        self.aq = None

    def connect(self):
        """Attempts to connect to MSFS. Returns True if successful."""
        try:
            # The SimConnect object handles the low-level pipe connection
            self.sm = SimConnect()
            # AircraftRequests fetches the actual variables
            self.aq = AircraftRequests(self.sm, _time=50)
            return True
        except Exception:
            return False

    def get_telemetry(self):
        """Fetches a dictionary of current flight data."""
        if not self.aq:
            return None

        try:
            return {
                "alt": self.aq.get("PLANE_ALTITUDE"),
                "spd": self.aq.get("AIRSPEED_INDICATED"),
                "gear": self.aq.get("GEAR_TOTAL_PCT_EXTENDED"),
                "hdg": math.degrees(self.aq.get("PLANE_HEADING_DEGREES_MAGNETIC") or 0) % 360,
                "aoa": math.degrees(self.aq.get("INCIDENCE_ALPHA") or 0)
            }
        except:
            return None