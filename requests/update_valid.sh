export API_URL=http://0.0.0.0:5000/projects

curl -X PATCH -H "Content-Type: application/json;charset=UTF-8" -d '{"name": "updated_project_1"}' $API_URL/update/1