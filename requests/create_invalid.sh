export API_URL=http://0.0.0.0:5000/projects

curl -X POST -H "Content-Type: application/json;charset=UTF-8" -d '{"name": "my_project","description": "my project description","date_start": "2024-01-01","date_end": "2024-01-31","area": {"type": "FeatureCollection","geometry": {"type": "Point","coordinates": [125.6, 10.1]}}}' $API_URL/create