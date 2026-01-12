"""
Модуль с функциями шифра Виженера

Содержит:
- encrypt_vigenere(plaintext, keyword) -> str: шифрует текст
- decrypt_vigenere(ciphertext, keyword) -> str: расшифровывает текст
"""


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    for i, char in enumerate(plaintext):
        key_char = keyword[i % len(keyword)]
        if char.isupper():
            shift = ord(key_char.upper()) - 65
            ciphertext += chr((ord(char) - 65 + shift) % 26 + 65)
        elif char.islower():
            shift = ord(key_char.lower()) - 97
            ciphertext += chr((ord(char) - 97 + shift) % 26 + 97)
        else:
            ciphertext += char
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    for i, char in enumerate(ciphertext):
        key_char = keyword[i % len(keyword)]
        if char.isupper():
            shift = ord(key_char.upper()) - 65
            plaintext += chr((ord(char) - 65 - shift) % 26 + 65)
        elif char.islower():
            shift = ord(key_char.lower()) - 97
            plaintext += chr((ord(char) - 97 - shift) % 26 + 97)
        else:
            plaintext += char
    return plaintext
