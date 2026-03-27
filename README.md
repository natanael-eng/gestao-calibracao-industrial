# 🛠️ Sistema de Gestão de Calibração Industrial (SMC)

[![Verificação Semanal de Calibração](https://github.com/natanael-eng/gestao-calibracao-industrial/actions/workflows/checar-calibracao.yml/badge.svg)](https://github.com/natanael-eng/gestao-calibracao-industrial/actions/workflows/checar-calibracao.yml)

## 📌 Sobre o Projeto
Este sistema foi desenvolvido para automatizar o controle de calibração de instrumentos industriais (Multímetros, Megômetros, HART, etc.), eliminando falhas humanas no acompanhamento de prazos e garantindo a conformidade com as normas de qualidade e segurança.

O sistema utiliza **Python** e **SQLite** para gerenciar os dados e o **GitHub Actions** para realizar auditorias automáticas diárias sem necessidade de intervenção manual.

## 🚀 Funcionalidades e Regras de Negócio
O sistema possui uma lógica de alertas progressivos baseada na criticidade do prazo:

* **Fase 1 (60 a 31 dias):** Alertas semanais informando a proximidade do vencimento.
* **Fase 2 (30 a 1 dia):** Alertas críticos a cada 48 horas para agilizar o envio ao laboratório.
* **Gestão de TAGs:** Identificação precisa por TAG do ativo e e-mail direto do responsável.
* **Segurança:** Interrupção automática de notificações após o vencimento (sinal de bloqueio de uso).

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3.10
* **Banco de Dados:** SQLite (Armazenamento leve e eficiente)
* **Automação (DevOps):** GitHub Actions (Execução agendada via Cron)
* **Comunicação:** Protocolo SMTP para alertas reais por e-mail.
* **Segurança de Dados:** Uso de GitHub Secrets para proteção de credenciais.

## 📈 Impacto na Manutenção
* **Zero Riscos:** Evita o uso de instrumentos fora da validade.
* **Produtividade:** Redução de horas gastas em conferência manual de planilhas.
* **Proatividade:** Antecipação de gargalos no laboratório de calibração.

---
**Desenvolvido por Natanael Lira Ferreira** *Manutenção Industrial | Engenharia de Software*
