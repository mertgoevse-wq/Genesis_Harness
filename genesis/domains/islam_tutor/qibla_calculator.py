import math

class QiblaCalculator:
    """Calculates Qibla direction based on the Kaaba's coordinates."""
    
    # Kaaba Coordinates
    KAABA_LAT = 21.4225
    KAABA_LON = 39.8262

    def calculate_direction(self, lat: float, lon: float) -> float:
        """Calculate bearing from given coordinates to Kaaba using spherical trigonometry."""
        lat_rad = math.radians(lat)
        lon_rad = math.radians(lon)
        kaaba_lat_rad = math.radians(self.KAABA_LAT)
        kaaba_lon_rad = math.radians(self.KAABA_LON)
        
        y = math.sin(kaaba_lon_rad - lon_rad)
        x = math.cos(lat_rad) * math.tan(kaaba_lat_rad) - math.sin(lat_rad) * math.cos(kaaba_lon_rad - lon_rad)
        
        bearing = math.degrees(math.atan2(y, x))
        return (bearing + 360) % 360

    def calculate_distance(self, lat: float, lon: float) -> float:
        """Calculate distance using Haversine formula (in km)."""
        R = 6371.0 # Earth radius in km
        lat_rad = math.radians(lat)
        lon_rad = math.radians(lon)
        kaaba_lat_rad = math.radians(self.KAABA_LAT)
        kaaba_lon_rad = math.radians(self.KAABA_LON)
        
        dlon = kaaba_lon_rad - lon_rad
        dlat = kaaba_lat_rad - lat_rad
        
        a = math.sin(dlat / 2)**2 + math.cos(lat_rad) * math.cos(kaaba_lat_rad) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c
