import random

N_PROJECTS = 20


def generate_position() -> list:
    lon = random.uniform(-180, 180)
    lat = random.uniform(-90, 90)
    return [lon, lat]


def generate_feature(geometry: str) -> dict | None:
    feature = {"type": "Feature", "geometry": {"type": geometry}}
    match geometry:
        case "Point":
            feature["geometry"]["coordinates"] = generate_position()
        case "Multipoint":
            feature["geometry"]["coordinates"] = [
                generate_position() for _ in range(random.randint(2, 20))
            ]
        case "Polygon":
            feature["geometry"]["coordinates"] = [
                [generate_position() for _ in range(random.randint(2, 20))]
                for _ in range(random.randint(2, 20))
            ]
        case "MultiPolygon":
            feature["geometry"]["coordinates"] = [
                [
                    [generate_position() for _ in range(random.randint(2, 20))]
                    for _ in range(random.randint(2, 20))
                ]
                for _ in range(random.randint(2, 20))
            ]
        case _:
            return
    return feature


VALID_GEOJSONS = [
    generate_feature("Point"),
    generate_feature("Multipoint"),
    generate_feature("Polygon"),
    generate_feature("MultiPolygon"),
    {
        "type": "FeatureCollection",
        "features": [generate_feature("Point"), generate_feature("Polygon")],
    },
]

INVALID_GEOJSONS = [
    {
        "type": "FeatureCollection",
        "geometry": {"type": "Point", "coordinates": [52, 21]},
    },
    {"type": "Feature", "geometry": {"type": "Point", "coordinates": [52, 120]}},
    {
        "type": "FeatureCollection",
        "geometry": {"type": "Multipoint", "coordinates": [52, 21]},
    },
    {"type": "Multipoint", "coordinates": [[52, 21], [53, 22], [54, 23]]},
    {"type": "Feature", "geometry": {"type": "Point", "coordinates": []}},
    {},
]

VALID_PROJECTS = [
    {
        "name": f"project_{i}",
        "description": random.choice([f"project_{i} description", None]),
        "date_start": random.choice(["2024-02-15", "2024-01-21", "2024-03-01"]),
        "date_end": random.choice(["2024-03-01", "2024-03-05", "2024-03-10"]),
        "area": random.choice(VALID_GEOJSONS),
    }
    for i in range(1, N_PROJECTS + 1)
]

INVALID_PROJECTS = [
    {
        "name": None,
        "description": "project description",
        "date_start": "2024-02-15",
        "date_end": "2024-03-05",
        "area": random.choice(VALID_GEOJSONS),
    },
    {
        "name": "project with a very long name that exceeds the character limit",
        "description": "project description",
        "date_start": "2024-02-15",
        "date_end": "2024-03-05",
        "area": random.choice(VALID_GEOJSONS),
    },
    {
        "name": 10,
        "description": "project description",
        "date_start": "2024-02-15",
        "date_end": "2024-03-05",
        "area": random.choice(VALID_GEOJSONS),
    },
    {
        "name": "my_project",
        "description": "project description",
        "date_start": "2024-02-15",
        "date_end": "2024-02-05",
        "area": random.choice(VALID_GEOJSONS),
    },
    {
        "name": "my_project",
        "description": "project description",
        "date_start": "2024-02-15",
        "date_end": None,
        "area": random.choice(VALID_GEOJSONS),
    },
    {
        "name": "my_project",
        "description": "project description",
        "date_start": "2024-02-15",
        "date_end": "2024-03-01",
        "area": None,
    },
]

INVALID_GEOJSON_PROJECTS = [
    {
        "name": f"project_{i}",
        "description": random.choice([f"project_{i} description", None]),
        "date_start": random.choice(["2024-02-15", "2024-01-21", "2024-03-01"]),
        "date_end": random.choice(["2024-03-01", "2024-03-05", "2024-03-10"]),
        "area": geojson,
    }
    for i, geojson in enumerate(INVALID_GEOJSONS)
]
