import sqlite3
import os
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage

# Configurações de Segurança (Lendo do GitHub Secrets)
EMAIL_SENDER = os.environ.get('USER_EMAIL')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

def enviar_email(equipamento, status, data_venc, destino):
    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        print(f"⚠️ Simulação: E-mail para {destino} sobre {equipamento}")
        return

    msg = EmailMessage()
    msg.set_content(f"Olá,\n\nEste é um alerta automático do sistema de manutenção.\n\n"
                    f"O equipamento: {equipamento}\n"
                    f"Status: {status}\n"
                    f"Data de Vencimento: {data_venc}\n\n"
                    f"Favor providenciar a calibração imediatamente.")
    
    msg['Subject'] = f"🚨 ALERTA DE CALIBRAÇÃO: {equipamento}"
    msg['From'] = EMAIL_SENDER
    msg['To'] = destino

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print(f"✅ E-mail enviado com sucesso para {destino}")
    except Exception as e:
        print(f"❌ Erro ao enviar e-mail: {e}")

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
    
    cursor.execute("SELECT count(*) FROM equipamentos")
    if cursor.fetchone()[0] == 0:
        # Datas ajustadas para 2025 para gerar alertas em 2026
        ferramentas = [
            ('Multímetro Fluke', '2025-05-15', 12, 'liranatan45@gmail.com'),
            ('Megômetro', '2025-01-10', 12, 'liranatan45@gmail.com'),
            ('Comunicador HART', '2024-03-01', 24, 'liranatan45@gmail.com'),
            ('Terrômetro', '2025-02-15', 12, 'liranatan45@gmail.com')
        ]
        cursor.executemany('INSERT INTO equipamentos (nome, ultima_calibracao, periodicidade_meses, responsavel_email) VALUES (?,?,?,?)', ferramentas)
    conn.commit()
    return conn

def verificar_vencimentos(conn):
    cursor = conn.cursor()
    hoje = datetime.now()
    alerta_periodo = hoje + timedelta(days=60)
    
    cursor.execute("SELECT nome, ultima_calibracao, periodicidade_meses, responsavel_email FROM equipamentos")
    for nome, ultima, periodicidade, email in cursor.fetchall():
        data_ultimo = datetime.strptime(ultima, '%Y-%m-%d')
        data_vencimento = data_ultimo + timedelta(days=periodicidade * 30)
        
        status = ""
        if hoje > data_vencimento:
            status = "VENCIDO"
        elif hoje <= data_vencimento <= alerta_periodo:
            status = "PRÓXIMO AO VENCIMENTO"
            
        if status:
            enviar_email(nome, status, data_vencimento.strftime('%d/%m/%Y'), email)

if __name__ == "__main__":
    conexao = inicializar_banco()
    verificar_vencimentos(conexao)
    conexao.close()
