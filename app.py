import os
import sqlite3
from flask import Flask, request, render_template

app = Flask(__name__)

# Configura o caminho correto do banco de dados dentro da pasta database
DATABASE = os.path.join('database', 'scp.db')

def conectar_banco():
    """Abre a conexão com o arquivo do SQLite"""
    conn = sqlite3.connect(DATABASE)
    return conn

@app.route('/')
def pagina_inicial():
    """Esta rota carrega o formulário HTML na tela do navegador"""
    # Importante: O seu arquivo HTML deve estar dentro da pasta 'templates'
    return render_template('index.html')

@app.route('/salvar-projeto', methods=['POST'])
def salvar_projeto():
    """Esta rota recebe os dados enviados pelo formulário e salva no banco"""
    
    # 1. Capturando os textos dos inputs do HTML pelo atributo 'name'
    lider = request.form.get('lider_executante')
    titulo = request.form.get('titulo')
    gerencia_geral = request.form.get('gerencia_geral')
    gerencia = request.form.get('gerencia')
    modalidade = request.form.get('modalidade')
    tipo_atendimento = request.form.get('tipo_atendimento')
    origem_demanda = request.form.get('origem_demanda')
    solicitante = request.form.get('solicitante_responsavel')
    justificativa = request.form.get('justificativa')
    pessoas_adicionais = request.form.get('pessoas_adicionais')
    enfoque = request.form.get('enfoque')
    prioridade = request.form.get('prioridade')
    status = request.form.get('status')
    data_inicial = request.form.get('data_inicial')
    prazo_estimado = request.form.get('prazo_estimado')

    # 2. Tratando os Checkboxes de Coordenação (une as opções marcadas com vírgula)
    lista_coordenacao = request.form.getlist('coordenacao[]')
    coordenacao_string = ", ".join(lista_coordenacao) if lista_coordenacao else None

    # 3. Tratando o arquivo Anexo
    anexo = request.files.get('anexo')
    anexo_path = None
    
    if anexo and anexo.filename != '':
        # Salva o arquivo físico dentro de static/uploads/
        caminho_completo = os.path.join('static', 'uploads', anexo.filename)
        anexo.save(caminho_completo)
        # Guarda apenas o caminho como texto no banco de dados
        anexo_path = caminho_completo

    # 4. Conectando ao banco e executando o comando SQL INSERT
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO projetos (
                lider_executante, titulo, coordenacao, gerencia_geral, gerencia,
                modalidade, tipo_atendimento, origem_demanda, solicitante_responsavel,
                justificativa, pessoas_adicionais, enfoque, prioridade, status,
                data_inicial, prazo_estimado, anexo_path
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            lider, titulo, coordenacao_string, gerencia_geral, gerencia,
            modalidade, tipo_atendimento, origem_demanda, solicitante,
            justificativa, pessoas_adicionais, enfoque, prioridade, status,
            data_inicial, prazo_estimado, anexo_path
        ))
        
        conn.commit()  # Confirma as alterações no banco
        conn.close()   # Fecha a conexão
        
        return "Dados salvos com sucesso no SQLite!", 200

    except Exception as e:
        # Se der qualquer erro no processo, exibe na tela para nos ajudar a identificar
        return f"Erro ao salvar no banco de dados: {str(e)}", 500

if __name__ == '__main__':
    # Roda o servidor em modo de desenvolvimento (atualiza a tela automaticamente se mudar o código)
    app.run(debug=True)