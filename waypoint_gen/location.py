import math

R = 6370000

class Location(object):
    def __init__(self, locn):
        self.lat = float(locn[0])
        self.long = float(locn[1])
        self.elev = float(locn[2])

    def __str__(self):
        return str(math.degrees(self.lat)) + "," + str(math.degrees(self.long)) + "," + str(self.elev)
        
    def getLat(self):
        return self.lat    

    def getLong(self):
        return self.long

    def getElev(self):
        return self.elev

    @staticmethod
    def getLocation(locn, bearing, distance, elev_diff):
        lat1, lon1 = locn.getLat(), locn.getLong()
        lat2 = math.asin(math.sin(lat1)*math.cos(float(distance)/R) + math.cos(lat1)*math.sin(float(distance)/R)*math.cos(bearing))
        lon2 = lon1 + math.atan2(math.sin(bearing)*math.sin(float(distance)/R)*math.cos(lat1), math.cos(float(distance)/R)-math.sin(lat1)*math.sin(lat2))
        lon2 = math.fmod((lon2+3*math.pi),(2*math.pi)) - math.pi;  
        return Location([lat2, lon2, locn.getElev() + elev_diff])

    # theta = atan2(sin(long2-long1).cos(lat2), cos(lat1).sin(lat2)-sin(lat1).cos(lat2).cos(long2-long1))
    @staticmethod
    def getBearing(latLong1, latLong2):
        lat1, long1 = latLong1.getLat(), latLong1.getLong()
        lat2, long2 = latLong2.getLat(), latLong2.getLong()
        x = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)* math.cos(lat2) * math.cos(long2-long1))
        y = math.sin(long2-long1) * math.cos(lat2)
        initial_bearing = math.atan2(y, x)
        compass_bearing = (math.degrees(initial_bearing) + 360) % 360
        return math.radians(compass_bearing)
    
    @staticmethod
    def getDistance(latLong1, latLong2):
        lat1, lon1 = latLong1.getLat(), latLong1.getLong()
        lat2, lon2 = latLong2.getLat(), latLong2.getLong()
        lon = lon2 - lon1 
        lat = lat2 - lat1 
        a = math.sin(lat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(lon/2)**2
        c = 2 * math.asin(math.sqrt(a)) 
        return c * R

    @staticmethod
    def getApproxCartesianDist(locn1, locn2):
        bearing = Location.getBearing(locn1, locn2)
        dist = Location.getDistance(locn1, locn2)
        dx = dist*math.sin(bearing)
        dy = dist*math.cos(bearing)
        dz = locn2.getElev() - locn1.getElev()
        return (dx, dy, dz)
    
    @staticmethod
    def getApproxCartesianWaypoints(waypoints, initLatLong):
        cartesianLocs = [[0, 0, 0]]
        dx, dy, dz = Location.getApproxCartesianDist(initLatLong, waypoints[0])
        cartesianLocs.append([dx, dy, dz])
        for i in range(1, len(waypoints)):
            [dx, dy, dz] = Location.getApproxCartesianDist(waypoints[i-1], waypoints[i])
            [x, y, z] = cartesianLocs[-1]
            cartesianLocs.append([x+dx, y+dy, z+dz])
        return cartesianLocs
