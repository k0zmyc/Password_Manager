import base64

'''
Module imported from https://github.com/TadPal/Simple-Encryption with approval of the author - TadPal, 22KB

This module provides an Encoder class that encodes and decodes text using a private key and base64 encoding.
The module is used to ensure that sensitive information (password) is not stored in plain text in the database.

Class:
Encoder: An Encoder object used to encode and decode text using a private key and base64 encoding.

Methods:
encode(): Uses the transform method to shift character value and then encode it using base64.
decode(): Uses the transform method to shift character value back and then decode it using base64.

Attributes:
text: A string containing the password to be encoded/decoded.
private_key: A bytes object containing the private key to be used for encoding/decoding.
result: A string containing the result of the encoding/decoding operation.
name: A string representing the name of the encoding method used. (In this case, Base64) - not neccesary in this project, used in the original
'''

class Encoder:
    def __init__(self, password="", private_key=b''):
        self.text = password
        self.private_key = private_key
        self.result = ""
        self.name = "Base64"

#**************************************************************************************************************************************************************************************************

    def encode(self):
        '''Uses transform method to shift character value and then encode it using base64'''
        key = []
        for byte in self.private_key:
            key.append(str(byte)) 
        key = ''.join(key)

        def transform(key, message):
            enc = []
            # Iterate through each character in the message
            for i in range(len(message)):
                # Get the corresponding key character for the current message character
                key_c = key[i%len(key)]
                # Perform the encoding transformation and add the result to the list of encoded characters
                enc.append(chr((ord(message[i]) + ord(key_c)) % 256))
            # Encode the list of encoded characters using base64 and return the result
            return base64.urlsafe_b64encode("".join(enc).encode()).decode()

        # Perform the encoding transformation using the private key and message text and store the result
        self.result = transform(key, self.text)

#**************************************************************************************************************************************************************************************************

    def decode(self):
        '''Uses transform method to shift character value back and then decode it using base64'''
        key = []
        for byte in self.private_key:
            key.append(str(byte)) 
        key = ''.join(key)

        def transform(key, message):
            dec = []
            # Decode the message using base64
            message = base64.urlsafe_b64decode(message).decode()
            # Iterate through each character in the decoded message
            for i in range(len(message)):
                # Get the corresponding key character for the current message character
                key_c = key[i % len(key)]
                # Perform the decoding transformation and add the result to the list of decoded characters
                dec.append(chr((256 + ord (message[i]) - ord(key_c)) % 256))
            # Return the list of decoded characters as a string
            return "".join(dec)

        # Perform the decoding transformation using the private key and message text and store the result
        self.result = transform(key, self.text)
