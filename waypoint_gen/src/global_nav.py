import math

from location import Location
from local_nav import LocalWP

class GlobalWP(object):
    def __init__(self, cfg, local_wp):
        self.cfg = cfg
        self.D_STEP = float(self.cfg.get("global_wp", "d_step"))
        self.local_wp = local_wp
    
    def getWaypoints(self, g_waypoints):
        waypoints = [g_waypoints[0]]
        count = 1
        for count in range(len(g_waypoints)):
            prevWaypoint = waypoints[-1]
            currWaypoint = g_waypoints[count]

            intermediateWayPoints = self.getIntermediateWaypoints(prevWaypoint, currWaypoint)
            [waypoints.append(i_waypoint) for i_waypoint in intermediateWayPoints]                

            bearing = Location.getBearing(prevWaypoint, currWaypoint)
            local_waypoints = self.local_wp.getLocalNavigationWaypoints(currWaypoint, bearing)             
            [waypoints.append(l_waypoint) for l_waypoint in local_waypoints]

            count += 1
        return waypoints

    def getIntermediateWaypoints(self, loc1, loc2):
        waypoints = [loc1]
        dist = Location.getDistance(loc1, loc2)
        bearing = Location.getBearing(loc1, loc2)
        currDist, currLatLong = 0, loc1
        v_step = (loc2.getElev()-loc1.getElev())/(float(dist)/self.D_STEP) if dist >= self.D_STEP else loc2.getElev()-loc1.getElev()
        while currDist < dist:
            if currDist + self.D_STEP <= dist:
                currLatLong = Location.getLocation(currLatLong, bearing, self.D_STEP, v_step)
                waypoints.append(currLatLong)            
            currDist += self.D_STEP
        return waypoints

