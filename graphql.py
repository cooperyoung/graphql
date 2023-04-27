import requests
import json
import re

# Class to keep track of Fields in the graphql schema
class Field:
    def __init__(self, Name):
        self.kind = None   #Str         # kind of Field            ex: SCALAR  or  OBJECT  or  NON_NULL
        self.name = Name         # String name of Field            ex: User
        self.args = []           # list of arguments        ex: User (id: xx)    id is an args
        self.description = None  #Str   # description of Field      432q     sa
        self.subfields = []      #
        self.isDeprecated = False        # Boolean
        self.deprecationReason = None         # change if isDeprecated == True
        self.type = {
            "kind",
            "name",
            "ofType"
        }                       # dictionary used to classfy subiems
        self.locations = []     # not sure what this is used for (array of strings)

# Class to extract useful data from error messages
class ErrorMessage:
    def __init__(self, error_message):
        self.guessed_word = None         # string
        self.real_word = None             # string
        self.arg = None                  # string
        self.arg_type = None              # string
        self.real_word_type = None        # string
        self.real_word_subfields = None   # boolean
        self.message = error_message
        

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
json_response = response.json()

# Examples of Error Messages:
    # 'message': 'Cannot query field "account" on type "Query".'
    # 'message': 'Cannot query field "pser" on type "Query". Did you mean "user"?'
    # 'message': 'Field "user" argument "id" of type "String!" is required, but it was not provided.'
    # 'message': 'Field "user" of type "User" must have a selection of subfields. Did you mean "user { ... }"?'
    # blank if a field is found but there are other errors


field_list = [Field]

# Psudo code:
i = 0                                       # set a counter to 0

for error in json_response['errors']:
    print(error['message'])
    current_guess = word_list[i]            # update the current guessed word
    current_error_message = ErrorMessage(error['message'])  # initialize ErrorMessage class

#    current_error_message.process()         # call a function to populate ErrorMessage class variabes
#                                                     # ex: real_word = error_message.split("Did you mean ")[1].strip(" '?")
#     while(current_guess != current_error_message.guessed_word):  # while the error message word isn't the 
#         new_field = Field(word_list[i])     # create a Field from the current_guess (no error means its a field)
#         field_list.insert(new_field)        # add new field to list
#         i += 1                              # increase counter by 1

#     # by now the current_guess should == current_error_message.guessed_word

#     if (current_error_message.real_word is not None):    # if the error message reveals a real word
#         new_field = current_error_message.guessed_word   # make a new field and add relevent info (args/subfields/etc)
    