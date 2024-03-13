export API_URL=http://0.0.0.0:5000/projects
export API_AUTH_TOKEN=SECRET_API_KEY

curl -X PATCH -H "Auth-Token: $API_AUTH_TOKEN" -H "Content-Type: application/json;charset=UTF-8" -d '{"name": "updated_project"}' $API_URL/update/10000000