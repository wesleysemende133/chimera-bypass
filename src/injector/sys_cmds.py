class SysCmds:
    def __init__(self, ssh_manager):
        """
        Recebe uma instância já conectada do SSHManager.
        """
        self.ssh = ssh_manager

    def mount_partitions(self):
        """Executa o mount_ich para montar as partições /mnt1 e /mnt2."""
        print("[*] Montando partições do iOS (/mnt1, /mnt2)...")
        # O comando mount_ich é nativo do ramdisk usado em A12
        self.ssh.execute_command("mount_ich")
        # Verifica se a montagem funcionou (checa se a pasta /mnt1 existe)
        self.ssh.execute_command("ls /mnt1 > /dev/null 2>&1 && echo 'MNT_OK' || echo 'MNT_FAIL'")

    def set_permissions(self, file_path):
        """Ajusta as permissões para que o iOS aceite o arquivo como legítimo."""
        print(f"[*] Ajustando permissões de: {file_path}")
        self.ssh.execute_command(f"chown mobile:mobile {file_path}")
        self.ssh.execute_command(f"chmod 644 {file_path}")

    def reboot_device(self):
        """Reinicia o dispositivo para aplicar as mudanças."""
        print("[*] Enviando comando de reboot...")
        self.ssh.execute_command("reboot")
