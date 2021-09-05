import csv

FILENAME = "username.csv"
DELIMITER = ','


class User:
    def __init__(self, name, site, password):
        self.name = name
        self.site = site
        self.password = password


def readUsernamesFile(fileName):
    users = []
    try:
        with open(fileName) as csvfile:
            userReader = csv.reader(csvfile, delimiter=DELIMITER)
            users = [User(row[0], row[1], row[2]) for row in userReader]
    except FileNotFoundError:
        users = []
    return users


def keepAskingUser(users):
    cmd = ""
    while cmd != "exit":
        cmd = input("[read/write/exit]> ")
        if cmd == "read":
            name = input("Username: ")
            usersWithPassword = filter(lambda u: u.name == name, users)
            if usersWithPassword:
                for user in usersWithPassword:
                    print(f"{user.site}: |{user.password}|")
            else:
                print("Username not found")
        elif cmd == "write":
            name = input("Username: ")
            site = input("Site: ")
            password = input("Password: ")

            users.append(User(name, site, password))


def saveUserFile(users, filename):
    with open(filename, "w") as csvfile:
        userWriter = csv.writer(csvfile, delimiter=DELIMITER)
        for user in users:
            userWriter.writerow([user.name, user.site, user.password])


def main():
    users = readUsernamesFile(FILENAME)
    keepAskingUser(users)
    saveUserFile(users, FILENAME)


if __name__ == '__main__':
    main()

