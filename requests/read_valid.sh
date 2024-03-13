export API_URL=http://0.0.0.0:5000/projects
export API_AUTH_TOKEN=SECRET_API_KEY

curl -X GET -H "Auth-Token: $API_AUTH_TOKEN" -H "Content-Type: application/json;charset=UTF-8" $API_URL/read/1