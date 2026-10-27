#!/usr/bin/env python3
import sys
import os
import argparse
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.payloads.fe00_generator import generate_fe00_record
from src.payloads.gestalt_patcher import patch_gestalt_cachedata
from src.injector.ssh_manager import SSHManager
from src.injector.file_uploader import FileUploader
from src.injector.sys_cmds import SysCmds
from src.utils.logger import setup_logger
from src.utils.checks import check_requirements, check_device_connection
from src.utils.plist_helper import dump_plist_to_screen

def main():
    parser = argparse.ArgumentParser(description="Project Chimera - A12 Bypass")
    parser.add_argument("--mock", action="store_true", help="Simula a injeção")
    parser.add_argument("--inspect", action="store_true", help="Apenas gera e inspeciona os plists")
    args = parser.parse_args()

    logger = setup_logger()
    
    print("\n" + "="*50)
    print("  🔥 PROJECT CHIMERA - A12/A13 HELLO SCREEN BYPASS 🔥")
    print("="*50 + "\n")

    # 0. VERIFICAÇÃO DE AMBIENTE
    if not check_requirements():
        logger.error("Ambiente não está pronto. Abortando.")
        sys.exit(1)

    # 1. EXPLOIT
    logger.info("[Fase 1] Preparando dispositivo...")
    if not args.mock:
        logger.warning(">>> AÇÃO DO USUÁRIO NECESSÁRIA <<<")
        print("1. Coloque o iPhone XS em modo DFU.")
        print("2. Execute o exploit usbliter8 para dar boot no ramdisk SSH.")
        input("\n[?] Pressione ENTER quando o Ramdisk SSH estiver ativo...")
    else:
        logger.info("[MOCK] Pulando espera do dispositivo (modo de teste).")

    # 2. GERAR PAYLOADS
    logger.info("[Fase 2] Gerando identidade falsa (FE00) e patch do Gestalt...")
    try:
        record_path = generate_fe00_record()
        gestalt_path = patch_gestalt_cachedata()
        
        if args.inspect:
            dump_plist_to_screen(record_path)
            dump_plist_to_screen(gestalt_path)
            logger.info("Inspeção concluída. Saindo.")
            sys.exit(0)
            
    except Exception as e:
        logger.error(f"Falha ao gerar payloads: {e}")
        sys.exit(1)

    # 3. INJEÇÃO
    logger.info("[Fase 3] Conectando ao dispositivo para injeção...")
    
    if args.mock:
        logger.info("[MOCK] Simulando injeção...")
        time.sleep(2)
        logger.info("[MOCK] Executando mount_ich...")
        time.sleep(1)
        logger.info(f"[MOCK] Enviando {record_path} para /mnt1/...")
        logger.info(f"[MOCK] Enviando {gestalt_path} para /mnt2/...")
        time.sleep(1)
        logger.info("[MOCK] Ajustando permissões...")
        logger.info("[MOCK] Reiniciando dispositivo...")
        print("\n✅ [MOCK] Fluxo completo simulado com sucesso!")
        sys.exit(0)

    # Verifica se o device está realmente online
    if not check_device_connection():
        logger.error("O iPhone XS não está respondendo no IP 10.0.0.1.")
        sys.exit(1)

    ssh = SSHManager(host="10.0.0.1", port=22, user="root", password="alpine")
    if not ssh.connect():
        logger.error("Falha na autenticação SSH.")
        sys.exit(1)

    logger.info("[Fase 4] Montando partições e injetando arquivos...")
    
    # Instancia os módulos de injeção
    sys_cmds = SysCmds(ssh)
    uploader = FileUploader(ssh)

    # Monta as partições
    sys_cmds.mount_partitions()
    time.sleep(2)

    # Define os diretórios remotos (baseados no iOS 16/17 para o iPhone XS)
    remote_record_dir = "/mnt1/private/var/root/Library/Lockdown/"
    remote_gestalt_dir = "/mnt2/private/var/containers/Shared/SystemGroup/systemgroup.com.apple.mobilegestalt.plist/"

    # Faz o upload dos arquivos
    uploaded_record = uploader.upload_activation_record(record_path, remote_record_dir)
    uploaded_gestalt = uploader.upload_gestalt_patch(gestalt_path, remote_gestalt_dir)

    if uploaded_record and uploaded_gestalt:
        # Ajusta permissões
        sys_cmds.set_permissions(uploaded_record)
        sys_cmds.set_permissions(uploaded_gestalt)
        
        # Reinicia
        logger.info("[Fase 5] Reiniciando dispositivo...")
        sys_cmds.reboot_device()
    else:
        logger.error("Falha no upload dos arquivos. Abortando reinicialização.")

    ssh.disconnect()
    logger.info("=== Processo Finalizado ===")

if __name__ == "__main__":
    main()
