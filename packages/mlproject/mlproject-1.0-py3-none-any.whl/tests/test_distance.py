
from mlproject.distance import haversine
#Paris
lat_paris=48.86
lon_paris=2.33
#Lyon
lat_lyon=45.76
lon_lyon=4.83

distance = haversine(lon_paris, lat_paris, lon_lyon, lat_lyon)

def test_distance_paris_lyon():
    assert (distance >390 and distance <396)
