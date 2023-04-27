import requests
import json

# Class to keep track of Fields in the graphql schema
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

# Class to extract useful data from error messages
class ErrorMessage:
    def __init__(self):
        self.guessed_word          # string
        self.real_word             # string
        self.arg                   # string
        self.arg_type              # string
        self.real_word_type        # string
        self.real_word_subfields   # boolean

# URL that we want to query                              -- this will later be a user input  
url = "https://graphql-catalog.app.iherb.com/"

# Create query from word_list                            -- this will later be loaded from a .txt file
word_list = ['pser', 'account', 'user']
fields = ",\n".join(word_list)
query_template = "query {{\n  {fields}\n}}"
query = query_template.format(fields=fields)

payload = {
    "query": query
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())

# Examples of Error Messages:
    # 'message': 'Cannot query field "account" on type "Query".'
    # 'message': 'Cannot query field "pser" on type "Query". Did you mean "user"?'
    # 'message': 'Field "user" argument "id" of type "String!" is required, but it was not provided.'
    # 'message': 'Field "user" of type "User" must have a selection of subfields. Did you mean "user { ... }"?'
    # blank if a field is found but there are other errors

# How to extract the suggestion from the error message: 
    # error_message = response_json["errors"][0]["message"]
    # suggestion = error_message.split("Did you mean ")[1].strip(" '?")
    # print(suggestion)


field_list = [Field]

# Psudo code:

# load a .txt file of words and call it word_list

# i = 0                                       # set a counter to 0
# for error_message in response:              # range through the 'messages' in response (range n in response_json["errors"][n]["message"])
#     current_guess = word_list[i]            # update the current guessed word
#     current_error_message = ErrorMessage()  # initialize ErrorMessage class
#     current_error_message.process()         # call a function to populate ErrorMessage class variabes
#                                                     # ex: real_word = error_message.split("Did you mean ")[1].strip(" '?")
#     while(current_guess != current_error_message.guessed_word):  # while the error message word isn't the 
#         new_field = Field(word_list[i])     # create a Field from the current_guess (no error means its a field)
#         field_list.insert(new_field)        # add new field to list
#         i += 1                              # increase counter by 1

#     # by now the current_guess should == current_error_message.guessed_word

#     if (current_error_message.real_word is not None):    # if the error message reveals a real word
#         new_field = current_error_message.guessed_word   # make a new field and add relevent info (args/subfields/etc)
    