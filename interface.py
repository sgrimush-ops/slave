#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Interface Gráfica - Sistema de Gestão de Estoque com IA

Interface amigável para todas as funcionalidades do sistema:
- Importar arquivos de vendas
- Processar dados
- Executar análises
- Interagir com agente IA
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys
import subprocess
import threading
from pathlib import Path
from datetime import datetime, timedelta

# Adiciona diretórios ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))


class SistemaEstoqueGUI:
    """Interface gráfica principal do sistema"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestão de Estoque com IA")
        self.root.geometry("1400x800")  # Aumentado para acomodar 2 colunas
        
        # Configurar estilo
        self.configurar_estilo()
        
        # Variáveis
        self.arquivo_vendas = tk.StringVar()
        self.arquivo_gerado = tk.StringVar()
        self.data_venda = tk.StringVar(value=(datetime.now() - timedelta(days=1)).strftime('%d/%m/%y'))
        
        # Criar interface
        self.criar_interface()
        
        # Verificar arquivos no diretório data
        self.verificar_arquivos_existentes()
    
    def configurar_estilo(self):
        """Configura o estilo da interface"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Cores
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'), foreground='#2c3e50')
        style.configure('Subtitle.TLabel', font=('Arial', 10, 'bold'), foreground='#34495e')
        style.configure('Info.TLabel', font=('Arial', 9), foreground='#7f8c8d')
        style.configure('Success.TButton', background='#27ae60', foreground='white')
        style.configure('Primary.TButton', background='#3498db', foreground='white')
        style.configure('Warning.TButton', background='#e67e22', foreground='white')
    
    def criar_interface(self):
        """Cria todos os elementos da interface"""
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=2)  # Coluna esquerda
        main_frame.columnconfigure(1, weight=3)  # Coluna direita (log)
        main_frame.rowconfigure(1, weight=1)     # Permite expansão vertical
        
        # Título (ocupa as 2 colunas)
        titulo = ttk.Label(main_frame, text="Sistema de Gestão de Estoque com IA", 
                          style='Title.TLabel')
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # === COLUNA ESQUERDA: Controles ===
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # Seção 1: Importar Arquivos
        self.criar_secao_importacao(left_frame, 0)
        
        # Seção 2: Processar Vendas
        self.criar_secao_processar(left_frame, 1)
        
        # Seção 3: Análise e Pedidos
        self.criar_secao_analise(left_frame, 2)
        
        # Seção 4: Agente IA
        self.criar_secao_agente(left_frame, 3)
        
        # === COLUNA DIREITA: Log ===
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        right_frame.rowconfigure(0, weight=1)
        right_frame.columnconfigure(0, weight=1)
        
        # Seção 5: Log de Saída (ocupa toda coluna direita)
        self.criar_secao_log(right_frame, 0)
        
        # Barra de Status (ocupa as 2 colunas)
        self.criar_barra_status(main_frame, 2)
    
    def criar_secao_importacao(self, parent, row):
        """Cria seção de importação de arquivos"""
        frame = ttk.LabelFrame(parent, text="1. Importar Arquivos", padding="10")
        frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Arquivo de vendas
        ttk.Label(frame, text="Arquivo de Vendas (CSV):", style='Subtitle.TLabel').grid(
            row=0, column=0, sticky=tk.W, pady=5)
        
        entry_vendas = ttk.Entry(frame, textvariable=self.arquivo_vendas, width=50)
        entry_vendas.grid(row=0, column=1, padx=5, pady=5)
        
        btn_vendas = ttk.Button(frame, text="Selecionar...", 
                               command=self.selecionar_arquivo_vendas)
        btn_vendas.grid(row=0, column=2, padx=5, pady=5)
        
        btn_importar_vendas = ttk.Button(frame, text="Importar para data/", 
                                         command=self.importar_arquivo_vendas,
                                         style='Primary.TButton')
        btn_importar_vendas.grid(row=0, column=3, padx=5, pady=5)
        
        # Arquivo gerado
        ttk.Label(frame, text="Arquivo Gerado (Excel):", style='Subtitle.TLabel').grid(
            row=1, column=0, sticky=tk.W, pady=5)
        
        entry_gerado = ttk.Entry(frame, textvariable=self.arquivo_gerado, width=50)
        entry_gerado.grid(row=1, column=1, padx=5, pady=5)
        
        btn_gerado = ttk.Button(frame, text="Selecionar...", 
                               command=self.selecionar_arquivo_gerado)
        btn_gerado.grid(row=1, column=2, padx=5, pady=5)
        
        btn_importar_gerado = ttk.Button(frame, text="Importar para data/", 
                                        command=self.importar_arquivo_gerado,
                                        style='Primary.TButton')
        btn_importar_gerado.grid(row=1, column=3, padx=5, pady=5)
        
        # Info
        info = ttk.Label(frame, 
                        text="Importa arquivos para a pasta data/ antes do processamento",
                        style='Info.TLabel')
        info.grid(row=2, column=0, columnspan=4, pady=(10, 0))
    
    def criar_secao_processar(self, parent, row):
        """Cria seção de processamento de vendas"""
        frame = ttk.LabelFrame(parent, text="2. Processar Vendas Diárias", padding="10")
        frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Data da venda
        ttk.Label(frame, text="Data da Venda:", style='Subtitle.TLabel').grid(
            row=0, column=0, sticky=tk.W, pady=5)
        
        entry_data = ttk.Entry(frame, textvariable=self.data_venda, width=15)
        entry_data.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(frame, text="(formato: dd/mm/yy)", style='Info.TLabel').grid(
            row=0, column=2, sticky=tk.W, pady=5)
        
        # Botão processar
        btn_processar = ttk.Button(frame, text="Processar Vendas", 
                                   command=self.processar_vendas,
                                   style='Success.TButton',
                                   width=25)
        btn_processar.grid(row=1, column=0, columnspan=3, pady=10)
        
        # Info
        info = ttk.Label(frame, 
                        text="Executa tratamento_abc.py: filtra dados, salva Excel e atualiza histórico Parquet",
                        style='Info.TLabel')
        info.grid(row=2, column=0, columnspan=3, pady=(5, 0))
    
    def criar_secao_analise(self, parent, row):
        """Cria seção de análise e geração de pedidos"""
        frame = ttk.LabelFrame(parent, text="3. Análise e Geração de Pedidos", padding="10")
        frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Botões em grid
        btn_analista = ttk.Button(frame, text="Executar Analista Completo", 
                                 command=self.executar_analista,
                                 style='Success.TButton',
                                 width=30)
        btn_analista.grid(row=0, column=0, padx=5, pady=5)
        
        btn_calcular = ttk.Button(frame, text="Apenas Calcular Sugestões", 
                                 command=self.calcular_sugestoes,
                                 style='Primary.TButton',
                                 width=30)
        btn_calcular.grid(row=0, column=1, padx=5, pady=5)
        
        btn_estrategias = ttk.Button(frame, text="Analisar Estratégias", 
                                    command=self.analisar_estrategias,
                                    style='Primary.TButton',
                                    width=30)
        btn_estrategias.grid(row=1, column=0, padx=5, pady=5)
        
        btn_abrir_sugestao = ttk.Button(frame, text="Abrir Arquivo Sugestões", 
                                       command=self.abrir_sugestoes,
                                       width=30)
        btn_abrir_sugestao.grid(row=1, column=1, padx=5, pady=5)
        
        # Info
        info = ttk.Label(frame, 
                        text="Executa analista.py ou componentes individuais",
                        style='Info.TLabel')
        info.grid(row=2, column=0, columnspan=2, pady=(10, 0))
    
    def criar_secao_agente(self, parent, row):
        """Cria seção do agente IA"""
        frame = ttk.LabelFrame(parent, text="4. Agente IA (LLaMA 3)", padding="10")
        frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Área de pergunta
        ttk.Label(frame, text="Consultar Agente IA:", style='Subtitle.TLabel').grid(
            row=0, column=0, sticky=tk.W, pady=5)
        
        self.pergunta_agente = scrolledtext.ScrolledText(frame, height=4, width=70, wrap=tk.WORD)
        self.pergunta_agente.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
        
        # Bind Enter para enviar pergunta (Ctrl+Enter para nova linha)
        self.pergunta_agente.bind('<Return>', self.consultar_agente_enter)
        
        # Botões
        btn_consultar = ttk.Button(frame, text="Consultar Agente", 
                                  command=self.consultar_agente,
                                  style='Success.TButton',
                                  width=20)
        btn_consultar.grid(row=2, column=0, pady=5, padx=5)
        
        btn_limpar_pergunta = ttk.Button(frame, text="Limpar Pergunta", 
                                  command=self.limpar_pergunta,
                                  width=20)
        btn_limpar_pergunta.grid(row=2, column=1, pady=5, padx=5)
        
        btn_historico = ttk.Button(frame, text="Ver Histórico de Vendas", 
                                  command=self.abrir_consulta_vendas,
                                  style='Primary.TButton',
                                  width=20)
        btn_historico.grid(row=2, column=2, pady=5, padx=5)
        
        # Botões de gerenciamento Ollama
        btn_iniciar_ollama = ttk.Button(frame, text="Iniciar Ollama", 
                                       command=self.iniciar_ollama_manual,
                                       style='Warning.TButton',
                                       width=25)
        btn_iniciar_ollama.grid(row=3, column=0, pady=5, padx=5)
        
        btn_listar_modelos = ttk.Button(frame, text="Ver Modelos Instalados", 
                                       command=self.listar_modelos_ollama,
                                       style='Primary.TButton',
                                       width=25)
        btn_listar_modelos.grid(row=3, column=1, pady=5, padx=5)
        
        # Info
        info = ttk.Label(frame, 
                        text="Requer Ollama rodando com algum modelo instalado (llama3, mistral, etc)",
                        style='Info.TLabel')
        info.grid(row=4, column=0, columnspan=2, pady=(5, 0))
    
    def criar_secao_log(self, parent, row):
        """Cria seção de log de saída"""
        frame = ttk.LabelFrame(parent, text="Log de Execução", padding="10")
        frame.grid(row=row, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        
        # Área de log com altura maior
        self.log_text = scrolledtext.ScrolledText(frame, width=80, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 5))
        self.log_text.config(state=tk.DISABLED)
        
        # Botão limpar
        btn_limpar = ttk.Button(frame, text="Limpar Log", command=self.limpar_log)
        btn_limpar.grid(row=1, column=0, pady=(0, 5))
    
    def criar_barra_status(self, parent, row):
        """Cria barra de status"""
        self.status_var = tk.StringVar(value="Pronto")
        status_bar = ttk.Label(parent, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
    
    # Métodos de verificação
    
    def verificar_arquivos_existentes(self):
        """Verifica se arquivos já existem no diretório data"""
        data_dir = Path("data")
        
        vendas_path = data_dir / "grid_tmp_abcmerc.csv"
        if vendas_path.exists():
            self.arquivo_vendas.set(str(vendas_path))
            self.log(f"[OK] Arquivo de vendas encontrado: {vendas_path}")
        
        gerado_path = data_dir / "gerado.xlsx"
        if gerado_path.exists():
            self.arquivo_gerado.set(str(gerado_path))
            self.log(f"[OK] Arquivo gerado encontrado: {gerado_path}")
    
    # Métodos de seleção de arquivos
    
    def selecionar_arquivo_vendas(self):
        """Seleciona arquivo de vendas CSV"""
        filename = filedialog.askopenfilename(
            title="Selecionar Arquivo de Vendas",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.arquivo_vendas.set(filename)
            self.log(f"Arquivo selecionado: {filename}")
    
    def selecionar_arquivo_gerado(self):
        """Seleciona arquivo gerado Excel"""
        filename = filedialog.askopenfilename(
            title="Selecionar Arquivo Gerado",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if filename:
            self.arquivo_gerado.set(filename)
            self.log(f"Arquivo selecionado: {filename}")
    
    # Métodos de importação
    
    def importar_arquivo_vendas(self):
        """Importa arquivo de vendas para data/"""
        arquivo = self.arquivo_vendas.get()
        if not arquivo or not os.path.exists(arquivo):
            messagebox.showerror("Erro", "Selecione um arquivo válido")
            return
        
        try:
            destino = Path("data") / "grid_tmp_abcmerc.csv"
            destino.parent.mkdir(exist_ok=True)
            
            # Verificar se já é o mesmo arquivo
            arquivo_path = Path(arquivo).resolve()
            destino_path = destino.resolve()
            
            if arquivo_path == destino_path:
                self.log("[AVISO] Arquivo já está no destino correto")
                self.status_var.set("Arquivo já está em data/")
                messagebox.showinfo("Informação", "Arquivo já está no destino correto")
                return
            
            import shutil
            shutil.copy2(arquivo, destino)
            
            self.log(f"[OK] Arquivo importado para: {destino}")
            self.status_var.set("Arquivo de vendas importado com sucesso")
            messagebox.showinfo("Sucesso", f"Arquivo importado para:\n{destino}")
            
        except Exception as e:
            self.log(f"[ERRO] Falha ao importar: {e}")
            messagebox.showerror("Erro", f"Falha ao importar arquivo:\n{e}")
    
    def importar_arquivo_gerado(self):
        """Importa arquivo gerado para data/"""
        arquivo = self.arquivo_gerado.get()
        if not arquivo or not os.path.exists(arquivo):
            messagebox.showerror("Erro", "Selecione um arquivo válido")
            return
        
        try:
            destino = Path("data") / "gerado.xlsx"
            destino.parent.mkdir(exist_ok=True)
            
            # Verificar se já é o mesmo arquivo
            arquivo_path = Path(arquivo).resolve()
            destino_path = destino.resolve()
            
            if arquivo_path == destino_path:
                self.log("[AVISO] Arquivo já está no destino correto")
                self.status_var.set("Arquivo já está em data/")
                messagebox.showinfo("Informação", "Arquivo já está no destino correto")
                return
            
            import shutil
            shutil.copy2(arquivo, destino)
            
            self.log(f"[OK] Arquivo importado para: {destino}")
            self.status_var.set("Arquivo gerado importado com sucesso")
            messagebox.showinfo("Sucesso", f"Arquivo importado para:\n{destino}")
            
        except Exception as e:
            self.log(f"[ERRO] Falha ao importar: {e}")
            messagebox.showerror("Erro", f"Falha ao importar arquivo:\n{e}")
    
    # Métodos de processamento
    
    def processar_vendas(self):
        """Executa tratamento_abc.py"""
        data = self.data_venda.get()
        if not data:
            messagebox.showerror("Erro", "Informe a data da venda")
            return
        
        # Verificar se arquivo existe
        if not Path("data/grid_tmp_abcmerc.csv").exists():
            messagebox.showerror("Erro", 
                               "Arquivo grid_tmp_abcmerc.csv não encontrado em data/\n"
                               "Importe o arquivo primeiro.")
            return
        
        self.log(f"\n{'='*60}")
        self.log(f"Iniciando processamento de vendas para {data}...")
        self.status_var.set("Processando vendas...")
        
        def executar():
            try:
                # Executa tratamento_abc.py com data
                processo = subprocess.Popen(
                    [sys.executable, "tratamento_abc.py"],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding='utf-8',
                    errors='replace'
                )
                
                # Envia data
                stdout, _ = processo.communicate(input=f"{data}\n")
                
                # Mostra saída
                self.log(stdout)
                
                if processo.returncode == 0:
                    self.log("[OK] Processamento concluido com sucesso!")
                    self.status_var.set("Vendas processadas com sucesso")
                    messagebox.showinfo("Sucesso", 
                                      "Vendas processadas!\n"
                                      "- resultado_abc.xlsx gerado\n"
                                      "- Histórico Parquet atualizado")
                else:
                    self.log("[ERRO] Erro no processamento")
                    self.status_var.set("Erro no processamento")
                    
            except Exception as e:
                self.log(f"[ERRO] {e}")
                self.status_var.set("Erro")
        
        # Executa em thread separada
        thread = threading.Thread(target=executar, daemon=True)
        thread.start()
    
    def executar_analista(self):
        """Executa analista.py completo"""
        if not Path("data/banco.db").exists():
            messagebox.showerror("Erro", 
                               "Banco de dados não encontrado!\n"
                               "Execute: python launchers/criar_db.py")
            return
        
        resposta = messagebox.askyesno("Confirmar", 
                                      "Executar análise completa?\n\n"
                                      "Isso irá:\n"
                                      "1. Calcular sugestões\n"
                                      "2. Gerar análises\n\n"
                                      "NOTA: Executa cálculos apenas, não inicia o modo interativo.\n\n"
                                      "Continuar?")
        if not resposta:
            return
        
        self.log(f"\n{'='*60}")
        self.log("Executando analista completo...")
        self.log("[INFO] Este processo pode demorar alguns minutos...")
        self.log("[INFO] Acompanhe o progresso abaixo...")
        self.status_var.set("Executando analista (aguarde)...")
        
        def executar():
            try:
                # Etapa 1: Calcular Sugestões
                self.log("\n=== ETAPA 1: Calculando Sugestões ===")
                self.log("[INFO] Aplicando estratégias de balanceamento...")
                
                processo1 = subprocess.Popen(
                    [sys.executable, "scripts/atualizar_simples.py"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    bufsize=1,
                    universal_newlines=True
                )
                
                while True:
                    output = processo1.stdout.readline()
                    if output == '' and processo1.poll() is not None:
                        break
                    if output:
                        self.log(output.strip())
                
                stderr1 = processo1.stderr.read()
                if stderr1:
                    self.log(stderr1)
                
                if processo1.wait() != 0:
                    self.log("[ERRO] Falha no cálculo de sugestões")
                    self.status_var.set("Erro no cálculo")
                    return
                
                self.log("\n[OK] Sugestões calculadas com sucesso!")
                
                # Etapa 2: Analisar Estratégias
                self.log("\n=== ETAPA 2: Analisando Estratégias ===")
                
                processo2 = subprocess.Popen(
                    [sys.executable, "scripts/analisar_estrategias.py"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    bufsize=1,
                    universal_newlines=True
                )
                
                while True:
                    output = processo2.stdout.readline()
                    if output == '' and processo2.poll() is not None:
                        break
                    if output:
                        self.log(output.strip())
                
                stderr2 = processo2.stderr.read()
                if stderr2:
                    self.log(stderr2)
                
                if processo2.wait() != 0:
                    self.log("[ERRO] Falha na análise de estratégias")
                    self.status_var.set("Erro na análise")
                    return
                
                self.log("\n[OK] Análise de estratégias concluída!")
                
                # Conclusão
                self.log("\n" + "="*60)
                self.log("[OK] ANALISTA COMPLETO - CONCLUÍDO COM SUCESSO!")
                self.log("="*60)
                self.log("\nArquivos gerados:")
                self.log("  • data/sugestao_ia.xlsx - Sugestões de pedido")
                self.log("  • data/analise_estrategias.xlsx - Análise detalhada")
                self.log("\nVocê pode agora:")
                self.log("  • Abrir os arquivos Excel para revisar")
                self.log("  • Consultar o Agente IA sobre os resultados")
                
                self.status_var.set("Análise completa concluída!")
                messagebox.showinfo("Sucesso", 
                                  "Análise completa concluída!\n\n"
                                  "Arquivos gerados:\n"
                                  "• data/sugestao_ia.xlsx\n"
                                  "• data/analise_estrategias.xlsx\n\n"
                                  "Use o Agente IA para consultas!")
                    
            except Exception as e:
                self.log(f"\n[ERRO] Exceção durante execução: {e}")
                import traceback
                self.log(traceback.format_exc())
                self.status_var.set("Erro na execução")
                messagebox.showerror("Erro", f"Erro ao executar analista:\n{e}")
        
        thread = threading.Thread(target=executar, daemon=True)
        thread.start()
    
    def calcular_sugestoes(self):
        """Calcula apenas as sugestões"""
        self.log(f"\n{'='*60}")
        self.log("Calculando sugestoes de pedido...")
        self.log("[INFO] Acompanhe o progresso abaixo...")
        self.status_var.set("Calculando sugestões (aguarde)...")
        
        def executar():
            try:
                processo = subprocess.Popen(
                    [sys.executable, "scripts/atualizar_simples.py"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    bufsize=1,
                    universal_newlines=True
                )
                
                # Ler output em tempo real
                while True:
                    output = processo.stdout.readline()
                    if output == '' and processo.poll() is not None:
                        break
                    if output:
                        self.log(output.strip())
                
                stderr = processo.stderr.read()
                if stderr:
                    self.log(stderr)
                
                returncode = processo.wait()
                
                if returncode == 0:
                    self.log("\n[OK] Sugestoes calculadas!")
                    self.status_var.set("Sugestões calculadas")
                    messagebox.showinfo("Sucesso", 
                                      "Sugestões calculadas!\n"
                                      "Arquivo: data/sugestao_ia.xlsx")
                else:
                    self.log(f"\n[ERRO] Erro no cálculo (código {returncode})")
                    self.status_var.set("Erro no cálculo")
                    
            except Exception as e:
                self.log(f"[ERRO] {e}")
                import traceback
                self.log(traceback.format_exc())
                self.status_var.set("Erro")
        
        thread = threading.Thread(target=executar, daemon=True)
        thread.start()
    
    def analisar_estrategias(self):
        """Analisa estratégias aplicadas"""
        self.log(f"\n{'='*60}")
        self.log("Analisando estrategias...")
        self.log("[INFO] Acompanhe o progresso abaixo...")
        self.status_var.set("Analisando estratégias (aguarde)...")
        
        def executar():
            try:
                processo = subprocess.Popen(
                    [sys.executable, "scripts/analisar_estrategias.py"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    bufsize=1,
                    universal_newlines=True
                )
                
                # Ler output em tempo real
                while True:
                    output = processo.stdout.readline()
                    if output == '' and processo.poll() is not None:
                        break
                    if output:
                        self.log(output.strip())
                
                stderr = processo.stderr.read()
                if stderr:
                    self.log(stderr)
                
                returncode = processo.wait()
                
                if returncode == 0:
                    self.log("\n[OK] Analise concluida!")
                    self.status_var.set("Análise concluída")
                    messagebox.showinfo("Sucesso", 
                                      "Análise de estratégias concluída!\n"
                                      "Arquivo: data/analise_estrategias.xlsx")
                else:
                    self.log(f"\n[ERRO] Erro na análise (código {returncode})")
                    self.status_var.set("Erro")
                    
            except Exception as e:
                self.log(f"[ERRO] {e}")
                import traceback
                self.log(traceback.format_exc())
                self.status_var.set("Erro")
        
        thread = threading.Thread(target=executar, daemon=True)
        thread.start()
    
    def abrir_sugestoes(self):
        """Abre arquivo de sugestões"""
        arquivo = Path("data/sugestao_ia.xlsx")
        if not arquivo.exists():
            messagebox.showerror("Erro", "Arquivo de sugestões não encontrado!\n"
                                        "Execute o cálculo de sugestões primeiro.")
            return
        
        try:
            if sys.platform == 'win32':
                os.startfile(arquivo)
            else:
                subprocess.run(['xdg-open', arquivo])
            self.log(f"[OK] Abrindo: {arquivo}")
        except Exception as e:
            self.log(f"[ERRO] Não foi possível abrir: {e}")
    
    def consultar_agente(self):
        """Consulta o agente IA"""
        pergunta = self.pergunta_agente.get('1.0', tk.END).strip()
        
        if not pergunta:
            messagebox.showwarning("Aviso", "Digite uma pergunta para o agente")
            return
        
        # Verificar se Ollama está rodando
        if not self.verificar_ollama():
            return
        
        self.log(f"\n{'='*60}")
        self.log(f"Consultando agente IA...")
        self.log(f"Pergunta: {pergunta}")
        self.status_var.set("Consultando agente IA...")
        
        def executar():
            try:
                # Redirecionar stdout para capturar logs do agente
                import io
                from contextlib import redirect_stdout, redirect_stderr
                
                # Criar buffer para capturar prints
                stdout_buffer = io.StringIO()
                stderr_buffer = io.StringIO()
                
                # Importa agente
                from src.agente_estoque import AgenteEstoque
                
                # Capturar prints do agente durante inicialização e consulta
                with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
                    agente = AgenteEstoque(usar_historico=True)
                    
                    # Forçar recarregamento do histórico para pegar dados mais recentes
                    if agente.analisador:
                        agente.analisador.recarregar()
                        print("[INFO] Histórico recarregado do disco")
                    
                    resposta = agente.consulta_livre(pergunta)
                
                # Mostrar logs capturados
                logs_stdout = stdout_buffer.getvalue()
                logs_stderr = stderr_buffer.getvalue()
                
                if logs_stdout:
                    self.log("\n--- Logs do Agente ---")
                    self.log(logs_stdout.strip())
                    self.log("--- Fim dos Logs ---\n")
                
                if logs_stderr:
                    self.log("\n--- Avisos/Erros ---")
                    self.log(logs_stderr.strip())
                    self.log("--- Fim dos Avisos ---\n")
                
                self.log(f"\nResposta do Agente:")
                self.log("-" * 60)
                self.log(resposta)
                self.log("-" * 60)
                self.status_var.set("Consulta concluída")
                
            except Exception as e:
                erro_msg = str(e)
                self.log(f"[ERRO] {erro_msg}")
                
                # Verificar se é erro de modelo não instalado
                if "not found" in erro_msg.lower() or "404" in erro_msg:
                    self.log("\n[SOLUÇÃO] Para instalar um modelo Ollama:")
                    self.log("1. Abra um terminal (CMD)")
                    self.log("2. Execute: ollama pull llama3")
                    self.log("   ou: ollama pull llama3.2")
                    self.log("   ou: ollama pull mistral")
                    self.log("3. Aguarde o download completar")
                    self.log("4. Tente novamente")
                    
                    messagebox.showerror(
                        "Modelo não instalado",
                        "Nenhum modelo de IA encontrado no Ollama.\n\n"
                        "Para instalar, abra um CMD e execute:\n"
                        "   ollama pull llama3.2\n\n"
                        "Modelos recomendados:\n"
                        "• llama3.2 (rápido, 3GB)\n"
                        "• llama3 (completo, 4.7GB)\n"
                        "• mistral (alternativa, 4GB)\n\n"
                        "Após instalar, clique em 'Consultar Agente' novamente."
                    )
                else:
                    self.log("Verifique se Ollama está rodando corretamente")
                
                self.status_var.set("Erro ao consultar agente")
        
        thread = threading.Thread(target=executar, daemon=True)
        thread.start()
    
    def consultar_agente_enter(self, event):
        """Chama consultar_agente quando Enter for pressionado"""
        # Ctrl+Enter ou Shift+Enter = nova linha (comportamento padrão)
        if event.state & 0x4 or event.state & 0x1:  # Ctrl ou Shift pressionado
            return
        
        # Enter sozinho = consultar agente
        self.consultar_agente()
        return 'break'  # Impede inserção de nova linha
    
    def limpar_pergunta(self):
        """Limpa o campo de pergunta do agente"""
        self.pergunta_agente.delete('1.0', tk.END)
        self.pergunta_agente.focus()
    
    def listar_modelos_ollama(self):
        """Lista modelos Ollama instalados"""
        self.log(f"\n{'='*60}")
        self.log("Verificando modelos Ollama instalados...")
        self.status_var.set("Verificando modelos...")
        
        def executar():
            try:
                import requests
                response = requests.get('http://localhost:11434/api/tags', timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    modelos = data.get('models', [])
                    
                    if not modelos:
                        self.log("\n[AVISO] Nenhum modelo instalado no Ollama!")
                        self.log("\n[INSTRUCOES] Para instalar um modelo:")
                        self.log("1. Abra um terminal (CMD)")
                        self.log("2. Execute um dos comandos:")
                        self.log("   • ollama pull llama3.2    (recomendado, ~3GB)")
                        self.log("   • ollama pull llama3      (completo, ~4.7GB)")
                        self.log("   • ollama pull mistral     (alternativa, ~4GB)")
                        self.log("   • ollama pull phi3        (leve, ~2GB)")
                        self.log("3. Aguarde o download completar")
                        
                        messagebox.showwarning(
                            "Nenhum modelo instalado",
                            "Nenhum modelo encontrado no Ollama.\n\n"
                            "Instale um modelo executando no CMD:\n"
                            "   ollama pull llama3.2\n\n"
                            "Veja mais modelos em: https://ollama.ai/library"
                        )
                    else:
                        self.log(f"\n[OK] {len(modelos)} modelo(s) encontrado(s):\n")
                        
                        for modelo in modelos:
                            nome = modelo.get('name', 'desconhecido')
                            tamanho = modelo.get('size', 0)
                            tamanho_gb = tamanho / (1024**3)
                            modified = modelo.get('modified_at', '')
                            
                            self.log(f"  • {nome}")
                            self.log(f"    Tamanho: {tamanho_gb:.2f} GB")
                            if modified:
                                self.log(f"    Modificado: {modified[:10]}")
                            self.log("")
                        
                        self.log("[INFO] O sistema usará automaticamente um destes modelos.")
                        self.status_var.set(f"{len(modelos)} modelo(s) instalado(s)")
                        
                        # Mostrar em messagebox também
                        lista_modelos = "\n".join([f"• {m['name']}" for m in modelos])
                        messagebox.showinfo(
                            "Modelos instalados",
                            f"Modelos Ollama instalados:\n\n{lista_modelos}\n\n"
                            f"O agente IA usará automaticamente um destes modelos."
                        )
                else:
                    self.log(f"[ERRO] Erro ao conectar com Ollama (status {response.status_code})")
                    self.status_var.set("Erro ao verificar modelos")
                    
            except Exception as e:
                self.log(f"[ERRO] Não foi possível conectar com Ollama: {e}")
                self.log("[INFO] Certifique-se que o Ollama está rodando")
                self.log("[INFO] Clique em 'Iniciar Ollama' primeiro")
                self.status_var.set("Erro: Ollama não está rodando")
                
                messagebox.showerror(
                    "Erro",
                    f"Não foi possível conectar com Ollama.\n\n"
                    f"Erro: {e}\n\n"
                    f"Certifique-se que o Ollama está rodando."
                )
        
        thread = threading.Thread(target=executar, daemon=True)
        thread.start()
    
    def abrir_consulta_vendas(self):
        """Abre utilitário de consulta de vendas"""
        if not Path("data/vendas_historico.parquet").exists():
            messagebox.showwarning("Aviso", 
                                 "Histórico de vendas não encontrado!\n"
                                 "Processe as vendas primeiro (tratamento_abc.py)")
            return
        
        try:
            # Abre em nova janela de terminal (não bloqueia)
            if sys.platform == 'win32':
                # Windows: abre em nova janela cmd
                subprocess.Popen(
                    ['cmd', '/c', 'start', 'cmd', '/k', 
                     sys.executable, 'utilitarios/consultar_vendas.py'],
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
            else:
                # Linux/Mac: abre em novo terminal
                subprocess.Popen([sys.executable, "utilitarios/consultar_vendas.py"])
            
            self.log("[OK] Abrindo consulta de vendas em nova janela...")
        except Exception as e:
            self.log(f"[ERRO] {e}")
    
    # Métodos auxiliares
    
    def verificar_ollama(self):
        """Verifica se Ollama está rodando"""
        try:
            import requests
            
            self.log("[INFO] Verificando se Ollama está rodando...")
            
            # Primeiro: verificar se o processo está ativo (Windows)
            if sys.platform == 'win32':
                try:
                    import subprocess
                    result = subprocess.run(
                        ['tasklist', '/FI', 'IMAGENAME eq ollama.exe'],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if 'ollama.exe' in result.stdout:
                        self.log("[OK] Processo ollama.exe encontrado na memória")
                    else:
                        self.log("[AVISO] Processo ollama.exe NÃO encontrado")
                except Exception as e:
                    self.log(f"[INFO] Não foi possível verificar processo: {e}")
            
            # Testar múltiplos endpoints para detectar Ollama
            endpoints = [
                'http://localhost:11434/api/tags',
                'http://localhost:11434/api/version',
                'http://localhost:11434/',
                'http://127.0.0.1:11434/api/tags',
                'http://127.0.0.1:11434/'
            ]
            
            self.log("[INFO] Testando conexão com servidor Ollama...")
            
            for endpoint in endpoints:
                try:
                    self.log(f"[INFO] Tentando: {endpoint}")
                    response = requests.get(endpoint, timeout=5)
                    self.log(f"[INFO] Resposta: Status {response.status_code}")
                    
                    if response.status_code in [200, 404]:  # 404 também indica que servidor está rodando
                        self.log(f"[OK] Ollama DETECTADO em: {endpoint}")
                        self.status_var.set("Ollama detectado e disponível")
                        return True
                        
                except requests.exceptions.ConnectionError as e:
                    self.log(f"[AVISO] {endpoint} - Sem conexão: {e}")
                    continue
                except requests.exceptions.Timeout as e:
                    self.log(f"[AVISO] {endpoint} - Timeout: {e}")
                    continue
                except Exception as e:
                    self.log(f"[AVISO] {endpoint} - Erro: {e}")
                    continue
            
            # Se chegou aqui, não encontrou em nenhum endpoint
            self.log("[ERRO] Ollama não respondeu em nenhum endpoint conhecido")
            self.log("[INFO] Verifique se o Ollama está realmente executando 'ollama serve'")
            return self.tentar_iniciar_ollama()
            
        except Exception as e:
            self.log(f"[ERRO] Erro ao verificar Ollama: {e}")
            import traceback
            self.log(f"[DEBUG] {traceback.format_exc()}")
            return False
    
    def tentar_iniciar_ollama(self):
        """Tenta iniciar o Ollama automaticamente"""
        self.log("[AVISO] Ollama não está rodando")
        
        # Perguntar se quer tentar iniciar
        resposta = messagebox.askyesno(
            "Ollama não disponível",
            "Ollama não está rodando.\n\n"
            "Deseja tentar iniciar o Ollama automaticamente?\n\n"
            "Nota: O Ollama precisa estar instalado.\n"
            "Se não estiver instalado, baixe em: https://ollama.ai/download"
        )
        
        if not resposta:
            return False
        
        try:
            self.log("[OK] Tentando iniciar Ollama...")
            self.status_var.set("Iniciando Ollama...")
            
            # Tentar iniciar Ollama em background
            if sys.platform == 'win32':
                # Windows: Tentar iniciar ollama serve em nova janela
                subprocess.Popen(
                    ['cmd', '/c', 'start', 'cmd', '/k', 'ollama', 'serve'],
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
            else:
                # Linux/Mac
                subprocess.Popen(['ollama', 'serve'], 
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
            
            # Aguardar alguns segundos para Ollama iniciar
            self.log("[OK] Aguardando Ollama iniciar (5 segundos)...")
            import time
            time.sleep(5)
            
            # Verificar se iniciou (testando múltiplos endpoints)
            import requests
            endpoints = [
                'http://localhost:11434/api/tags',
                'http://localhost:11434/',
                'http://127.0.0.1:11434/api/tags'
            ]
            
            for tentativa in range(3):
                for endpoint in endpoints:
                    try:
                        response = requests.get(endpoint, timeout=2)
                        if response.status_code in [200, 404]:
                            self.log(f"[OK] Ollama iniciado com sucesso em: {endpoint}")
                            self.status_var.set("Ollama iniciado com sucesso")
                            messagebox.showinfo("Sucesso", 
                                              "Ollama iniciado com sucesso!\n"
                                              "Você pode usar o Agente IA agora.")
                            return True
                    except:
                        continue
                
                if tentativa < 2:
                    self.log(f"[AVISO] Tentativa {tentativa + 1}/3... aguardando...")
                    time.sleep(3)
            
            # Se chegou aqui, não conseguiu iniciar
            self.log("[ERRO] Não foi possível iniciar Ollama automaticamente")
            self.status_var.set("Falha ao iniciar Ollama")
            messagebox.showerror("Erro ao iniciar Ollama",
                               "Não foi possível iniciar o Ollama automaticamente.\n\n"
                               "Soluções:\n"
                               "1. Abra um terminal e execute: ollama serve\n"
                               "2. Ou verifique se Ollama está instalado\n"
                               "3. Instale do site: https://ollama.ai/download")
            return False
            
        except FileNotFoundError:
            self.log("[ERRO] Ollama não está instalado")
            self.status_var.set("Ollama não instalado")
            messagebox.showerror("Ollama não instalado",
                               "Ollama não está instalado no sistema.\n\n"
                               "Para usar o Agente IA:\n"
                               "1. Baixe Ollama: https://ollama.ai/download\n"
                               "2. Instale o Ollama\n"
                               "3. Execute: ollama pull llama3\n"
                               "4. Reinicie esta interface")
            return False
        except Exception as e:
            self.log(f"[ERRO] Erro ao tentar iniciar Ollama: {e}")
            self.status_var.set("Erro ao iniciar Ollama")
            messagebox.showerror("Erro",
                               f"Erro ao tentar iniciar Ollama:\n{e}\n\n"
                               "Tente iniciar manualmente: ollama serve")
            return False
    
    def iniciar_ollama_manual(self):
        """Botão para iniciar Ollama manualmente"""
        self.log("\n" + "="*60)
        self.log("Iniciando Ollama manualmente...")
        self.status_var.set("Verificando Ollama...")
        
        def executar():
            # Verificar se já está rodando
            try:
                import requests
                response = requests.get('http://localhost:11434/api/tags', timeout=2)
                if response.status_code == 200:
                    self.log("[OK] Ollama já está rodando!")
                    self.status_var.set("Ollama ativo")
                    messagebox.showinfo("Ollama Ativo", 
                                      "Ollama já está rodando!\n"
                                      "Você pode usar o Agente IA.")
                    return
            except:
                pass
            
            # Tentar iniciar
            if self.tentar_iniciar_ollama():
                self.log("[OK] Ollama iniciado com sucesso!")
            else:
                self.log("[ERRO] Não foi possível iniciar Ollama")
        
        # Executar em thread separada
        thread = threading.Thread(target=executar, daemon=True)
        thread.start()
    
    def log(self, mensagem):
        """Adiciona mensagem ao log"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, mensagem + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def limpar_log(self):
        """Limpa o log"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete('1.0', tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.status_var.set("Log limpo")


def main():
    """Função principal"""
    # Verificar se está sendo executado diretamente
    if __name__ != "__main__":
        return
    
    print("Iniciando interface grafica...")
    root = tk.Tk()
    app = SistemaEstoqueGUI(root)
    print("Interface carregada. Aguardando interacao do usuario...")
    root.mainloop()
    print("Interface encerrada.")


if __name__ == "__main__":
    main()
