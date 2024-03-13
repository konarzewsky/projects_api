export API_URL=http://0.0.0.0:5000/projects
export API_AUTH_TOKEN=SECRET_API_KEY

curl -X DELETE -H "Auth-Token: $API_AUTH_TOKEN" -H "Content-Type: application/json;charset=UTF-8" $API_URL/delete/1