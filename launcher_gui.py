import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import threading
import os
import sys
import time
import queue
from datetime import datetime

class ScriptLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Pistolinha - Executor de Automações")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variáveis de controle
        self.current_process = None
        self.is_running = False
        self.log_queue = queue.Queue()
        
        # Configuração dos scripts disponíveis
        self.scripts_config = {
            "Fechamento PDF Magalu": {
                "file": "script_fechamento.py",
                "description": "Processa extração de PDFs de motoristas e gera fechamento em Excel",
                "args": ["--pdfs_folder", "--type_sheet", "--output_excel"],
                "required_files": ["config.ini"]
            },
            "Outro Script": {
                "file": "outro_script.py", 
                "description": "Exemplo de outro script",
                "args": ["--input", "--output"],
                "required_files": []
            }
            # Adicione mais scripts aqui conforme necessário
        }
        
        self.setup_ui()
        self.check_log_queue()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar redimensionamento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text=" 🔫 Pistolinha Launcher", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Seleção de Script
        ttk.Label(main_frame, text="Selecionar Script:", 
                 font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        self.script_var = tk.StringVar()
        self.script_combo = ttk.Combobox(main_frame, textvariable=self.script_var,
                                        values=list(self.scripts_config.keys()),
                                        state="readonly", width=40)
        self.script_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        self.script_combo.bind('<<ComboboxSelected>>', self.on_script_selected)
        
        # Botão para selecionar script personalizado
        ttk.Button(main_frame, text="Procurar Script...", 
                  command=self.browse_script).grid(row=1, column=2, padx=(10, 0), pady=(0, 5))
        
        # Descrição do script
        self.description_label = ttk.Label(main_frame, text="", foreground="gray")
        self.description_label.grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))
        
        # Frame para controles
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        control_frame.columnconfigure(2, weight=1)
        
        # Botões de controle
        self.start_button = ttk.Button(control_frame, text="▶ Executar", 
                                      command=self.start_script, style="Accent.TButton")
        self.start_button.grid(row=0, column=0, padx=(0, 10))
        
        self.stop_button = ttk.Button(control_frame, text="⏹ Parar", 
                                     command=self.stop_script, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=(0, 10))
        
        # Barra de progresso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(control_frame, variable=self.progress_var, 
                                           mode='indeterminate')
        self.progress_bar.grid(row=0, column=2, sticky=(tk.W, tk.E), padx=(10, 0))
        
        # Status
        self.status_var = tk.StringVar(value="Pronto para executar")
        status_label = ttk.Label(control_frame, textvariable=self.status_var, 
                                foreground="green")
        status_label.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(5, 0))
        
        # Frame para logs
        log_frame = ttk.LabelFrame(main_frame, text="Logs de Execução", padding="5")
        log_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Área de logs com scroll
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Botões para logs
        log_buttons = ttk.Frame(log_frame)
        log_buttons.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        ttk.Button(log_buttons, text="Limpar Logs", 
                  command=self.clear_logs).grid(row=0, column=0)
        ttk.Button(log_buttons, text="Salvar Logs", 
                  command=self.save_logs).grid(row=0, column=1, padx=(10, 0))
        
        # Configurar tags para colorir logs
        self.log_text.tag_configure("INFO", foreground="black")
        self.log_text.tag_configure("WARNING", foreground="orange")
        self.log_text.tag_configure("ERROR", foreground="red")
        self.log_text.tag_configure("SUCCESS", foreground="green")
        
    def on_script_selected(self, event=None):
        """Atualiza a descrição quando um script é selecionado"""
        selected = self.script_var.get()
        if selected in self.scripts_config:
            desc = self.scripts_config[selected]["description"]
            self.description_label.config(text=f"📋 {desc}")
        
    def browse_script(self):
        """Permite selecionar um script personalizado"""
        file_path = filedialog.askopenfilename(
            title="Selecionar Script Python",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        if file_path:
            script_name = os.path.basename(file_path)
            self.scripts_config[script_name] = {
                "file": file_path,
                "description": "Script personalizado selecionado",
                "args": [],
                "required_files": []
            }
            # Atualizar combobox
            self.script_combo['values'] = list(self.scripts_config.keys())
            self.script_var.set(script_name)
            self.on_script_selected()
    
    def log_message(self, message, level="INFO"):
        """Adiciona mensagem ao log com timestamp e nível"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] {level}: {message}\n"
        
        # Adicionar à queue para thread-safe update
        self.log_queue.put((formatted_msg, level))
    
    def check_log_queue(self):
        """Verifica a queue de logs e atualiza a interface"""
        try:
            while True:
                message, level = self.log_queue.get_nowait()
                self.log_text.insert(tk.END, message, level)
                self.log_text.see(tk.END)
        except queue.Empty:
            pass
        
        # Reagendar verificação
        self.root.after(100, self.check_log_queue)
    
    def clear_logs(self):
        """Limpa a área de logs"""
        self.log_text.delete(1.0, tk.END)
        self.log_message("Logs limpos", "INFO")
    
    def save_logs(self):
        """Salva os logs em arquivo"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".log",
            filetypes=[("Log files", "*.log"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.get(1.0, tk.END))
                self.log_message(f"Logs salvos em: {file_path}", "SUCCESS")
            except Exception as e:
                self.log_message(f"Erro ao salvar logs: {e}", "ERROR")
    
    def validate_script(self, script_config):
        """Valida se o script e arquivos necessários existem"""
        script_file = script_config["file"]
        
        # Verifica se o arquivo do script existe
        if not os.path.isfile(script_file):
            self.log_message(f"Script não encontrado: {script_file}", "ERROR")
            return False
        
        # Verifica arquivos necessários
        for required_file in script_config.get("required_files", []):
            if not os.path.isfile(required_file):
                self.log_message(f"Arquivo necessário não encontrado: {required_file}", "WARNING")
                response = messagebox.askyesno(
                    "Arquivo não encontrado", 
                    f"O arquivo '{required_file}' não foi encontrado.\n\nDeseja continuar mesmo assim?"
                )
                if not response:
                    return False
        
        return True
    
    def run_script_thread(self, script_config):
        """Executa o script em thread separada"""
        try:
            script_file = script_config["file"]
            
            # Comando para executar o script
            cmd = [sys.executable, script_file]
            
            self.log_message(f"Iniciando execução: {script_file}", "INFO")
            self.log_message(f"Comando: {' '.join(cmd)}", "INFO")
            
            # Executa o processo
            self.current_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1,
                cwd=os.path.dirname(script_file) if os.path.dirname(script_file) else None
            )
            
            # Lê output em tempo real
            for line in iter(self.current_process.stdout.readline, ''):
                if not self.is_running:
                    break
                
                line = line.strip()
                if line:
                    # Determina o nível baseado no conteúdo
                    if "ERROR" in line.upper() or "ERRO" in line.upper():
                        level = "ERROR"
                    elif "WARNING" in line.upper() or "AVISO" in line.upper():
                        level = "WARNING"
                    elif "SUCCESS" in line.upper() or "SUCESSO" in line.upper():
                        level = "SUCCESS"
                    else:
                        level = "INFO"
                    
                    self.log_message(line, level)
            
            # Aguarda finalização
            return_code = self.current_process.wait()
            
            if return_code == 0:
                self.log_message("Script executado com sucesso! ✅", "SUCCESS")
                self.root.after(0, lambda: self.status_var.set("✅ Finalizado com sucesso"))
            else:
                self.log_message(f"Script finalizado com código de erro: {return_code}", "ERROR")
                self.root.after(0, lambda: self.status_var.set(f"❌ Erro (código: {return_code})"))
                
        except Exception as e:
            self.log_message(f"Erro durante execução: {e}", "ERROR")
            self.root.after(0, lambda: self.status_var.set(f"❌ Erro: {str(e)}"))
        
        finally:
            # Limpa variáveis e atualiza interface
            self.current_process = None
            self.is_running = False
            self.root.after(0, self.execution_finished)
    
    def start_script(self):
        """Inicia a execução do script selecionado"""
        selected = self.script_var.get()
        
        if not selected:
            messagebox.showwarning("Aviso", "Por favor, selecione um script para executar.")
            return
        
        if selected not in self.scripts_config:
            messagebox.showerror("Erro", "Script selecionado não encontrado na configuração.")
            return
        
        script_config = self.scripts_config[selected]
        
        # Valida o script
        if not self.validate_script(script_config):
            return
        
        # Confirma execução
        response = messagebox.askyesno(
            "Confirmar Execução", 
            f"Deseja executar o script:\n\n{selected}\n\n{script_config['description']}"
        )
        
        if not response:
            return
        
        # Atualiza interface para modo execução
        self.is_running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.progress_bar.start(10)  # Animação da barra
        self.status_var.set("🔄 Executando...")
        
        # Limpa logs anteriores
        self.log_text.delete(1.0, tk.END)
        
        # Inicia thread de execução
        thread = threading.Thread(target=self.run_script_thread, args=(script_config,))
        thread.daemon = True
        thread.start()
    
    def stop_script(self):
        """Para a execução do script"""
        if self.current_process and self.is_running:
            response = messagebox.askyesno(
                "Confirmar Parada", 
                "Deseja realmente parar a execução do script?"
            )
            
            if response:
                self.log_message("Parando execução...", "WARNING")
                self.is_running = False
                
                try:
                    self.current_process.terminate()
                    # Aguarda um pouco e força se necessário
                    time.sleep(2)
                    if self.current_process.poll() is None:
                        self.current_process.kill()
                    
                    self.log_message("Execução interrompida pelo usuário", "WARNING")
                    self.status_var.set("⏹ Interrompido")
                    
                except Exception as e:
                    self.log_message(f"Erro ao parar processo: {e}", "ERROR")
                
                self.execution_finished()
    
    def execution_finished(self):
        """Atualiza interface quando execução termina"""
        self.is_running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.progress_bar.stop()
        
        # Mostra dialog de finalização
        if "sucesso" in self.status_var.get().lower():
            messagebox.showinfo("Execução Concluída", "Script executado com sucesso! ✅")
        elif "erro" in self.status_var.get().lower():
            messagebox.showerror("Execução com Erro", "Script finalizado com erros. ❌\nVerifique os logs para mais detalhes.")
        elif "interrompido" in self.status_var.get().lower():
            messagebox.showwarning("Execução Interrompida", "Script foi interrompido pelo usuário. ⏹")

def main():
    root = tk.Tk()
    
    # Configura tema (opcional)
    try:
        root.tk.call("source", "azure.tcl")
        root.tk.call("set_theme", "light")
    except:
        pass  # Se não conseguir carregar tema personalizado, usa o padrão
    
    app = ScriptLauncher(root)
    root.mainloop()

if __name__ == "__main__":
    main()