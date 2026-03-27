import sqlite3
from datetime import datetime, timedelta

# Configuração de e-mails fictícios para os responsáveis
RESPONSAVEIS = ["liranatan45@gmail.com", "oficina.eletrica@exemplo.com"]

def inicializar_banco():
    conn = sqlite3.connect('ferramentas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS equipamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            ultima_calibracao DATE NOT NULL,
            periodicidade_meses INTEGER NOT NULL,
            responsavel_email TEXT
        )
    ''')
    
    # Inserindo dados de exemplo se o banco estiver vazio
    cursor.execute("SELECT count(*) FROM equipamentos")
    if cursor.fetchone()[0] == 0:
        ferramentas = [
            ('Multímetro Fluke', '2025-05-15', 12, RESPONSAVEIS[0]), # Vence em 2 meses!
            ('Megômetro', '2025-01-15', 12, RESPONSAVEIS[1]),        # Já venceu!
            ('Comunicador HART', '2025-03-01', 24, RESPONSAVEIS[0]),
            ('Medidor Portátil de Vazão', '2025-04-20', 12, RESPONSAVEIS[1]),
            ('Terrômetro', '2025-02-15', 12, RESPONSAVEIS[0])
        ]
        cursor.executemany('INSERT INTO equipamentos (nome, ultima_calibracao, periodicidade_meses, responsavel_email) VALUES (?,?,?,?)', ferramentas)
    
    conn.commit()
    return conn

def verificar_vencimentos(conn):
    cursor = conn.cursor()
    hoje = datetime.now()
    alerta_periodo = hoje + timedelta(days=60) # Janela de 2 meses para o alerta
    
    cursor.execute("SELECT nome, ultima_calibracao, periodicidade_meses, responsavel_email FROM equipamentos")
    for nome, ultima, periodicidade, email in cursor.fetchall():
        data_ultimo = datetime.strptime(ultima, '%Y-%m-%d')
        # Calcula a data do próximo vencimento
        data_vencimento = data_ultimo + timedelta(days=periodicidade * 30)
        
        if hoje <= data_vencimento <= alerta_periodo:
            print(f"⚠️ ALERTA: O equipamento '{nome}' vence em {data_vencimento.strftime('%d/%m/%Y')}.")
            print(f"   Encaminhando alerta para: {email}")
        elif hoje > data_vencimento:
            print(f"❌ CRÍTICO: O equipamento '{nome}' está com a calibração VENCIDA desde {data_vencimento.strftime('%d/%m/%Y')}!")

if __name__ == "__main__":
    conexao = inicializar_banco()
    verificar_vencimentos(conexao)
    conexao.close()
