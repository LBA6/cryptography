import requests
import urllib3
from random import randint
from Cryptodome.Util import number

# Function to calculate the Greatest Common Divisor (GCD) using the Euclidean algorithm
def gcd(x, y):
    if x < y:
        return gcd(y, x)
    elif x % y == 0:
        return y
    else:
        return gcd(y, x % y)

# Generate a random key that is coprime with q
def gen_key(prime_nb):
    key = randint(2, prime_nb - 1)
    while gcd(prime_nb, key) != 1:
        key = randint(2, prime_nb - 1)
    return key

# Encrypt the message
def encrypt(msg, prime_nb, dest_pub_key, gen):
    key = gen_key(prime_nb)  # Ephemeral private key
    shared_secret = pow(dest_pub_key, key, prime_nb)  # Shared secret
    pub_key = pow(gen, key, prime_nb)  # Public ephemeral key

    enc_msg = [(ord(char) * shared_secret) % prime_nb for char in msg]  # Encrypt each character
    return enc_msg, pub_key

# Decrypt the message
def decrypt(enc_msg, pub_key, priv_key, prime_nb):
    shared_secret = pow(pub_key, priv_key, prime_nb)  # Shared secret
    s_inv = pow(shared_secret, -1, prime_nb)  # Modular inverse of shared secret

    dec_msg = [chr((char * s_inv) % prime_nb) for char in enc_msg]  # Decrypt each character
    return dec_msg


# Disable SSL certificate verification
urllib3.disable_warnings()

def register():
    data = {}
    response = requests.post('http://127.0.0.1:5000/get_users', json=data, verify=False)
    users = response.json()['users']
    created_users = eval(users)
    
    username = input("Enter username: ")

    while username in created_users:
        username = str(input(f"\nUser {username} already registered.\nEnter a new username: "))

    prime_nb = number.getPrime(1024)
    gen = randint(2, prime_nb - 1)
    print(f"Your prime number is: {prime_nb}\nYour generator is:  {gen}")

    priv_key = gen_key(prime_nb)
    pub_key = pow(gen, priv_key, prime_nb)
    print(f"Your private key is: {priv_key}\nYourpublic key is: {pub_key}")

    data = {'username': username, 'prime_nb': prime_nb, 'gen': gen, 'pub_key':pub_key}
    response = requests.post('http://127.0.0.1:5000/register', json=data, verify=False)
    print(response.json()['message'])
    return (username, priv_key, prime_nb)

def write_message(username):
    data={}
    response = requests.post('http://127.0.0.1:5000/get_users', json=data, verify=False)
    users = response.json()['users']
    user_list = eval(users)
    user_list.remove(username)

    print("\nList of users :")
    for user in user_list: print(user)

    user = str(input("\nEnter the name of the dest: "))
    if user not in user_list:
        user = str(input("Unvalid user.\nEnter the name of the dest: "))

    data={'user':user}
    response = requests.post('http://127.0.0.1:5000/get_user_data', json=data, verify=False)
    user_data = response.json()

    msg = input("Message: ")

    enc_message, pub_key = encrypt(msg, user_data['prime_nb'], user_data['pub_key'], user_data['gen'])

    data = {'sender':username, 'dest': user, 'message': enc_message, 'public_key': pub_key}
    response = requests.post('http://127.0.0.1:5000/send_message', json=data, verify=False)
    print(response.json()['message'])

def read_message(username, private_key, prime_nb):
    data={'username':username}
    response = requests.post('http://127.0.0.1:5000/read_messages', json=data, verify=False)
    messages = response.json()['messages']

    if not messages:
        print("No message.")
    else:
        for mess in messages:
            sender = mess[0]
            sender_pub_key = int(mess[1])
            enc_msg = mess[2]

            dec_msg = ''.join(decrypt(enc_msg, sender_pub_key, private_key, prime_nb))

            print(f"-----\nSender: {sender}\nmessage : {dec_msg}\n-----")


def main():
    print("You need to register")
    username, private_key, prime_nb = register()
    while True:
        choice = input("\nChoose an option (1: Send message, 2: Read message, 3: Exit): ")
        if choice == "1":
            write_message(username)
        elif choice == "2":
            read_message(username, private_key, prime_nb)
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

main()
