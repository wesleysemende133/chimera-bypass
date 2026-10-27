
```markdown
<div align="center">

# 🔥 Project Chimera

### A12/A13 Activation Lock Bypass Research Toolkit

**Criado e desenvolvido por [Wesley Agnaldo Semende](https://github.com/wesleysemende133)**

</div>

---

> ## ⚠️ AVISO IMPORTANTE
>
> **Esta ferramenta NÃO FOI TESTADA em nenhum dispositivo real.**
>
> O Project Chimera foi construído com base em pesquisas de engenharia reversa e na lógica de exploits públicos (como o `usbliter8`). Se você pretende testá-la, **use um dispositivo que você possui e que não seja o seu principal**.
>
> **Contribua com a comunidade**: envie Issues e Pull Requests com logs de erro e resultados. O avanço do projeto depende da colaboração de todos.

---

## 📑 Sumário

- [Visão Geral](#-visão-geral)
- [Aviso Legal e Limitações](#-aviso-legal-e-limitações)
- [Arquitetura do Projeto](#️-arquitetura-do-projeto)
- [Como Usar](#-como-usar)
  - [Pré-requisitos](#pré-requisitos)
  - [Instalação](#instalação)
  - [Execução](#execução)
- [Diferencial Técnico](#-o-diferencial-técnico-por-que-o-chimera-funciona-no-wi-fi)
- [Como Contribuir](#-como-contribuir)
- [Licença](#-licença)
- [Autor](#-autor)

---

## 📖 Visão Geral

O **Project Chimera** é uma ferramenta de **pesquisa de segurança** e **bypass de Activation Lock** desenvolvida do zero para dispositivos Apple equipados com os chips **A12 (iPhone XS/XR)** e **A13 (iPhone 11 / SE 2)**.

Diferente de abordagens que tentam negociar um handshake falso com o `mobileactivationd` — e falham com `PlistError` —, o Chimera adota uma filosofia de **substituição de identidade em nível de sistema**.

A ferramenta explora a vulnerabilidade de BootROM **`usbliter8`** para obter controle total do dispositivo (**Pwned DFU**) e dar boot em um **Ramdisk SSH**. A partir daí, o Chimera injeta:

- 🆔 Uma identidade de fábrica falsa (`FE00`)
- 📄 Um registro de ativação manipulado
- 🧩 Um patch no `MobileGestalt`

…forçando o iOS a **ignorar a tela de ativação** e inicializar o sistema.

---

## 🚨 Aviso Legal e Limitações

| Categoria | Descrição |
|-----------|-----------|
| **Status de Teste** | Protótipo **não testado em hardware real**. Use por sua conta e risco. |
| **Uso Educacional** | Criado para pesquisa de segurança, aprendizado de engenharia reversa e auditoria de dispositivos próprios. |
| **Sem Sinal Celular** | Devido à arquitetura do **SEP (Secure Enclave)** no A12/A13, a troca de identidade invalida a assinatura da Baseband. O dispositivo funcionará **apenas com Wi-Fi**. Chamadas e dados móveis não funcionarão. |
| **Não é Permanente** | O bypass pode ser perdido caso o dispositivo seja atualizado, restaurado ou tenha a memória NVRAM limpa. |

> ⚖️ **Isenção de responsabilidade:** Este projeto destina-se exclusivamente a fins educacionais e de pesquisa em dispositivos próprios. O autor não se responsabiliza por uso indevido, danos ao dispositivo ou violação de termos de serviço.

---

## 🏗️ Arquitetura do Projeto

O projeto foi desenhado de forma **modular**, separando a interação de hardware (C), a orquestração (Python) e a execução no dispositivo (Shell).

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

O cérebro do projeto. Gerencia o fluxo de **5 fases**, verifica a integridade do ambiente, aciona o gerador de payloads e comanda a injeção via SSH.

- `--mock` → testa a lógica sem hardware
- `--inspect` → visualiza os plists gerados

### 💉 2. Exploit e Hardware (`src/exploit/`)

| Arquivo | Responsabilidade |
|---------|------------------|
| `usb_dfu.c` | Comunicação com o controlador Synopsys DesignWare via `libusb` |
| `usbliter8.c` | Envio do payload que explora a BootROM e permite o boot do Ramdisk |

> **Nota:** Requer um **Raspberry Pi Pico 2 (RP2350)** ou **Linux com acesso USB direto**.

### 📝 3. Geração de Payloads (`src/payloads/`)

- **`fe00_generator.py`** — Cria o `activation_record.plist` falso. Gera um UDID iniciado em `0000FE00` (identidade de teste de fábrica da Apple) e zera os dados da Baseband (`IMEI`, `MEID`).
- **`gestalt_patcher.py`** — Cria o `mobilegestalt_patched.plist`, alterando os offsets de modelo para `iPod7,1` e contornando a verificação de ativação do hardware.

### 📡 4. Injeção (`src/injector/`)

- **`ssh_manager.py`** — Gerencia a conexão com o Ramdisk SSH (IP `10.0.0.1`, usuário `root`, senha `alpine`).
- **`file_uploader.py`** — Envia os plists para os diretórios corretos do iOS (`/mnt1` e `/mnt2`).
- **`sys_cmds.py`** — Executa comandos no dispositivo: `mount_ich`, `chown`/`chmod` e `reboot`.

---

## 🚀 Como Usar

### Pré-requisitos

1. **Python 3.10+** com `venv` configurado
2. **Hardware para o exploit** (Raspberry Pi Pico 2 ou PC Linux)
3. **Ramdisk SSH** compatível com A12/A13

### Instalação

```bash
# Clone o repositório e entre na pasta
git clone https://github.com/<seu-usuario>/chimera-bypass.git
cd chimera-bypass

