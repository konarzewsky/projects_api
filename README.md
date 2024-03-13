# API to manage ```projects``` (plots of land)
Author: Wojciech Konarzewski

## How to run it locally?

1. Prerequisites
- installed git (used version: ```git version 2.34.1```)
- installed docker (used version: ```Docker version 25.0.3, build 4debf41```)
- installed docker-compose (used version: ```Docker Compose version v2.24.2```)

2. Clone this repository
```
git clone https://github.com/konarzewsky/projects_api.git
cd projects_api/
```

3. Prepare environment
```
cp .env.example .env
```

4. Build application
```
docker-compose build projects_api
```

5. Run application
```
docker-compose up projects_api
```
This command starts two services: **db** and **projects_api**. First launch of the **db_dev** service creates an empty postgres database and creates the "projects" table.

## Endpoints

- POST ```/projects/create``` (creates new project)

Example request:
```
curl -X POST -H "Auth-Token: SECRET_API_KEY" -H "Content-Type: application/json;charset=UTF-8" -d '{"name": "my_project","description": "my project description","date_start": "2024-01-01","date_end": "2024-01-31","area": {"type": "Feature","geometry": {"type": "Point","coordinates": [125.6, 10.1]}}}' http://0.0.0.0:5000/projects/create
```
Example response:
```
{
    "name":"my_project",
    "description":"my project description",
    "date_start":"2024-01-01",
    "date_end":"2024-01-31",
    "area":{"type":"Feature","geometry":{"type":"Point","coordinates":[125.6,10.1]}},
    "id":21,
    "created_at":"2024-03-13T15:59:11.893259",
    "updated_at":"2024-03-13T15:59:11.893259"
}
```

- GET ```/projects/read/{project_id}``` (returns project by id)

Example request:
```
curl -X GET -H "Auth-Token: SECRET_API_KEY" -H "Content-Type: application/json;charset=UTF-8" http://0.0.0.0:5000/projects/read/1
```
Example response:
```
{
    "name":"my_project",
    "description":"my project description",
    "date_start":"2024-01-01",
    "date_end":"2024-01-31",
    "area":{"type":"Feature","geometry":{"type":"Point","coordinates":[125.6,10.1]}},
    "id":1,
    "created_at":"2024-03-13T16:03:34.744572",
    "updated_at":"2024-03-13T16:03:34.744572"
}
```

- GET ```/projects/list``` (returns all projects)

Example request:
```
curl -X GET -H "Auth-Token: SECRET_API_KEY" -H "Content-Type: application/json;charset=UTF-8" http://0.0.0.0:5000/projects/list
```
Example response:
```
[
    {
        "name":"my_project",
        "description":"my project description",
        "date_start":"2024-01-01",
        "date_end":"2024-01-31",
        "area":{"type":"Feature","geometry":{"type":"Point","coordinates":[125.6,10.1]}},
        "id":1,
        "created_at":"2024-03-13T16:03:34.744572",
        "updated_at":"2024-03-13T16:03:34.744572"
    },
    {
        "name":"my_second_project",
        "description":"my second project description",
        "date_start":"2024-02-01",
        "date_end":"2024-02-15",
        "area":{"type":"Feature","geometry":{"type":"Point","coordinates":[52.97,21.12]}},
        "id":2,
        "created_at":"2024-03-13T16:05:57.549886",
        "updated_at":"2024-03-13T16:05:57.549886"
    }
]
```

- DELETE ```/projects/delete/{project_id}``` (deletes project by id)

Example request:
```
curl -X DELETE -H "Auth-Token: SECRET_API_KEY" -H "Content-Type: application/json;charset=UTF-8" http://0.0.0.0:5000/projects/delete/1
```
Example response:
```
{
    "detail":"Project (id=1) deleted"
}
```

- PATCH ```/projects/update/{project_id}``` (updates project by id)

Example request:
```
curl -X PATCH -H "Auth-Token: SECRET_API_KEY" -H "Content-Type: application/json;charset=UTF-8" -d '{"name": "updated_project_2"}' http://0.0.0.0:5000/projects/update/2
```
Example response:
```
{
    "name":"updated_project_2",
    "description":"my second project description",
    "date_start":"2024-02-01",
    "date_end":"2024-02-15",
    "area":{"type":"Feature","geometry":{"type":"Point","coordinates":[52.97,21.12]}},
    "id":2,
    "created_at":"2024-03-13T16:05:57.549886",
    "updated_at":"2024-03-13T16:11:02.318236"
}
```

## Development

- Sample requests can be made using files in ```/requests``` dir (e.g. ```bash requests/create_invalid.sh```)
- Check code ```bash lint.sh```
- Run tests ```bin/tests```
- Before pushing changes to remote ```bin/pre-push```
