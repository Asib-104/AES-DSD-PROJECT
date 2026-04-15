from Crypto.Cipher import AES

def aes128_encrypt_from_64hex(input_hex: str) -> str:
    # Remove spaces/newlines and normalize
    input_hex = input_hex.strip().replace(" ", "").lower()

    if len(input_hex) != 64:
        raise ValueError("Input must be exactly 64 hex characters (32 for key + 32 for plaintext).")

    # Split
    key_hex = input_hex[:32]
    pt_hex = input_hex[32:]

    # Convert hex → bytes
    key = bytes.fromhex(key_hex)
    plaintext = bytes.fromhex(pt_hex)

    if len(key) != 16 or len(plaintext) != 16:
        raise ValueError("Key and plaintext must each be 16 bytes (AES-128 block size).")

    # AES-128 ECB (no padding)
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(plaintext)

    return ciphertext.hex()


if __name__ == "__main__":
    user_input = input("Enter 64 hex chars (32 key + 32 plaintext):\n")
    try:
        ct = aes128_encrypt_from_64hex(user_input)
        print("Ciphertext:", ct)
    except Exception as e:
        print("Error:", e)
