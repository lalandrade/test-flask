# Importa as bibliotecas necessárias do Flask e módulos padrão do Python
from flask import Flask, render_template, request, jsonify
import json  # Para manipulação de arquivos JSON
import os    # Para verificar existência de arquivos
import uuid  # Para gerar IDs únicos para usuários

# Cria a aplicação Flask
app = Flask(__name__)

# Função para carregar os usuários do arquivo JSON
def carregar_usuarios():
    # Tenta verificar se o arquivo 'usuarios.json' existe e lê os dados
    try:
        if os.path.exists("usuarios.json"):  # Verifica existência do arquivo
            with open("usuarios.json", "r", encoding="utf-8") as arquivo:
                return json.load(arquivo)  # Retorna a lista de usuários
        else:
            return []  # Retorna lista vazia se o arquivo não existir
    except:
        return []  # Retorna lista vazia em caso de erro na leitura

# Função para salvar um novo usuário no arquivo JSON
def salvar_usuario(usuario):
    # Carrega os usuários existentes
    usuarios = carregar_usuarios()

    try:
        # Adiciona o novo usuário à lista
        usuarios.append(usuario)

        # Salva a lista atualizada no arquivo 'usuarios.json'
        with open("usuarios.json", "w", encoding="utf-8") as arquivo:
            json.dump(usuarios, arquivo, indent=4)

        return True  # Retorna True se o salvamento foi bem-sucedido
    except:
        return False  # Retorna False em caso de erro ao salvar

# Função para deletar um usuário pelo ID
def deletar_usuario(id):
    usuarios = carregar_usuarios()  # Carrega usuários existentes
    usuarios_filtrados = [u for u in usuarios if u.get("id") != id]  # Remove usuário com o ID fornecido

    # Verifica se algum usuário foi removido
    if len(usuarios) == len(usuarios_filtrados):
        return False  # Nenhum usuário removido

    try:
        # Salva a lista filtrada no arquivo JSON
        with open("usuarios.json", "w", encoding="utf-8") as arquivo:
            json.dump(usuarios_filtrados, arquivo, indent=4)
        return True  # Retorna True se deletado com sucesso
    except:
        return False  # Retorna False em caso de erro ao salvar

# Rota principal, renderiza a página inicial com formulário de cadastro
@app.route("/")
def home():
    return render_template("cadastro-usuario.html")

# Rota para cadastrar usuário via formulário HTML (POST)
@app.route("/cadastro-usuario", methods=["POST"])
def cadastrar_usuario():
    # Recupera os dados enviados pelo formulário
    nome = request.form.get("nome")
    cpf = request.form.get("cpf")
    email = request.form.get("email")
    idade = request.form.get("idade")
    senha = request.form.get("senha")

    # Cria um dicionário com os dados do usuário, incluindo um ID único
    usuario = {
        "id": str(uuid.uuid4()),
        "nome": nome,
        "cpf": cpf,
        "email": email,
        "idade": idade,
        "senha": senha,
    }

    # Tenta salvar o usuário no arquivo JSON
    status = salvar_usuario(usuario)

    # Retorna mensagem de sucesso ou erro
    if status:
        return f"Usuário '{usuario['nome']}' cadastrado com sucesso!"
    else:
        return "Não foi possível cadastrar o usuário"

# Rota para retornar todos os usuários em formato JSON
@app.route("/usuarios/json")
def buscar_usuarios_json():
    usuarios = carregar_usuarios()  # Carrega usuários do arquivo
    return jsonify(usuarios)  # Retorna JSON

# Rota para exibir todos os usuários em uma página HTML
@app.route("/usuarios")
def buscar_usuarios():
    usuarios = carregar_usuarios()  # Carrega usuários do arquivo
    return render_template("usuarios.html", usuarios=usuarios)  # Renderiza template com lista de usuários

# Rota para deletar usuário pelo ID via requisição DELETE
@app.route("/usuarios/<id>", methods=["DELETE"])
def excluir_usuario(id):
    sucesso = deletar_usuario(id)  # Tenta deletar usuário

    if sucesso:
        return jsonify({"mensagem": f"Usuário deletado com sucesso."}), 200  # Retorna sucesso
    else:
        return jsonify({"erro": "Usuário não encontrado."}), 404  # Retorna erro se usuário não existe

# Rota para atualizar um usuário via requisição PUT
@app.route("/usuarios/", methods=["PUT"])
def atualizar_usuario():   
    usuario_edit = request.get_json()  # Captura dados enviados em JSON
    usuarios = carregar_usuarios()     # Carrega lista de usuários existente

    # Procura usuário pelo ID e atualiza os dados
    for usuario in usuarios:
        if usuario.get("id") == usuario_edit.get("id"):
            usuario.update(usuario_edit)
            break
        
    try:
        # Salva a lista atualizada no arquivo JSON
        with open("usuarios.json", "w", encoding="utf-8") as arquivo:
            json.dump(usuarios, arquivo, indent=4)

        return jsonify({"mensagem": "Usuário atualizado com sucesso"}), 200  # Sucesso
    except:
        return jsonify({"erro": "Não foi possível salvar as modificações"}), 404  # Erro ao salvar

# Executa o servidor Flask em modo debug
if __name__ == '__main__':
    app.run(debug=True)