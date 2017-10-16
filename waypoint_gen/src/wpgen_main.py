import ConfigParser
import sys

from location import *
from global_nav import *
from local_nav import *
from utils import *

def usage():
    print "Usage: python wpgen_main.py <loc_of_interest_file> <out_waypoints>"

def getLocation(raw_loc):
    return Location([math.radians(float(raw_loc[0])), math.radians(float(raw_loc[1])), float(raw_loc[2])])

def main():
    if len(sys.argv) != 3:
        usage()
        exit()

    loc_of_interest = sys.argv[1]
    out_waypoints = sys.argv[2]
     
    data = filter(lambda x: not x.startswith("#") , open(loc_of_interest, "r").readlines())
    locations = [getLocation(location.rstrip().split(",")) for location in data] 

    cfg = ConfigParser.ConfigParser()
    cfg.readfp(open("config.cfg"))
    local_wp = LocalWP(cfg)
    global_wp = GlobalWP(cfg, local_wp)

    waypoints = [locations[0]] + global_wp.getWaypoints(locations[1:len(locations)-1]) + [locations[-1]]
    out = open(out_waypoints, "w")
    for waypoint in waypoints:
        out.write(str(waypoint) + "\n")
    out.close()

    cartesian = Location.getApproxCartesianWaypoints(waypoints, locations[0])    
    plot([x[0] for x in cartesian], [x[1] for x in cartesian], [x[2] for x in cartesian])

if __name__ == "__main__":
    main()

