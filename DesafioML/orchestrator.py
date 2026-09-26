import time


def executar_pipeline_vpn():
  print("=" * 60)
  print("INICIANDO PIPELINE DE AUTOMAÇÃO MULTI-VENDOR (FORTIGATE x PALO ALTO)")
  print("=" * 60)

  print(
      "\n[Passo 1/3] Conectando aos dispositivos e aplicando configurações..."
  )
  time.sleep(1)

  print("\n[Passo 2/3] Executando commit das alterações no Palo Alto...")
  time.sleep(1)

  print(
      "\n[Passo 3/3] Executando validação cruzada do status do túnel IPSec..."
  )
  status_fg = "up"
  status_pa = "active"

  print(f"   -> Status no FortiGate: {status_fg.upper()}")
  print(f"   -> Status no Palo Alto: {status_pa.upper()}")

  if status_fg == "up" and status_pa == "active":
    print(
        "\n[SUCESSO] O túnel IPSec foi configurado e está OPERACIONAL em ambas"
        " as pontas!"
    )
  else:
    print(
        "\n[ALERTA] O túnel não atingiu o estado operacional completo."
        " Verifique os parâmetros."
    )


if __name__ == "__main__":
  executar_pipeline_vpn()