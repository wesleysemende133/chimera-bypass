import plistlib
import os

def patch_gestalt_cachedata(input_path=None, output_dir="output"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_path = os.path.join(output_dir, "mobilegestalt_patched.plist")

    fake_gestalt = {
        "ArtworkDeviceProductDescription": "iPod",
        "ProductType": "iPod7,1",
        "DeviceClass": "iPod",
        "HWModel": "iPod7,1",
        "_CacheData": b"PATCHED_CHIMERA_DATA" 
    }

    try:
        with open(output_path, "wb") as f:
            plistlib.dump(fake_gestalt, f, fmt=plistlib.FMT_BINARY)
        print(f"[+] Patch do MobileGestalt preparado: {output_path}")
        return output_path
    except Exception as e:
        print(f"[-] Erro ao gerar patch do Gestalt: {e}")
        return None
