import math

from location import Location

class LocalWP(object):
    def __init__(self, cfg):
        self.cfg = cfg
        self.L_RAD = float(self.cfg.get("local_wp", "ini_rad"))
        self.ANGLE_INCR = float(self.cfg.get("local_wp", "ha_step"))
        self.L_RAD_INCR = float(self.cfg.get("local_wp", "va_step"))
        self.ELEV_H = float(self.cfg.get("local_wp", "elev_h"))
        self.ELEV_L = float(self.cfg.get("local_wp", "elev_l"))
        self.ELEV_INCR = float(self.cfg.get("local_wp", "elev_step"))

    def getLocalNavigationWaypoints(self, center, bearing):
        inc, elev, rad = 0, center.getElev(), self.L_RAD
        local_waypoints = [Location.getLocation(center, bearing, self.L_RAD, center.getElev())]
        while elev <= self.ELEV_H:
            elev += self.ELEV_INCR
            rad += self.L_RAD_INCR
            nxt_loc = Location.getLocation(center, bearing+inc, rad, elev)
            local_waypoints.append(nxt_loc)
            inc += self.ANGLE_INCR
        while inc <= 2*math.pi:
            nxt_loc = Location.getLocation(center, bearing+inc, rad, elev)
            local_waypoints.append(nxt_loc)
            inc += self.ANGLE_INCR
        return local_waypoints
