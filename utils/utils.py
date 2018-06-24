import utm

# given a global gps pos and gps of home, find local utm relative to home.
# assume global_pos and home are in the same zone number and label for now
def gps2local(gps_pos, gps_home):
    utm_global_pos = utm.from_latlon(gps_pos[0], gps_pos[1])
    utm_home = utm.from_latlon(gps_home[0], gps_home[1])
    utm_local_pos = [utm_global_pos[i] - utm_home[i] for i in range(2)] + [-(gps_pos[2] - gps_home[2])]
    return utm_local_pos

# given a global gps pos and gps of home, find local utm relative to home
# assume global_pos and home are in the same zone number and label for now
def local2gps(local_pos, gps_home):
    utm_home = utm.from_latlon(gps_home[0], gps_home[1])
    utm_global_pos = [utm_home[0] + local_pos[0], utm_home[1] + local_pos[1], utm_home[2], utm_home[3]]
    gps_pos = list(utm.to_latlon(utm_global_pos[0], utm_global_pos[1], utm_global_pos[2], utm_global_pos[3])) + [-(local_pos[2]-gps_home[2])]
    return gps_pos

##############################################################################

def test_gps2local():
    gps_pos = [37.393037, -122.079465, 30]
    gps_home = [37.400154, -122.108432, 20]
    ret = [round(v, 2) for v in gps2local(gps_pos, gps_home)]
    assert(ret == [2571.59, -764.96, -10])

def test_local2gps():
    local_pos = [25.21, 128.07, -30.]
    gps_home = [37.400154, -122.108432, 20]
    ret = [round(v, 2) for v in local2gps(local_pos, gps_home)]
    assert(ret == [37.40, -122.11, 50])
    
def run_test():
    test_gps2local()
    test_local2gps()

if '__main__' == __name__:
    run_test()
