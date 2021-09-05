import nacl.secret
import nacl.utils
import nacl.pwhash

def main():
    salt = nacl.utils.random(nacl.pwhash.argon2i.SALTBYTES)

    with open("salt", "w") as fp:
        fp.write(salt.hex())


if __name__=='__main__':
    main()