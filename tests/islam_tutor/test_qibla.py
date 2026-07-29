from genesis.domains.islam_tutor.qibla_calculator import QiblaCalculator

def test_qibla_direction_from_berlin():
    calc = QiblaCalculator()
    # Berlin coords
    lat = 52.5200
    lon = 13.4050
    direction = calc.calculate_direction(lat, lon)
    # Berlin Qibla is roughly 136-137 degrees
    assert 135 < direction < 138

def test_qibla_distance_from_berlin():
    calc = QiblaCalculator()
    lat = 52.5200
    lon = 13.4050
    dist = calc.calculate_distance(lat, lon)
    # Roughly 4100 - 4200 km
    assert 4000 < dist < 4500
