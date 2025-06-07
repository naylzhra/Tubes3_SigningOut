import base64

class Encryptor:
    def __init__(self, key: str):
        self.key = key

    def _shift_char(self, c, k, encrypt=True):
        base = ord(' ')
        range_size = 95  # printable ASCII from ' ' (32) to '~' (126)

        c_idx = ord(c) - base
        k_idx = ord(k) - base
        shift = (c_idx + k_idx) % range_size if encrypt else (c_idx - k_idx) % range_size
        return chr(base + shift)

    def _apply_cipher(self, text: str, encrypt=True) -> str:
        text = text or ""
        result = []
        for i, c in enumerate(text):
            if 32 <= ord(c) <= 126:
                k = self.key[i % len(self.key)]
                result.append(self._shift_char(c, k, encrypt))
            else:
                result.append(c)
        return ''.join(result)

    def encrypt(self, plaintext: str) -> str:
        cipher = self._apply_cipher(plaintext, encrypt=True)
        return base64.urlsafe_b64encode(cipher.encode()).decode()

    def decrypt(self, ciphertext: str) -> str:
        try:
            decoded = base64.urlsafe_b64decode(ciphertext.encode()).decode()
            return self._apply_cipher(decoded, encrypt=False)
        except Exception:
            return "[DECRYPTION FAILED]"
