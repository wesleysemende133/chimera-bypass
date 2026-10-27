
```markdown
# 🔥 Project Chimera - A12/A13 Hello Screen Bypass

> **Criado e desenvolvido por Wesley Agnaldo Semende.**
> 
> ⚠️ **AVISO IMPORTANTE:** Esta ferramenta ainda **NÃO FOI TESTADA em nenhum celular real**. Ela foi construída com base em pesquisas de engenharia reversa e na lógica de exploits públicos (como o `usbliter8`). 
> 
> **Pedimos encarecidamente** que, se você for testar, use um dispositivo que você possui e que não seja o seu principal. **Faça testes em telemóveis reais e contribua com o código** enviando Issues e Pull Requests com os logs de erro e resultados. A comunidade só avança com a colaboração de todos.

## 📖 Visão Geral
O **Project Chimera** é uma ferramenta de pesquisa de segurança e bypass de ativação (Activation Lock) desenvolvida do zero para dispositivos Apple equipados com chips **A12 (iPhone XS/XR) e A13 (iPhone 11/SE 2)**.

Diferente de abordagens que tentam negociar um handshake falso com o `mobileactivationd` (e falham com `PlistError`), o Chimera adota uma filosofia de **substituição de identidade em nível de sistema**. 

A ferramenta explora a vulnerabilidade de BootROM **`usbliter8`** para obter controle total do dispositivo (Pwned DFU) e dar boot em um Ramdisk SSH. A partir daí, o Chimera injeta uma identidade de fábrica falsa (`FE00`), um registro de ativação manipulado e um patch no `MobileGestalt`, forçando o iOS a ignorar a tela de ativação e inicializar o sistema.

## 🚨 Aviso Legal e Limitações
* **Status de Teste:** Protótipo não testado em hardware real. Use por sua conta e risco.
* **Uso Educacional:** Esta ferramenta foi criada para fins de pesquisa de segurança, aprendizado de engenharia reversa e auditoria de dispositivos próprios.
* **Sem Sinal Celular (Wi-Fi Only):** Devido à arquitetura de segurança do SEP (Secure Enclave) no A12/A13, a troca de identidade invalida a assinatura da Baseband. O dispositivo funcionará **apenas com Wi-Fi**. Chamadas e dados móveis não funcionarão.
* **Não é Permanente:** O bypass pode ser perdido caso o dispositivo seja atualizado, restaurado ou tenha a memória NVRAM limpa.

---

## 🏗️ Arquitetura do Projeto

O projeto foi desenhado para ser modular, separando a interação de hardware (C), a orquestração (Python) e a execução no dispositivo (Shell).

```text
chimera-bypass/
├── bin/                  # Binários compilados do exploit e ramdisk
├── src/
│   ├── main.py           # Maestro (Orquestrador principal)
│   ├── exploit/          # Módulos em C (Comunicação USB e usbliter8)
│   ├── payloads/         # Geradores de identidade FE00 e patch do Gestalt
│   ├── injector/         # Módulos de conexão SSH e injeção de arquivos
│   └── utils/            # Logs, verificações de ambiente e helpers
└── output/               # Arquivos plist gerados (identidade e patch)
```

### 🧠 1. Orquestração (`src/main.py`)
O cérebro do projeto. Ele gerencia o fluxo de 5 fases, verifica a integridade do ambiente, aciona o gerador de payloads e comanda a injeção via SSH. Possui um modo `--mock` para testes de lógica sem hardware, e `--inspect` para visualizar os plists gerados.

### 💉 2. Exploit e Hardware (`src/exploit/`)
* **`usb_dfu.c` & `usbliter8.c`:** Responsáveis por se comunicar com o controlador Synopsys DesignWare via `libusb`. Eles enviam o payload malicioso que explora a BootROM, permitindo o boot do Ramdisk.
* *Nota: Requer um Raspberry Pi Pico 2 (RP2350) ou Linux com acesso USB direto.*

### 📝 3. Geração de Payloads (`src/payloads/`)
* **`fe00_generator.py`:** Cria o `activation_record.plist` falso. Ele gera um UDID começando com `0000FE00` (identidade de teste de fábrica da Apple) e zera os dados da Baseband (`IMEI`, `MEID`).
* **`gestalt_patcher.py`:** Cria o `mobilegestalt_patched.plist`. Este arquivo altera os offsets de modelo para `iPod7,1`, enganando o sistema e contornando a verificação de ativação do hardware.

### 📡 4. Injeção (`src/injector/`)
* **`ssh_manager.py`:** Gerencia a conexão com o Ramdisk SSH (geralmente no IP `10.0.0.1` com usuário `root` e senha `alpine`).
* **`file_uploader.py`:** Envia os plists gerados para os diretórios corretos do iOS (`/mnt1` e `/mnt2`).
* **`sys_cmds.py`:** Executa comandos no dispositivo, como `mount_ich` (para montar as partições do iOS), `chown`/`chmod` (para ajustar permissões) e `reboot`.

---

## 🚀 Como Usar

### Pré-requisitos
1. Python 3.10+ e `venv` configurado.
2. Hardware para o exploit (Raspberry Pi Pico 2 ou PC Linux).
3. Ramdisk SSH compatível com A12/A13.

### Instalação
```bash
# Clone o repositório e entre na pasta
cd chimera-bypass

# Crie o ambiente virtual e ative
python3 -m venv venv
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Compile os módulos C
cd src/exploit && make && cd ../..
```

### Execução

**1. Testar a Lógica (Sem dispositivo):**
```bash
python3 src/main.py --mock
```

**2. Inspecionar os Payloads Gerados:**
```bash
python3 src/main.py --inspect
```

**3. Executar o Bypass Real (Requer Ramdisk SSH ativo):**
```bash
python3 src/main.py
```

O fluxo executará as seguintes etapas:
1. Aguardará o Ramdisk SSH subir.
2. Gerará o registro FE00 e o patch do Gestalt na pasta `output/`.
3. Conectará via SSH e montará as partições (`/mnt1` e `/mnt2`).
4. Injetará o registro de ativação e o patch no sistema de arquivos.
5. Ajustará as permissões e reiniciará o dispositivo.

---

## 🤝 Como Contribuir

Este é um projeto de código aberto e pesquisa. Se você tem um iPhone XS, XR, 11 ou SE 2 e deseja testar:

1. Faça um Fork do repositório.
2. Crie uma Branch para a sua modificação (`git checkout -b feature/MeuTeste`).
3. Faça o Commit das suas alterações (`git commit -m 'Adicionando logs de teste no A13'`).
4. Faça o Push para a Branch (`git push origin feature/MeuTeste`).
5. Abra um Pull Request.

Se você encontrou um erro (ex: caminho de arquivo diferente no iOS 17), por favor, abra uma **Issue** detalhando o dispositivo, a versão do iOS e o log do erro. Juntos podemos tornar o Chimera uma ferramenta funcional.

---

## 🔬 O Diferencial Técnico: Por que o Chimera funciona (no Wi-Fi)?

O projeto abandona a abordagem de "falsos handshakes" de rede (que falham no A12+) e adota a **substituição de arquivos em disco**. Como o `usbliter8` nos concede controle total da partição de dados antes do iOS inicializar, o sistema lê o arquivo `activation_record.plist` modificado como se fosse legítimo. O patch do `MobileGestalt` atua como uma segunda camada de segurança, impedindo que o iOS reverta o estado de ativação com base no hardware real.

---
**Autor:** Wesley Agnaldo Semende
**Licença:** MIT (ou a licença de sua preferência)
```
# chimera-bypass