# Crie o ambiente virtual e ative
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
# venv\Scripts\activate    # Windows

# Instale as dependências
pip install -r requirements.txt

# Compile os módulos C
cd src/exploit && make && cd ../..
```

### Execução

**1️⃣ Testar a lógica (sem dispositivo):**
```bash
python3 src/main.py --mock
```

**2️⃣ Inspecionar os payloads gerados:**
```bash
python3 src/main.py --inspect
```

**3️⃣ Executar o bypass real (requer Ramdisk SSH ativo):**
```bash
python3 src/main.py
```

#### 🔄 Fluxo de execução

1. Aguarda o Ramdisk SSH subir
2. Gera o registro `FE00` e o patch do Gestalt em `output/`
3. Conecta via SSH e monta as partições (`/mnt1` e `/mnt2`)
4. Injeta o registro de ativação e o patch no sistema de arquivos
5. Ajusta as permissões e reinicia o dispositivo

---

## 🤝 Como Contribuir

Este é um projeto **open source** de pesquisa. Se você possui um iPhone XS, XR, 11 ou SE 2 e deseja testar:

1. Faça um **Fork** do repositório
2. Crie uma **Branch** para sua modificação:
   ```bash
   git checkout -b feature/MeuTeste
   ```
3. Faça o **Commit** das suas alterações:
   ```bash
   git commit -m "Adicionando logs de teste no A13"
   ```
4. Faça o **Push** para a branch:
   ```bash
   git push origin feature/MeuTeste
   ```
5. Abra um **Pull Request**

> 🐛 Encontrou um erro? (ex: caminho de arquivo diferente no iOS 17)
> Abra uma **Issue** detalhando o **dispositivo**, a **versão do iOS** e o **log do erro**.
> Juntos podemos tornar o Chimera uma ferramenta funcional.

---

## 🔬 O Diferencial Técnico: Por que o Chimera funciona (no Wi-Fi)?

O projeto abandona a abordagem de **falsos handshakes de rede** — que falham no A12+ — e adota a **substituição de arquivos em disco**.

Como o `usbliter8` nos concede controle total da partição de dados **antes** do iOS inicializar, o sistema lê o arquivo `activation_record.plist` modificado como se fosse legítimo. O patch do `MobileGestalt` atua como uma **segunda camada de segurança**, impedindo que o iOS reverta o estado de ativação com base no hardware real.

---

## 📜 Licença

Distribuído sob a licença **MIT**. Consulte o arquivo [`LICENSE`](LICENSE) para mais informações.

---

## 👤 Autor

<div align="center">

**Wesley Agnaldo Semende**

[![GitHub](https://img.shields.io/badge/GitHub-@wesley-181717?style=for-the-badge&logo=github)](https://github.com/wesleysemende133)
[![Email](https://img.shields.io/badge/Email-contato-red?style=for-the-badge&logo=gmail)](mailto:weseleysemende@gmail.com)

</div>

---

<div align="center">

**⭐ Se este projeto foi útil para você, considere dar uma estrela no repositório!**

*Feito com 🔥 e engenharia reversa por Wesley Agnaldo Semende*

</div>
```
