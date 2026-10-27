import os

def check_requirements():
    """Verifica se as dependências e arquivos essenciais estão presentes."""
    print("[*] Verificando pré-requisitos do ambiente...")
    errors = []

    # 1. Verificar pastas essenciais
    if not os.path.exists("output"):
        try:
            os.makedirs("output")
            print("  [+] Pasta 'output/' criada.")
        except Exception as e:
            errors.append(f"Não foi possível criar a pasta output: {e}")

    # 2. Verificar se o binário C do exploit foi compilado
    exploit_bin = "bin/chimera_exploit"
    if not os.path.exists(exploit_bin):
        print(f"  [!] Aviso: Binário '{exploit_bin}' não encontrado.")
        print("      Rode 'make' na pasta src/exploit/ para compilá-lo.")
    
    # 3. Verificar se as bibliotecas Python estão instaladas
    try:
        import paramiko
        print("  [+] Paramiko instalado.")
    except ImportError:
        errors.append("Biblioteca 'paramiko' não instalada. Rode: pip install paramiko")

    try:
        import usb.core
        print("  [+] PyUSB instalado.")
    except ImportError:
        errors.append("Biblioteca 'pyusb' não instalada. Rode: pip install pyusb")

    # Retorna True se não houver erros graves
    if errors:
        print("\n[!] Erros encontrados durante a verificação:")
        for err in errors:
            print(f"    - {err}")
        return False
    
    print("[+] Verificação concluída com sucesso!\n")
    return True

def check_device_connection():
    """Verifica se o dispositivo está respondendo no IP do Ramdisk SSH."""
    import socket
    
    host = "10.0.0.1"
    port = 22
    
    print(f"[*] Testando conexão com o dispositivo ({host}:{port})...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3) # 3 segundos de timeout
    
    result = sock.connect_ex((host, port))
    sock.close()
    
    if result == 0:
        print("[+] Dispositivo online e aceitando conexões SSH!")
        return True
    else:
        print("[-] Dispositivo não encontrado (Ramdisk SSH inativo).")
        return False
