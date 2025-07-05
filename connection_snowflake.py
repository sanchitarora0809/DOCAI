import snowflake.connector
import os
import sys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization
sys.path.append("..")


def get_snowflake_conn():
    # Insted of this we will have it on key vault
    current_directory = os.path.dirname(os.path.abspath(__file__))
    key_path = os.path.join(current_directory, '', 'rsa_key.p8')

    with open(key_path, "rb") as key:
        p_key= serialization.load_pem_private_key(
            key.read(),
            password='123'.encode(),
            backend=default_backend()
        )

    pkb = p_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption())


    ctx = snowflake.connector.connect(
            user='sanchit.arora@cginfinity.com',
            account='VLB03298-CGINFINITY_PARTNER',
            private_key=pkb,
            warehouse='docai_wh',
            role='DOCUMENT_AI',
            database='Marketplace',
            schema='RAW_DOCS'
        )
    

    return ctx

def disconnect_snowflake(conn):
    conn.close()

if __name__ == "__main__":
    connection = get_snowflake_conn()
    print("Connection established!")


