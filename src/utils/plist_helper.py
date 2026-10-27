import plistlib
import os

def read_plist(filepath):
    """Lê um arquivo plist e retorna um dicionário Python."""
    if not os.path.exists(filepath):
        print(f"[-] Arquivo não encontrado: {filepath}")
        return None
    
    try:
        with open(filepath, 'rb') as f:
            # Tenta ler como binário, se falhar tenta como XML
            try:
                return plistlib.load(f)
            except Exception:
                f.seek(0)
                return plistlib.load(f, fmt=plistlib.FMT_XML)
    except Exception as e:
        print(f"[-] Erro ao ler plist {filepath}: {e}")
        return None

def write_plist(filepath, data, binary=True):
    """Salva um dicionário em um arquivo plist."""
    try:
        fmt = plistlib.FMT_BINARY if binary else plistlib.FMT_XML
        with open(filepath, 'wb') as f:
            plistlib.dump(data, f, fmt=fmt)
        print(f"[+] Plist salvo: {filepath}")
        return True
    except Exception as e:
        print(f"[-] Erro ao salvar plist {filepath}: {e}")
        return False

def dump_plist_to_screen(filepath):
    """Imprime o conteúdo de um plist no terminal para debug."""
    data = read_plist(filepath)
    if data:
        print(f"\n--- Conteúdo de {filepath} ---")
        for key, value in data.items():
            print(f"  {key}: {value}")
        print("-------------------------------\n")
