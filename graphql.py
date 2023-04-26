import requests
import json

class Field:
    def __init__(self, Name):
        self.kind   #Str         # kimd of Field            ex: SCALAR  or  OBJECT  or  NON_NULL
        self.name = Name         # String name of Field            ex: User
        self.args = []           # list of arguments        ex: User (id: xx)    id is an args
        self.description  #Str   # description of Field      
        self.subfields = []      #
        self.isDeprecated        # Boolean
        self.deprecationReason = "null"         # change if isDeprecated == True
        self.type = {
            "kind",
            "name",
            "ofType"
        }                       # dictionary used to classfy subiems
        self.locations = []     # not sure what this is used for (array of strings)

class ErrorMessage:
    def __init__(self):
        self.guessed_word          # string
        self.real_word             # string
        self.arg                   # string
        self.arg_type              # string
        self.real_word_type        # string
        self.real_word_subfields   # boolean

url = "https://graphql-catalog.app.iherb.com/"

query = '''
    query {
        blog(id:1) {
            name
        },
        account,
        user
    }
'''

payload = {
    "query": query
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())

# Extract the suggestion from the error message
# error_message = response_json["errors"][0]["message"]
# suggestion = error_message.split("Did you mean ")[1].strip(" '?")
# print(suggestion)
