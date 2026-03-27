import sqlite3
import os
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage

# Configurações de Segurança
EMAIL_SENDER = os.environ.get('USER_EMAIL')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

def enviar_email(equipamento, tag, status, dias_restantes, destino):
    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        print(f"⚠️ Simulação: {equipamento} ({tag}) - {dias_restantes} dias para vencer.")
        return

    msg = EmailMessage()
    corpo = (f"ALERTA DE SISTEMA - GESTÃO DE ATIVOS\n\n"
             f"Equipamento: {equipamento}\n"
             f"TAG: {tag}\n"
             f"Status: {status}\n"
             f"Prazo: Faltam {dias_restantes} dias para o vencimento.\n\n"
             f"Favor programar o envio para o laboratório de calibração.")
    
    msg.set_content(corpo)
    msg['Subject'] = f"🚨 [{tag}] Alerta de Calibração - {dias_restantes} dias"
    msg['From'] = EMAIL_SENDER
    msg['To'] = destino

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print(f"✅ E-mail enviado para {destino} (TAG: {tag})")

def inicializar_banco():
    conn = sqlite3.connect('ferramentas.db')
    cursor = conn.cursor()
    # Adicionando a coluna TAG
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS equipamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag TEXT NOT NULL,
            nome TEXT NOT NULL,
            ultima_calibracao DATE NOT NULL,
            periodicidade_meses INTEGER NOT NULL,
            responsavel_email TEXT
        )
    ''')
    
    cursor.execute("SELECT count(*) FROM equipamentos")
    if cursor.fetchone()[0] == 0:
        # Exemplo com TAGs padrão Alcoa
        ferramentas = [
            ('MT-001', 'Multímetro Fluke', '2025-05-25', 12, 'liranatan45@gmail.com'),
            ('MG-005', 'Megômetro', '2025-05-10', 12, 'liranatan45@gmail.com'),
            ('HT-010', 'Comunicador HART', '2024-06-01', 24, 'liranatan45@gmail.com')
        ]
        cursor.executemany('INSERT INTO equipamentos (tag, nome, ultima_calibracao, periodicidade_meses, responsavel_email) VALUES (?,?,?,?,?)', ferramentas)
    conn.commit()
    return conn

def verificar_vencimentos(conn):
    cursor = conn.cursor()
    hoje = datetime.now()
    dia_da_semana = hoje.weekday() # 0 = Segunda, 1 = Terça...
    
    cursor.execute("SELECT tag, nome, ultima_calibracao, periodicidade_meses, responsavel_email FROM equipamentos")
    for tag, nome, ultima, periodicidade, email in cursor.fetchall():
        data_ultimo = datetime.strptime(ultima, '%Y-%m-%d')
        data_vencimento = data_ultimo + timedelta(days=periodicidade * 30)
        dias_restantes = (data_vencimento - hoje).days
        
        # REGRA 1: Entre 60 e 31 dias -> Enviar apenas na Segunda-feira (Semanal)
        if 31 <= dias_restantes <= 60:
            if dia_da_semana == 0: # Segunda-feira
                enviar_email(nome, tag, "ALERTA SEMANAL", dias_restantes, email)
        
        # REGRA 2: Entre 1 e 30 dias -> Enviar a cada 2 dias (Dias pares de dias restantes)
        elif 0 < dias_restantes <= 30:
            if dias_restantes % 2 == 0: # Envia quando faltar 30, 28, 26... dias
                enviar_email(nome, tag, "ALERTA CRÍTICO (2 DIAS)", dias_restantes, email)
        
        # Se dias_restantes <= 0, o alerta para de ser emitido conforme solicitado.
        elif dias_restantes <= 0:
            print(f"ℹ️ {nome} ({tag}) já venceu. Alerta interrompido conforme regra de negócio.")

if __name__ == "__main__":
    conexao = inicializar_banco()
    verificar_vencimentos(conexao)
    conexao.close()
