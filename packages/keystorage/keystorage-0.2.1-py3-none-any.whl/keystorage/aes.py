"""
En este archivo esta todo lo necesario para 
cifrar de manera rapida texto plano a traves 
del cifrado AES
"""
import base64
import hashlib

from Crypto.Cipher import AES

def sha256_32b_generator(key:str) -> str:
    """
    Encargada de retornar una cadena de 32 bytes
    generada con SHA256
    """
    sha_hash = hashlib.sha256(key.encode())  # Se genera un hash de 64 bytes
    sha_hash = sha_hash.hexdigest()
    return sha_hash[:32] #Retornamos solo los 32 primeros bytes para poder utilizarlo como clave para AES

def encrypt_16b_message(message:str, key:str) -> bytes:
    """
    Encargada de encriptar mensajes concretos de 16 bytes
    """
    assert len(message) == 16, "The length of the message must be 16 bytes"
    assert len(key) == 32, "The length of the key must be 32 bytes"
    cipher = AES.new(key)
    return cipher.encrypt(message)

def encrypt(message:str, key:str) -> bytes:
    """
    Encargada de encriptar las claves, a traves de AES.
    retorna un string en codificación utf-16
    """ 
    key_hash = sha256_32b_generator(key) # Se crea la clave de 32 bytes

    message_to_encrypt = split_message(message, 16,padding=True)
    encrypted_message = b""

    for part in message_to_encrypt:
        encrypted = encrypt_16b_message(part, key_hash)
        encrypted_message += encrypted


    return base64.b64encode(encrypted_message).decode("utf-8")    

def add_padding_message(message:str) -> str:
    """
    Se encarga de rellenar con espacios 
    el mensaje hasta llegar a 16 bytes
    """

    assert len(message) < 16, "the length of the message must be less than 16 bytes"
    assert not "ñ" in message, "for now ñ's are not accepted"
    len_message = len(message)

    while len_message < 16:
            message += " "
            len_message += 1

    return message

def remove_padding_message(message:str) -> str:
    """
    Se encarga de quitar el relleno a los mensajes
    """
    return message.strip()


def split_message(message:str, large:int ,padding:bool = False) -> list:
    """
    Encargada de dividir un string en x grupos
    de 16 bytes y luego juntarlos en una lista
    """
    message_list = []
    
    while len(message) > large:
        split_16b = message[:large]
        message = message[large:]
        message_list.append(split_16b)
    
    if padding and len(message) > 0 and len(message) < 16:
        message = add_padding_message(message)
    
    message_list.append(message)
    
    return(message_list)

def decrypt(message:str, key:str) -> str:
    """
    Encargada de desencriptar mensajes
    """
    message_bytes = message.encode("utf-8")
    message_bytes = base64.b64decode(message_bytes)

    message_bytes_list = split_message(message_bytes, 16)

    shaKey = sha256_32b_generator(key)

    cipher = AES.new(shaKey)
    decrypt_messages = ""
    for element in message_bytes_list:
        decrypt_message = cipher.decrypt(element) 
        decrypt_messages += decrypt_message.decode("utf-8")

    return decrypt_messages.rstrip()