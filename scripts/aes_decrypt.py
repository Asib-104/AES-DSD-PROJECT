from Crypto.Cipher import AES

def aes128_decrypt_from_64hex(input_hex: str) -> str:
    # Remove spaces/newlines and normalize
    input_hex = input_hex.strip().replace(" ", "").lower()

    if len(input_hex) != 64:
        raise ValueError("Input must be exactly 64 hex characters (32 for key + 32 for ciphertext).")

    # Split
    key_hex = input_hex[:32]
    ct_hex = input_hex[32:]

    # Convert hex → bytes
    key = bytes.fromhex(key_hex)
    ciphertext = bytes.fromhex(ct_hex)

    if len(key) != 16 or len(ciphertext) != 16:
        raise ValueError("Key and ciphertext must each be 16 bytes (AES-128 block size).")

    # AES-128 ECB (no padding)
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.decrypt(ciphertext)

    return plaintext.hex()


if __name__ == "__main__":
    user_input = input("Enter 64 hex chars (32 key + 32 ciphertext):\n")
    try:
        pt = aes128_decrypt_from_64hex(user_input)
        print("Plaintext:", pt)
    except Exception as e:
        print("Error:", e)
