import paramiko
import time

class SSHManager:
    def __init__(self, host="10.0.0.1", port=22, user="root", password="alpine"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        print(f"[*] Tentando conectar ao iPhone XS via SSH em {self.host}:{self.port}...")
        try:
            self.client.connect(
                self.host, 
                port=self.port, 
                username=self.user, 
                password=self.password, 
                timeout=10,
                banner_timeout=10
            )
            print("[+] Conexão SSH estabelecida com sucesso!")
            return True
        except Exception as e:
            print(f"[-] Erro ao conectar SSH: {e}")
            return False

    def execute_command(self, command):
        print(f"[*] Executando no device: {command}")
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            stdout.channel.recv_exit_status() # Espera terminar
            out = stdout.read().decode().strip()
            err = stderr.read().decode().strip()
            if out:
                print(f"    -> {out}")
            if err:
                print(f"    -> [STDERR]: {err}")
        except Exception as e:
            print(f"[-] Falha ao executar comando: {e}")

    def upload_file(self, local_path, remote_path):
        print(f"[*] Enviando {local_path} para {remote_path}...")
        try:
            sftp = self.client.open_sftp()
            sftp.put(local_path, remote_path)
            sftp.close()
            print("    -> Upload concluído.")
            return True
        except Exception as e:
            print(f"[-] Erro no upload: {e}")
            return False

    def disconnect(self):
        self.client.close()
        print("[+] Conexão SSH encerrada.")
