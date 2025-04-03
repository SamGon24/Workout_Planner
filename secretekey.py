import secrets

def generate_secret_key():
    # Generate a random 32-byte hexadecimal key
    secret_key = secrets.token_hex(32)
    return secret_key

if __name__ == "__main__":
    print("Your generated secret key is:")
    print(generate_secret_key())