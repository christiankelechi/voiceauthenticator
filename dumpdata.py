import json

# some JSON:
x =  { "email":"John@gmail.com","password":"1234"}

# parse x:
with open("user_login_data.json","w") as file:
    json.dump(x,file,indent=4)
# the result is a Python dictionary:
print(x)