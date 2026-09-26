import tkinter as tk
from tkinter import messagebox, scrolledtext
from utils.cisco_handler import CiscoSwitchManager


class AppAutomacaoModular:

  def __init__(self, root):
    self.root = root
    self.root.title(
        "Gerenciador de Automação Cisco - Painel Modular com CLI Preview"
    )
    self.root.geometry("750x1020")

    # ================= CAMPOS DE CONEXÃO =================
    frame_conn = tk.LabelFrame(
        root, text=" 1. Conexão e Credenciais ", font=("Arial", 9, "bold")
    )
    frame_conn.pack(fill="x", padx=15, pady=5)

    tk.Label(frame_conn, text="IP do Switch:").grid(
        row=0, column=0, sticky="w", padx=5, pady=2
    )
    self.entry_ip = tk.Entry(frame_conn, width=25)
    self.entry_ip.grid(row=0, column=1, padx=5, pady=2)
    self.entry_ip.insert(0, "192.168.1.10")

    tk.Label(frame_conn, text="Usuário:").grid(
        row=0, column=2, sticky="w", padx=5, pady=2
    )
    self.entry_user = tk.Entry(frame_conn, width=15)
    self.entry_user.grid(row=0, column=3, padx=5, pady=2)
    self.entry_user.insert(0, "")

    tk.Label(frame_conn, text="Senha:").grid(
        row=1, column=0, sticky="w", padx=5, pady=2
    )
    self.entry_pass = tk.Entry(frame_conn, width=25, show="*")
    self.entry_pass.grid(row=1, column=1, padx=5, pady=2)

    self.btn_validar_cred = tk.Button(
        frame_conn,
        text="Validar Privilégio (Level 15)",
        bg="#0056b3",
        fg="white",
        command=self.validar_permissao_usuario,
    )
    self.btn_validar_cred.grid(
        row=1, column=2, columnspan=2, padx=5, pady=2, sticky="ew"
    )

    # ================= CONFIGURAÇÃO E VLANs =================
    frame_conf = tk.LabelFrame(
        root, text=" 2. Parâmetros de Configuração ", font=("Arial", 9, "bold")
    )
    frame_conf.pack(fill="x", padx=15, pady=5)

    tk.Label(frame_conf, text="Hostname Desejado:").grid(
        row=0, column=0, sticky="w", padx=5, pady=2
    )
    self.entry_host = tk.Entry(frame_conf, width=30)
    self.entry_host.grid(row=0, column=1, columnspan=3, sticky="w", padx=5, pady=2)
    self.entry_host.insert(0, "SWITCH_AUTOMATIZADO")
    self.entry_host.bind("<KeyRelease>", lambda e: self.atualizar_preview())

    # VLANs inputs
    tk.Label(
        frame_conf, text="VLANs (ID / Nome):", font=("Arial", 8, "bold")
    ).grid(row=1, column=0, sticky="w", padx=5, pady=2)

    self.entry_v10_id = tk.Entry(frame_conf, width=5)
    self.entry_v10_id.grid(row=2, column=0, padx=5, sticky="w")
    self.entry_v10_id.insert(0, "10")
    self.entry_v10_id.bind("<KeyRelease>", lambda e: self.atualizar_preview())
    self.entry_v10_name = tk.Entry(frame_conf, width=20)
    self.entry_v10_name.grid(row=2, column=1, padx=5, sticky="w")
    self.entry_v10_name.insert(0, "VLAN_DADOS")
    self.entry_v10_name.bind("<KeyRelease>", lambda e: self.atualizar_preview())

    self.entry_v20_id = tk.Entry(frame_conf, width=5)
    self.entry_v20_id.grid(row=3, column=0, padx=5, sticky="w")
    self.entry_v20_id.insert(0, "20")
    self.entry_v20_id.bind("<KeyRelease>", lambda e: self.atualizar_preview())
    self.entry_v20_name = tk.Entry(frame_conf, width=20)
    self.entry_v20_name.grid(row=3, column=1, padx=5, sticky="w")
    self.entry_v20_name.insert(0, "VLAN_VOZ")
    self.entry_v20_name.bind("<KeyRelease>", lambda e: self.atualizar_preview())

    self.entry_v50_id = tk.Entry(frame_conf, width=5)
    self.entry_v50_id.grid(row=4, column=0, padx=5, sticky="w")
    self.entry_v50_id.insert(0, "50")
    self.entry_v50_id.bind("<KeyRelease>", lambda e: self.atualizar_preview())
    self.entry_v50_name = tk.Entry(frame_conf, width=20)
    self.entry_v50_name.grid(row=4, column=1, padx=5, sticky="w")
    self.entry_v50_name.insert(0, "VLAN_SEGURANÇA")
    self.entry_v50_name.bind("<KeyRelease>", lambda e: self.atualizar_preview())

    # --- Caixa de Pré-visualização CLI ---
    tk.Label(
        frame_conf,
        text="Pré-visualização dos Comandos (CLI Preview):",
        font=("Arial", 8, "bold"),
        fg="darkgreen",
    ).grid(row=5, column=0, columnspan=3, sticky="w", padx=5, pady=(5, 2))
    self.txt_preview = scrolledtext.ScrolledText(
        frame_conf, height=4, width=70, bg="#f4f4f4"
    )
    self.txt_preview.grid(
        row=6, column=0, columnspan=4, padx=5, pady=2, sticky="ew"
    )

    # ================= PAINEL DE BOTÕES E LOGS ISOLADOS =================
    frame_etapas = tk.LabelFrame(
        root, text=" 3. Execução Modular por Etapas ", font=("Arial", 9, "bold")
    )
    frame_etapas.pack(fill="both", expand=True, padx=15, pady=5)

    # Etapa A: Aplicar Configurações
    self.btn_aplicar = tk.Button(
        frame_etapas,
        text="A. Aplicar Configurações",
        bg="#28a745",
        fg="white",
        font=("Arial", 8, "bold"),
        command=self.executar_aplicacao,
    )
    self.btn_aplicar.grid(row=0, column=0, padx=5, pady=2, sticky="ew")
    self.txt_log_aplicar = scrolledtext.ScrolledText(
        frame_etapas, height=3, width=45
    )
    self.txt_log_aplicar.grid(row=0, column=1, padx=5, pady=2)

    # Etapa B: Salvar na NVRAM
    self.btn_salvar = tk.Button(
        frame_etapas,
        text="B. Salvar (NVRAM)",
        bg="#17a2b8",
        fg="white",
        font=("Arial", 8, "bold"),
        command=self.executar_salvar,
    )
    self.btn_salvar.grid(row=1, column=0, padx=5, pady=2, sticky="ew")
    self.txt_log_salvar = scrolledtext.ScrolledText(
        frame_etapas, height=3, width=45
    )
    self.txt_log_salvar.grid(row=1, column=1, padx=5, pady=2)

    # Etapa C: Backup de Configuração
    self.btn_backup = tk.Button(
        frame_etapas,
        text="C. Realizar Backup",
        bg="#ffc107",
        fg="black",
        font=("Arial", 8, "bold"),
        command=self.executar_backup,
    )
    self.btn_backup.grid(row=2, column=0, padx=5, pady=2, sticky="ew")
    self.txt_log_backup = scrolledtext.ScrolledText(
        frame_etapas, height=3, width=45
    )
    self.txt_log_backup.grid(row=2, column=1, padx=5, pady=2)

    # Etapa D: Validação de Configuração
    self.btn_validar = tk.Button(
        frame_etapas,
        text="D. Validar Estado",
        bg="#6c757d",
        fg="white",
        font=("Arial", 8, "bold"),
        command=self.executar_validacao,
    )
    self.btn_validar.grid(row=3, column=0, padx=5, pady=2, sticky="ew")
    self.txt_log_validar = scrolledtext.ScrolledText(
        frame_etapas, height=3, width=45
    )
    self.txt_log_validar.grid(row=3, column=1, padx=5, pady=2)

    # Executa o preview inicial
    self.atualizar_preview()

  def atualizar_preview(self):
    hostname = self.entry_host.get().strip()
    if not hostname:
      self.txt_preview.delete("1.0", tk.END)
      self.txt_preview.insert(
          tk.END, "[ERRO] O campo Hostname não pode estar em branco!"
      )
      return

    try:
      vlans = [
          {
              "id": self.entry_v10_id.get().strip(),
              "name": self.entry_v10_name.get().strip(),
          },
          {
              "id": self.entry_v20_id.get().strip(),
              "name": self.entry_v20_name.get().strip(),
          },
          {
              "id": self.entry_v50_id.get().strip(),
              "name": self.entry_v50_name.get().strip(),
          },
      ]

      for v in vlans:
        if not v["id"] or not v["name"]:
          self.txt_preview.delete("1.0", tk.END)
          self.txt_preview.insert(
              tk.END, "[ERRO] Preencha todos os IDs e Nomes de VLANs!"
          )
          return

      comandos = ["configure terminal"]
      comandos.append(
          f"# [Condicional] hostname {hostname} (Aplicado apenas se diferente)"
      )
      for v in vlans:
        comandos.append(f"vlan {v['id']}")
        comandos.append(f" name {v['name']}")
      comandos.append("end")

      self.txt_preview.delete("1.0", tk.END)
      self.txt_preview.insert(tk.END, "\n".join(comandos))

    except Exception as e:
      self.txt_preview.delete("1.0", tk.END)
      self.txt_preview.insert(
          tk.END, f"[ERRO] Erro ao gerar preview: {e}"
      )

  def validar_permissao_usuario(self):
    ip = self.entry_ip.get().strip()
    user = self.entry_user.get().strip()
    senha = self.entry_pass.get()

    if not ip or not user:
      messagebox.showwarning("Aviso", "IP e Usuário são obrigatórios!")
      return

    try:
      manager = CiscoSwitchManager(ip, user, senha)
      net_conn = manager.conectar()
      output = net_conn.send_command("show privilege")
      net_conn.disconnect()

      if "15" in output:
        messagebox.showinfo(
            "Sucesso", "Usuário com privilégio Level 15 confirmado."
        )
      else:
        messagebox.showwarning(
            "Alerta", "Usuário NÃO está no nível de privilégio 15."
        )
    except Exception as e:
      messagebox.showerror("Erro", f"Falha na validação: {e}")

  def executar_aplicacao(self):
    ip = self.entry_ip.get().strip()
    user = self.entry_user.get().strip()
    senha = self.entry_pass.get()
    hostname = self.entry_host.get().strip()

    if not ip or not user or not hostname:
      messagebox.showerror("Erro", "Preencha IP, Usuário e Hostname!")
      return

    vlans = [
        {
            "id": self.entry_v10_id.get().strip(),
            "name": self.entry_v10_name.get().strip(),
        },
        {
            "id": self.entry_v20_id.get().strip(),
            "name": self.entry_v20_name.get().strip(),
        },
        {
            "id": self.entry_v50_id.get().strip(),
            "name": self.entry_v50_name.get().strip(),
        },
    ]

    self.txt_log_aplicar.delete("1.0", tk.END)
    self.txt_log_aplicar.insert(tk.END, "[*] Aplicando configurações...\n")
    self.root.update()

    try:
      manager = CiscoSwitchManager(ip, user, senha)
      _, hostname_atual = manager.aplicar_configuracoes_condicionais(
          hostname, vlans
      )
      self.txt_log_aplicar.insert(
          tk.END, f"[+] Sucesso! Hostname anterior: {hostname_atual}\n"
      )
      messagebox.showinfo("Sucesso", "Configurações aplicadas com sucesso!")
    except Exception as e:
      self.txt_log_aplicar.insert(tk.END, f"[X] Erro: {e}\n")
      messagebox.showerror("Erro", str(e))

  def executar_salvar(self):
    ip = self.entry_ip.get().strip()
    user = self.entry_user.get().strip()
    senha = self.entry_pass.get()

    if not ip or not user:
      messagebox.showerror("Erro", "Preencha IP e Usuário!")
      return

    self.txt_log_salvar.delete("1.0", tk.END)
    self.txt_log_salvar.insert(tk.END, "[*] Salvando na NVRAM...\n")
    self.root.update()

    try:
      manager = CiscoSwitchManager(ip, user, senha)
      manager.salvar_nvram()
      self.txt_log_salvar.insert(
          tk.END, "[+] Configuração salva na NVRAM com sucesso!\n"
      )
      messagebox.showinfo("Sucesso", "Configuração salva na NVRAM!")
    except Exception as e:
      self.txt_log_salvar.insert(tk.END, f"[X] Erro: {e}\n")
      messagebox.showerror("Erro", str(e))

  def executar_backup(self):
    ip = self.entry_ip.get().strip()
    user = self.entry_user.get().strip()
    senha = self.entry_pass.get()
    hostname = self.entry_host.get().strip()

    if not ip or not user or not hostname:
      messagebox.showerror("Erro", "Preencha IP, Usuário e Hostname!")
      return

    self.txt_log_backup.delete("1.0", tk.END)
    self.txt_log_backup.insert(tk.END, "[*] Gerando backup local...\n")
    self.root.update()

    try:
      manager = CiscoSwitchManager(ip, user, senha)
      bkp_file = manager.realizar_backup(hostname)
      self.txt_log_backup.insert(
          tk.END, f"[+] Backup salvo em:\n{bkp_file}\n"
      )
      messagebox.showinfo("Sucesso", f"Backup gerado em {bkp_file}")
    except Exception as e:
      self.txt_log_backup.insert(tk.END, f"[X] Erro: {e}\n")
      messagebox.showerror("Erro", str(e))

  def executar_validacao(self):
    ip = self.entry_ip.get().strip()
    user = self.entry_user.get().strip()
    senha = self.entry_pass.get()
    hostname = self.entry_host.get().strip()

    if not ip or not user or not hostname:
      messagebox.showerror("Erro", "Preencha IP, Usuário e Hostname!")
      return

    vlan_ids = [
        self.entry_v10_id.get().strip(),
        self.entry_v20_id.get().strip(),
        self.entry_v50_id.get().strip(),
    ]

    self.txt_log_validar.delete("1.0", tk.END)
    self.txt_log_validar.insert(tk.END, "[*] Validando estado atual...\n")
    self.root.update()

    try:
      manager = CiscoSwitchManager(ip, user, senha)
      divergencias = manager.validar_estado(hostname, vlan_ids)

      if divergencias:
        self.txt_log_validar.insert(
            tk.END, "[!] Divergências encontradas:\n"
        )
        for d in divergencias:
          self.txt_log_validar.insert(tk.END, f" - {d}\n")
        messagebox.showwarning(
            "Alerta de Validação", "Divergências detectadas no switch!"
        )
      else:
        self.txt_log_validar.insert(
            tk.END, "[+] Nenhuma divergência encontrada!\n"
        )
        messagebox.showinfo(
            "Sucesso", "Validação concluída sem divergências!"
        )
    except Exception as e:
      self.txt_log_validar.insert(tk.END, f"[X] Erro: {e}\n")
      messagebox.showerror("Erro", str(e))


if __name__ == "__main__":
  root = tk.Tk()
  app = AppAutomacaoModular(root)
  root.mainloop()