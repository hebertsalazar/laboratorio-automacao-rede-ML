from datetime import datetime
import os
from netmiko import ConnectHandler


class CiscoSwitchManager:

  def __init__(
      self, host, username, password, port=22, device_type="cisco_ios"
  ):
    self.device = {
        "device_type": device_type,
        "host": host,
        "username": username,
        "password": password,
        "port": port,
    }

  def conectar(self):
    return ConnectHandler(**self.device)

  def aplicar_configuracoes_condicionais(self, hostname_desejado, vlans_lista):
    net_connect = self.conectar()
    sh_run_host = net_connect.send_command(
        "show running-config | include hostname"
    )
    hostname_atual = ""
    for linha in sh_run_host.splitlines():
      if linha.startswith("hostname "):
        hostname_atual = linha.split()[1].strip()

    config_commands = []
    if hostname_desejado.lower() != hostname_atual.lower():
      config_commands.append(f"hostname {hostname_desejado}")

    for vlan in vlans_lista:
      config_commands.append(f"vlan {vlan['id']}")
      config_commands.append(f" name {vlan['name']}")

    output = ""
    if config_commands:
      output = net_connect.send_config_set(config_commands)

    net_connect.disconnect()
    return output, hostname_atual

  def salvar_nvram(self):
    net_connect = self.conectar()
    output = net_connect.save_config()
    net_connect.disconnect()
    return output

  def realizar_backup(self, hostname):
    net_connect = self.conectar()
    config_running = net_connect.send_command("show running-config")

    if not os.path.exists("backup"):
      os.makedirs("backup")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"backup/bkp_{hostname}_{timestamp}.cfg"

    with open(filename, "w") as f:
      f.write(config_running)

    net_connect.disconnect()
    return filename

  def validar_estado(self, hostname_esperado, vlan_ids):
    net_connect = self.conectar()
    sh_run_host = net_connect.send_command(
        "show running-config | include hostname"
    )
    sh_vlan = net_connect.send_command("show vlan brief")
    net_connect.disconnect()

    divergencias = []
    if hostname_esperado not in sh_run_host:
      divergencias.append(f"Hostname divergente. Esperado: {hostname_esperado}")

    for vid in vlan_ids:
      if str(vid) not in sh_vlan:
        divergencias.append(f"VLAN {vid} não encontrada no switch.")

    return divergencias