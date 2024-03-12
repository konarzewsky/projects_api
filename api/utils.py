import logging
import sys
from typing import Any

from config.env import LOG_LEVEL


def prepare_logger():
    logger = logging.getLogger()
    logger.setLevel(level=LOG_LEVEL)
    formatter = logging.Formatter(
        "%(asctime)s,%(msecs)d %(levelname)-8s [%(pathname)s:%(lineno)d] %(message)s"
    )
    if not logger.handlers:
        lh = logging.StreamHandler(sys.stdout)
        lh.setFormatter(formatter)
        logger.addHandler(lh)
    return logger


def validate_geojson(v: dict) -> bool:
    """
    simple geojson validator (it checks basic assumptions only)
    based on https://datatracker.ietf.org/doc/html/rfc7946
    """
    if "type" not in v:
        return False

    match v["type"]:
        case "FeatureCollection":
            if "features" not in v:
                return False
            elif not isinstance(v["features"], list):
                return False
            features = v["features"]
        case "Feature":
            features = [v]
        case _:
            return False

    for f in features:
        if "type" not in f or f.get("type") != "Feature":
            return False
        if "geometry" not in f or not isinstance(f.get("geometry"), dict):
            return False
        if "coordinates" not in f["geometry"]:
            return False

        coordinates = f["geometry"]["coordinates"]

        match f["geometry"]["type"]:
            case "Point":
                if not validate_position(coordinates):
                    return False
            case "Multipoint" | "LineString":
                if not isinstance(coordinates, list):
                    return False
                if not all([validate_position(position) for position in coordinates]):
                    return False
            case "Polygon" | "MultiLineString":
                if not coordinates or not isinstance(coordinates, list):
                    return False
                for coordinates_a in coordinates:
                    if not validate_positions_array(coordinates_a):
                        return False
            case "MultiPolygon":
                if not coordinates or not isinstance(coordinates, list):
                    return False
                for coordinates_a in coordinates:
                    if not coordinates_a or not isinstance(coordinates_a, list):
                        return False
                    for coordinates_b in coordinates_a:
                        if not validate_positions_array(coordinates_b):
                            return False
            case _:
                return False

    return True


def validate_position(position: Any) -> bool:
    """
    Validates coordinates (longitude, latitude)
    Validation for the third optional element which is altitude/elevation is skipped
    """
    if not isinstance(position, list):
        return False
    if len(position) < 2 or len(position) > 3:
        return False
    try:
        lat = float(position[1])
        lon = float(position[0])
    except ValueError:
        return False
    if not (-90 <= lat <= 90):
        return False
    if not (-180 <= lon <= 180):
        return False
    return True


def validate_positions_array(positions: Any) -> bool:
    if not isinstance(positions, list):
        return False
    if not all([validate_position(position) for position in positions]):
        return False
    return True
