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
    
    # process() extracts important info out of the ErrorMessage and updates the class parameters
    def process(self):
        pattern4 = r'Field "(.*?)" argument "(.*?)" of type "(.*?)!" is required, but it was not provided\.'
        pattern3 = r'Field "(.*?)" of type ".*?" must have a selection of subfields\. Did you mean "(.*?) { ... }"\?'
        pattern2 = r'Cannot query field "(.*?)" on type "Query". Did you mean "(.*?)"\?'
        pattern1 = r'Cannot query field "(.*?)" on type "Query"\.'
        if re.match(pattern4, self.message):
            key_words = re.search(pattern4, self.message)
            self.guessed_word = key_words.group(1)
            self.arg = key_words.group(2)
            self.arg_type = key_words.group(3)
            print(self.guessed_word)
        elif re.match(pattern3, self.message):
            key_words = re.search(pattern3, self.message)
            self.guessed_word = key_words.group(1)
            self.real_word_type = key_words.group(2)
            self.real_word_subfields = True
            print(self.guessed_word)
        elif re.match(pattern2, self.message):
            key_words = re.search(pattern2, self.message)
            self.guessed_word = key_words.group(1)
            self.real_word = key_words.group(2)
            print(self.guessed_word)
        elif re.match(pattern1, self.message):
            self.guessed_word = re.search(pattern1, self.message).group(1)
            print(self.guessed_word)
        else:
            print(f'new error message: {self.message}')


# URL that we want to query                              -- this will later be a user input  
url = "https://graphql-catalog.app.iherb.com/"

# Create query from word_list                            -- this will later be loaded from a .txt file
word_list = ['account', 'pser', 'user']
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


field_list = []

# Psudo code:
i = 0                                       # set a counter to 0

for error in json_response['errors']:
    print(error['message'])
    current_guess = word_list[i]            # update the current guessed word
    current_error_message = ErrorMessage(error['message'])  # initialize ErrorMessage class
    current_error_message.process()         # call a function to populate ErrorMessage class variabes
    
    # The only reason the following doesn't work is that we aren't increasing i in the right place yet 
    # (ex: user appears twice as the guessed_word)

    # while(current_guess != current_error_message.guessed_word):  # while the error message word isn't the 
    #     new_field = Field(word_list[i])     # create a Field from the current_guess (no error means its a field)
    #     field_list.insert(0, new_field)        # add new field to list
    #     i += 1                              # increase counter by 1


#     if (current_error_message.real_word is not None):    # if the error message reveals a real word
#         new_field = current_error_message.guessed_word   # make a new field and add relevent info (args/subfields/etc)
    