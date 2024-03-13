export API_URL=http://0.0.0.0:5000/projects

curl -X PATCH -H "Content-Type: application/json;charset=UTF-8" -d '{"name": "updated_project"}' $API_URL/update/10000000