import requests
import json

url = "https://graphql-catalog.app.iherb.com/sdfxghjk"

query = '''
    query {
        pser(id: "admin") {
            id
        }
    }
'''

payload = {
    "query": query
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, data=json.dumps(payload), headers=headers)

# print(response.json())
# {'errors': [{'message': 'Cannot query field "pser" on type "Query". Did you mean "user"?', 'locations': [{'line': 3, 'column': 9}], 'extensions': {'code': 'GRAPHQL_VALIDATION_FAILED'}}]}

response_string = json.dumps(response.json())
response_json = json.loads(response_string)

# Extract the suggestion from the error message
error_message = response_json["errors"][0]["message"]
suggestion = error_message.split("Did you mean ")[1].strip(" '?")
print(suggestion)






