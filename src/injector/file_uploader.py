import os

class FileUploader:
    def __init__(self, ssh_manager):
        """
        Recebe uma instância já conectada do SSHManager.
        """
        self.ssh = ssh_manager

    def upload_activation_record(self, local_path, remote_dir):
        """Envia o activation_record.plist para o diretório correto."""
        # Caminho onde o iOS espera o registro de ativação no iPhone XS
        remote_path = os.path.join(remote_dir, "activation_record.plist")
        
        print(f"[*] Preparando para enviar registro de ativação...")
        if not os.path.exists(local_path):
            print(f"[-] Arquivo local não encontrado: {local_path}")
            return False

        success = self.ssh.upload_file(local_path, remote_path)
        if success:
            print("[+] Registro de ativação enviado com sucesso.")
            return remote_path
        return False

    def upload_gestalt_patch(self, local_path, remote_dir):
        """Envia o mobilegestalt_patched.plist para o diretório correto."""
        # Caminho onde o MobileGestalt fica armazenado no iOS (A12+)
        remote_path = os.path.join(remote_dir, "mobilegestalt_patched.plist")
        
        print(f"[*] Preparando para enviar patch do MobileGestalt...")
        if not os.path.exists(local_path):
            print(f"[-] Arquivo local não encontrado: {local_path}")
            return False

        success = self.ssh.upload_file(local_path, remote_path)
        if success:
            print("[+] Patch do MobileGestalt enviado com sucesso.")
            return remote_path
        return False
