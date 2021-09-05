import csv
import nacl.secret
import nacl.utils
import nacl.pwhash
import getpass

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


def keepAskingUser(users, key):
    cmd = ""

    box = nacl.secret.SecretBox(key)

    while cmd != "exit":
        cmd = input("[read/write/exit]> ")
        if cmd == "read":
            name = input("Username: ")
            usersWithPassword = filter(lambda u: u.name == name, users)
            if usersWithPassword:
                for user in usersWithPassword:
                    decPasswd = box.decrypt(bytes.fromhex(user.password))
                    print(f"{user.site}: |{decPasswd.decode()}|")
            else:
                print("Username not found")
        elif cmd == "write":
            name = input("Username: ")
            site = input("Site: ")
            password = input("Password: ")

            encPasswd = box.encrypt(password.encode('utf-8'))

            users.append(User(name, site, encPasswd.hex()))


def saveUserFile(users, filename):
    with open(filename, "w") as csvfile:
        userWriter = csv.writer(csvfile, delimiter=DELIMITER)
        for user in users:
            userWriter.writerow([user.name, user.site, user.password])

def readPassword():
    kdf = nacl.pwhash.argon2i.kdf

    try:
        with open("salt") as fp:
            salt = bytes.fromhex(fp.readline())
    except FileNotFoundError:
        print("salt file not found")
        quit()

    ops = nacl.pwhash.argon2i.OPSLIMIT_SENSITIVE
    mem = nacl.pwhash.argon2i.MEMLIMIT_SENSITIVE

    password = getpass.getpass().encode('utf-8')

    key = kdf(nacl.secret.SecretBox.KEY_SIZE, password, salt,
                 opslimit=ops, memlimit=mem)

    return key

def main():
    users = readUsernamesFile(FILENAME)
    key = readPassword()
    keepAskingUser(users, key)
    saveUserFile(users, FILENAME)


if __name__ == '__main__':
    main()
