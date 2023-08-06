from invoke import task


@task(help={"filename": "The filename to encrypt."})
def encrypt(c, filename):
    """
    Generate an encrypted version of the file using OpenSSL.
    """
    c.run(
        f'openssl aes-256-cbc -md sha256 -k "$DECRYPT_PASSWORD" -in {filename} -out {filename}.enc'
    )


@task(help={"filename": "The filename (not including .enc) to decrypt."})
def decrypt(c, filename):
    """
    Generate an decrypted version of the file using OpenSSL.
    """
    c.run(
        f'openssl aes-256-cbc -md sha256 -k "$DECRYPT_PASSWORD" -in {filename}.enc -out {filename} -d'
    )
