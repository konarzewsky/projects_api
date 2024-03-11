import random

VALID_PROJECTS = [
    {
        "name": f"project_{i}",
        "description": random.choice([f"project_{i} description", None]),
        "date_start": random.choice(["2024-02-15", "2024-01-21", "2024-03-01"]),
        "date_end": random.choice(["2024-03-01", "2024-03-05", "2024-03-10"]),
        "area": "",  # TODO: add valid geojson
    }
    for i in range(10)
]

INVALID_PROJECTS = [
    {
        "name": None,
        "description": "project description",
        "date_start": "2024-02-15",
        "date_end": "2024-03-05",
        "area": "",  # TODO: add valid geojson
    },
    {
        "name": "project with a very long name that exceeds the character limit",
        "description": "project description",
        "date_start": "2024-02-15",
        "date_end": "2024-03-05",
        "area": "",  # TODO: add valid geojson
    },
    {
        "name": 10,
        "description": "project description",
        "date_start": "2024-02-15",
        "date_end": "2024-03-05",
        "area": "",  # TODO: add valid geojson
    },
    {
        "name": "my_project",
        "description": "project description",
        "date_start": "2024-02-15",
        "date_end": "2024-02-05",
        "area": "",  # TODO: add valid geojson
    },
    {
        "name": "my_project",
        "description": "project description",
        "date_start": "2024-02-15",
        "date_end": None,
        "area": "",  # TODO: add valid geojson
    },
    {
        "name": "my_project",
        "description": "project description",
        "date_start": "2024-02-15",
        "date_end": "2024-03-05",
        "area": None,  # TODO: add invalid geojson
    },
]
