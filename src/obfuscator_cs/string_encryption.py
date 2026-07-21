import base64
import os
from typing import Tuple
# Requires: pip install pycryptodome
try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad
except ImportError:
    AES = None

class StringEncryptor:
    """
    Performs compile-time AES-256 (Rijndael) encryption on C# literal strings.
    Generates dynamic C# decryption routines to embed in the target AST.
    """
    def __init__(self):
        self.key = os.urandom(32) # 256-bit key
        self.iv = os.urandom(16)  # 128-bit IV
        
    def encrypt_string(self, plaintext: str) -> str:
        """Encrypts a string and returns it as a Base64 encoded payload."""
        if AES is None:
            raise RuntimeError("pycryptodome is required for AST string encryption.")
            
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        padded_data = pad(plaintext.encode('utf-8'), AES.block_size)
        encrypted_bytes = cipher.encrypt(padded_data)
        
        return base64.b64encode(encrypted_bytes).decode('utf-8')

    def generate_csharp_decryption_stub(self, method_name: str = "DecryptString") -> str:
        """
        Generates the C# method required to decrypt the strings at runtime.
        """
        b64_key = base64.b64encode(self.key).decode('utf-8')
        b64_iv = base64.b64encode(self.iv).decode('utf-8')

        return f"""
public static string {method_name}(string cipherText)
{{
    byte[] cipherBytes = Convert.FromBase64String(cipherText);
    byte[] key = Convert.FromBase64String("{b64_key}");
    byte[] iv = Convert.FromBase64String("{b64_iv}");

    using (System.Security.Cryptography.Aes aes = System.Security.Cryptography.Aes.Create())
    {{
        aes.Key = key;
        aes.IV = iv;
        aes.Mode = System.Security.Cryptography.CipherMode.CBC;

        using (System.Security.Cryptography.ICryptoTransform decryptor = aes.CreateDecryptor(aes.Key, aes.IV))
        using (System.IO.MemoryStream ms = new System.IO.MemoryStream(cipherBytes))
        using (System.Security.Cryptography.CryptoStream cs = new System.Security.Cryptography.CryptoStream(ms, decryptor, System.Security.Cryptography.CryptoStreamMode.Read))
        using (System.IO.StreamReader sr = new System.IO.StreamReader(cs))
        {{
            return sr.ReadToEnd();
        }}
    }}
}}
"""
