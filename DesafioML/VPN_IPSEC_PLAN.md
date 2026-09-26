# Plano de Automação: Túnel VPN IPSec Site-to-Site (FortiGate <-> Palo Alto)

## 1. Definição de Parâmetros
* **Dispositivo A:** FortiGate (Matriz) - IP WAN: `200.200.200.1`
* **Dispositivo B:** Palo Alto (Filial) - IP WAN: `150.150.150.1`
* **Redes Locais:** 
  * FortiGate: `10.100.0.0/16`
  * Palo Alto: `10.200.0.0/16`
* **Rede de Túnel:** `169.255.1.0/30`
* **Fase 1 (IKEv2):** AES-256-GCM, SHA-256, DH Group 14, Lifetime: 28800s.
* **Fase 2 (IPSec ESP):** AES-256-GCM, SHA-256, PFS (Group 14), Lifetime: 3600s.