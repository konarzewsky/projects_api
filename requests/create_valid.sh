export API_URL=http://0.0.0.0:5000/projects
export API_AUTH_TOKEN=SECRET_API_KEY

curl -X POST -H "X-API-KEY: $API_AUTH_TOKEN" -H "Content-Type: application/json;charset=UTF-8" -d '{"name": "my_project","description": "my project description","date_start": "2024-01-01","date_end": "2024-01-31","area": {"type": "Feature","geometry": {"type": "Point","coordinates": [125.6, 10.1]}}}' $API_URL/create