import hashlib
import base64

from secrets import token_bytes

from utils.random_password_generator import generate_password
from utils.read_configuration import read_configuration


def create_user_credentials(config: dict()):
# TODO: This function only offers digest PBE. Offer options for strong / weak PBE and plain text.
    """
    This function creates a list of tuples containing the
    username, hashed password, and password. These can then 
    be inserted in a usergroup.xml of the geoserver.
    """
    
    # read the configuration
    configuration = read_configuration(config)

    # get list of required users
    users = configuration['users']
    
    # initialize empty list to store the credentials
    user_credentials = []

    # define location of stored secrets
    stored_secrets = configuration['stored_secrets']

    for user in users:

        # create a random password and a random 16 bit salt token per user
        name = user
        password = generate_password()
        salt = token_bytes(16)

        # prepend the salt to the random password and hash for 100.000 times
        prepended_string = salt + password.encode()
        sha256_hash = prepended_string
        for _ in range(100000):
            sha256_hash = hashlib.sha256(sha256_hash).digest()

        # prepend the salt to the final hash
        final_hash_with_salt = salt + sha256_hash

        # encode the combined byte string to base64
        base64_encoded = base64.b64encode(final_hash_with_salt)

        # decode to text
        password_hash = base64_encoded.decode()

        # collect credentials als line of text as written to stored_secrets
        secret = user + '   ' + password_hash + '   ' + password

        # open secrets
        with open(stored_secrets, "r") as read_secrets:
            content = read_secrets.read()

        # check if user is already in the secrets.txt
        # if so
        if user in content:
            with open(stored_secrets, "r") as file:
                lines = file.readlines()

            # Find the line that starts with the search name
            for i, line in enumerate(lines):
                if line.startswith(user):
                    lines[i] = secret + "\n"
                    break

                # Write the modified lines back to the file
                with open(stored_secrets, "w") as file:
                    file.writelines(lines)
                print(f"INFO: Credentials for {user} have been updated.")

        # if not
        else:
            with open(stored_secrets, "a") as write_secrets:
                write_secrets.write(secret + "\n")
            print(f"INFO: Credentials for user {user} created.")

          # collect the credentials for output
        user_credentials.append((name, password_hash, password))

    return user_credentials