from modules.altumbase.users import get_diamonds_received, get_deso_locked

userlist = []
users = get_diamonds_received()
#users = get_deso_locked()

for user in users:
    print(user)
