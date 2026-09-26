# Laboratório de Automação de Redes e Infraestrutura (Cisco & VPNs Multi-Vendor)

## 📋 Descrição Geral do Projeto
Este projeto foi desenvolvido para atender ao **Desafio de Automação de Infraestrutura de Redes**, compreendendo duas frentes principais:
1. **Parte 1 (Automação de Switch Cisco):** Um script em Python gerenciado via Git que utiliza uma interface gráfica modular (**Tkinter**) e a biblioteca de automação de rede **Netmiko** para interagir com switches Cisco IOS. O sistema permite validar permissões administrativas, pré-visualizar comandos CLI em tempo real, aplicar configurações condicionais de hostname e VLANs customizadas, salvar na NVRAM, gerar backups locais com carimbo de data/hora e realizar validações automáticas de estado contra divergências.
2. **Parte 2 (Planejamento de VPN IPSec):** A documentação técnica detalhada (`VPN_IPSEC_PLAN.md`) do projeto de arquitetura e automação de um túnel VPN IPSec site-to-site entre dispositivos de fabricantes distintos (**FortiGate** e **Palo Alto**), incluindo parâmetros criptográficos, análise de APIs REST e estratégias de validação contínua.

---

## 🛠️ Tecnologias Utilizadas
* **Python 3.10+**
* **Netmiko** (Comunicação SSH com dispositivos de rede)
* **Tkinter & ScrolledText** (Interface Gráfica e Logs Modulares)
* **Git** (Controle de versões)
* **GitHub Actions** (Automação de pipelines CI/CD)

---

## ⚙️ Pré-requisitos e Instalação de Dependências

Certifique-se de ter o **Python** instalado em sua máquina com a opção *"Add python.exe to PATH"* marcada.

1. Clone o repositório em sua máquina local:
   ```bash
   git clone [https://github.com/hebertsalazar/laboratorio-automacao-rede-ML.git](https://github.com/hebertsalazar/laboratorio-automacao-rede-ML.git)
   cd laboratorio-automacao-rede-ML

   Instale as dependências necessárias descritas no arquivo requirements.txt:

Bash
pip install -r requirements.txt
🖥️ Como Interagir com o Frontend (app.py)
O painel gráfico modular foi estruturado em três etapas lógicas para garantir total controle e segurança operacional antes de enviar qualquer alteração ao equipamento de rede:

Seção 1 - Conexão e Credenciais:

IP do Switch: Insira o endereço IP gerencial do switch Cisco (simulado via GNS3/EVE-NG ou real).

Usuário / Senha: Insira suas credenciais administrativas. O campo de usuário inicia em branco por segurança.

Validação de Privilégio: Clique no botão azul "Validar Privilégio (Level 15)" para testar se a conta possui permissão máxima antes de prosseguir.

Seção 2 - Parâmetros de Configuração e CLI Preview:

Hostname: Insira o nome desejado. O sistema conta com lógica condicional: o comando de alteração de hostname só será enviado se o nome digitado for diferente do nome atual detectado no switch.

VLANs Customizadas: Especifique dinamicamente os IDs e os Nomes para pelo menos as VLANs exigidas:

VLAN 10 - VLAN_DADOS

VLAN 20 - VLAN_VOZ

VLAN 50 - VLAN_SEGURANÇA

CLI Preview: A caixa verde exibe em tempo real a pré-visualização exata dos comandos de configuração que serão disparados.

Seção 3 - Execução Modular por Etapas:
Cada botão possui um botão dedicado e uma caixa de log isolada:

A. Aplicar Configurações: Envia os comandos via SSH de forma condicional.

B. Salvar (NVRAM): Executa o comando de gravação definitiva (write memory).

C. Realizar Backup: Gera um arquivo de backup local com o hostname e timestamp no diretório backup/.

D. Validar Estado: Realiza o health check comparando a infraestrutura atual com os parâmetros esperados, disparando alertas visuais em caso de divergências.

📂 Estrutura de Diretórios do Projeto
Plaintext
laboratorio-automacao-rede/

├── .github/

│   └── workflows/

│       └── network-automation.yml   # Pipeline CI/CD para GitHub Actions

├── utils/

│   ├── __init__.py

│   └── cisco_handler.py             # Módulo de backend Netmiko

├── backup/                          # Diretório de arquivos de configuração salvos

├── app.py                           # Interface Gráfica Modular (Tkinter)

├── orchestrator.py                  # Script de orquestração multi-vendor

├── VPN_IPSEC_PLAN.md                # Planejamento detalhado da VPN IPSec

├── requirements.txt                 # Dependências do projeto

└── README.md                        # Documentação técnica

📝 Notas de Implementação
Proteção contra Campos Vazios: O sistema valida preventivamente se há campos em branco na interface antes de abrir túneis SSH, evitando corrupção ou apagamento acidental de parâmetros no switch.

Pipeline de CI/CD: O arquivo de workflow do GitHub Actions foi estruturado para suportar Self-Hosted Runners, permitindo a execução de testes automatizados diretamente em redes privadas de laboratório.
