import plistlib
import os
import uuid
import random
import string

def generate_fake_serial():
    prefix = "F17XQ0P"
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"{prefix}{suffix}"

def generate_fe00_record(output_dir="output"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    fake_udid = f"0000FE00-{uuid.uuid4().hex[:16].upper()}"
    fake_serial = generate_fake_serial()

    activation_record = {
        "AccountToken": b"",
        "ActivationRandomness": str(uuid.uuid4()).upper(),
        "ActivationState": "Unactivated",
        "UniqueDeviceID": fake_udid,
        "SerialNumber": fake_serial,
        "ProductType": "iPhone11,2",
        "ProductVersion": "16.7.5",
        "BuildVersion": "20H240",
        "HardwareModel": "N841AP",
        "IMEI": "000000000000000",
        "MEID": "00000000000000",
        "BasebandActivationTicketVersion": "V2",
        "BasebandStatus": "NoBaseband",
        "FairPlayKeyData": b"",
        "RKCData": b"",
        "SepNonce": b"",
        "UseFDR": False,
        "SessionMode": True,
        "ActivationStateAcknowledged": True
    }

    output_path = os.path.join(output_dir, "activation_record.plist")
    with open(output_path, "wb") as f:
        plistlib.dump(activation_record, f, fmt=plistlib.FMT_BINARY)
        
    print(f"[+] Registro FE00 gerado com sucesso: {output_path}")
    print(f"    -> UDID Falso: {fake_udid}")
    print(f"    -> Serial Falso: {fake_serial}")
    return output_path

if __name__ == "__main__":
    generate_fe00_record()
