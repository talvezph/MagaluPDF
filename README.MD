# 📖 Manual de Uso - Sistema de Fechamento PDF

## 🎯 Objetivo
Este sistema automatiza o processamento de PDFs de motoristas para gerar fechamentos financeiros em planilhas Excel com fórmulas dinâmicas.

## 🛠️ Instalação

### Pré-requisitos
- Python 3.7+ instalado
- Pip (gerenciador de pacotes Python)

### Passos
1. **Extrair o projeto:**
   ```bash
   unzip projeto_fechamento.zip
   cd projeto_fechamento
   ```

2. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar o sistema:**
   ```bash
   cp exemplos/exemplo_config.ini config.ini
   ```
   Edite o `config.ini` com seus caminhos e valores.

## 📁 Estrutura de Arquivos Necessários

### 1. Pasta de PDFs
```
pdfs/
├── joao_silva.pdf
├── joao_silva2.pdf      # Múltiplos PDFs do mesmo motorista
├── maria_santos.pdf
└── pedro_oliveira.pdf
```

### 2. Planilha de Tipos de Veículos
Excel com as colunas:
- **Nome do Motorista** (ou "Motorista" ou "Nome")
- **Diária Combinada** (ou "Diaria Combinada" ou "Diaria")
- **Tipo de Veículo** (qualquer coluna com "tipo" no nome)

Exemplo:
| Nome do Motorista | Diária Combinada | Tipo de Veículo |
|-------------------|------------------|-----------------|
| JOÃO SILVA        | 120.00          | MOTO           |
| MARIA SANTOS      | 150.00          | CARRO          |
| PEDRO OLIVEIRA    | 140.00          | VAN            |

## 🚀 Usando o Launcher (Recomendado)

### 1. Iniciar o Launcher
```bash
python launcher.py
```

### 2. Interface do Launcher
- **Selecionar Script:** Escolha "Fechamento PDF" no dropdown
- **Descrição:** Aparece automaticamente
- **Executar:** Clique no botão ▶ para iniciar
- **Acompanhar:** Veja logs em tempo real
- **Parar:** Use ⏹ se necessário

### 3. Monitoramento
- **Barra de Progresso:** Mostra que está executando
- **Status:** Indica o estado atual
- **Logs:** Detalhes em tempo real com cores:
  - 🟢 **Verde:** Sucesso
  - 🟡 **Laranja:** Avisos
  - 🔴 **Vermelho:** Erros
  - ⚫ **Preto:** Informações

## 💻 Usando via Linha de Comando

### Comando Básico
```bash
python script_fechamento.py
```

### Com Parâmetros Personalizados
```bash
python script_fechamento.py \
  --pdfs_folder "meus_pdfs/" \
  --type_sheet "minha_planilha.xlsx" \
  --output_excel "resultado_janeiro.xlsx" \
  --error_report "erros_janeiro.log"
```

## 📊 Resultado Gerado

### Planilha Excel com:
- **Uma aba por motorista**
- **13 colunas** com dados e fórmulas
- **Formatação automática:**
  - Cabeçalho em azul claro
  - Linha "Total" em amarelo
- **Fórmulas Excel nativas** que recalculam automaticamente

### Colunas da Planilha:
1. **Data** - Data do registro
2. **Motorista** - Nome do motorista
3. **Tipo de Veículo** - Tipo do veículo
4. **Entregues** - Quantidade de entregas
5. **Insucessos** - Quantidade de insucessos
6. **Valor Entregas** - Valor das entregas
7. **Descontos** - Valor dos descontos
8. **Acréscimo Calculado** - Complemento da diária
9. **Acréscimo Pago** - Acréscimos extraídos do PDF
10. **Recebido** - `=Valor Entregas + Acréscimo Calculado`
11. **Total Dia** - `=Valor Entregas + Acréscimo Pago - Descontos`
12. **Bônus** - Bônus diário quando aplicável
13. **Diferença** - `=Recebido - Total Dia`

## 🔧 Configuração Avançada

### config.ini Detalhado
```ini
[Paths]
# Pasta com PDFs (pode ser relativa ou absoluta)
pdfs_folder = pdfs/

# Planilha de tipos (Excel com .xlsx ou .xls)
type_sheet = tipos_veiculos.xlsx

# Arquivo de saída (será criado/sobrescrito)
output_excel = fechamento_final.xlsx

[Values]
# Valor por entrega (decimal com ponto)
delivery_value = 8.0

# Bônus diário (decimal com ponto)
daily_bonus = 30.0
```

### Personalização de Scripts no Launcher
Edite o `launcher.py` na seção `scripts_config`:

```python
self.scripts_config = {
    "Meu Script Personalizado": {
        "file": "caminho/para/meu_script.py",
        "description": "Descrição do que faz",
        "args": ["--arg1", "--arg2"],
        "required_files": ["arquivo_necessario.txt"]
    }
}
```

## 📈 Dicas de Uso

### 1. Organização de Arquivos
- **Nomes consistentes:** Use nomes similares para PDFs do mesmo motorista
- **Pasta organizada:** Mantenha PDFs em pasta específica
- **Backup:** Faça backup dos PDFs originais

### 2. Múltiplos PDFs por Motorista
- O sistema automaticamente consolida PDFs com nomes similares
- Exemplo: `joao.pdf`, `joao2.pdf`, `joao3.pdf` → Uma aba "JOAO"

### 3. Validação de Dados
- **Verifique logs** para avisos sobre dados não encontrados
- **Confira nomes** na planilha de tipos vs PDFs
- **Valide datas** nos PDFs (formato dd/mm/yyyy)

### 4. Solução de Problemas Comuns
- **Erro "Script não encontrado":** Verifique caminho no config.ini
- **Erro "Planilha não encontrada":** Confirme nome e extensão
- **Motorista não encontrado:** Verifique nome na planilha de tipos
- **Valores zerados:** Verifique formato dos PDFs

## 🆘 Suporte e Logs

### Tipos de Log
- **INFO:** Operações normais
- **WARNING:** Avisos (continuação possível)
- **ERROR:** Erros críticos (interrupção)
- **SUCCESS:** Operações bem-sucedidas

### Arquivo de Erro
- Gerado automaticamente: `error_report.log`
- Contém apenas WARNING e ERROR
- Útil para análise posterior

### Salvando Logs do Launcher
- Use botão "Salvar Logs" na interface
- Escolha local e nome do arquivo
- Formato `.log` ou `.txt`

---

## 🎉 Conclusão

Este sistema oferece uma solução completa para automatizar fechamentos financeiros a partir de PDFs, com interface gráfica amigável e resultados profissionais em Excel.

**Para dúvidas ou problemas, consulte os logs detalhados ou entre em contato com o suporte técnico.**# MagaluPDF
