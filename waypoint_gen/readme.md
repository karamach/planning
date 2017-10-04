# Waypoint Generation

# Introduction

The module generates intermediate  waypoints for a flight path, given a set of initial locations of interest. The goal while generating the path is to spend time at each of the locations of interests, while moving in a straight line trajectory between waypoints. The high level idea was to mimic the behavior of a drone or aerial vehicle that is on a search operation looking for and trying to identify objects of interest at certain likely locations. At each location, the path spirals down to a lesser altitude to do better object detection. 

# Parameters

The waypoint generation is controlled by the following parameters as used in the config file

* global_wp::d_step Distance between two intermediate waypoints
* local_wp::ini_rad Initial radius for local pattern
* local_wp::ha_step Angle between intermediate waypoints in local circular pattern
* local_wp::va_step Incremental increase in radius for concentric local search
* local_wp::elev_h Max elevation for local search
* local_wp::elev_l Min elevation for local search
* local_wpelev_step Incremental elevation change between intermediate waypoints between locations of interest

# Sample Output

Below is a sample output of the generated path. As can be the path spirals to a lower altitude at each location of interest and has a straight line trajectory between locations of interest.

![alt text](https://github.com/karamach/planning/blob/master/waypoint_gen/images/path.png)

# TODO
1. Employ shortest part to find optimal path between locations of interest.

# References
- http://www.movable-type.co.uk/scripts/latlong.html
- https://en.wikipedia.org/wiki/Decimal_degrees
- http://stackoverflow.com/questions/1185408/converting-from-longitude-latitude-to-cartesian-coordinates
- http://www.latlong.net/place/seattle-wa-usa-2655.html
- http://www.gps-coordinates.net/gps-coordinates-converter
- http://www.darrinward.com/lat-long/?id=2365962
- http://www.gpsvisualizer.com/map_input?form=data
- http://www.hamstermap.com/quickmap.php
