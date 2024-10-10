import json

def storeCredentials(email,password):
    # some JSON:
    x =  { "email":email,"password":password}
    # parse x:
    with open("user_login_data.json","w") as file:
        json.dump(x,file,indent=4)
    # the result is a Python dictionary:
    print("file saved successfully")

# storeCredentials("Jerome@gmail.com","1234")