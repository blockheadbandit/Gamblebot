import json
import os

#HELPER FUNCTIONS------------------------#
async def open_bank(user):
    users = await get_bank_info()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 100
        users[str(user.id)]["bank"] = 400
    with open("./UserData/Banks.json","w") as f:
        json.dump(users,f)
    return True

async def get_bank_info():
    with open("./UserData/Banks.json","r") as f:
        users = json.load(f)
    return users

async def update_bank(user,amn = 0,mode = "wallet"):
    users = await get_bank_info()

    users[str(user.id)][mode] += amn

    with open("./UserData/Banks.json","w") as f:
        json.dump(users,f)
    
    balance = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
    return balance
