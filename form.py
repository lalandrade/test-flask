from flask import Flask, render_template, request, jsonify
import json
import os
import uuid

app = Flask(__name__)

def carregar_usuarios():
    # Verifica se o arquivo 'usuarios.json' existe e carrega os dados
    try:
        if os.path.exists("usuarios.json"):
            with open("usuarios.json", "r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        else:
            return []  # Retorna uma lista vazia se o arquivo não existir
    except:
        return []  # Retorna uma lista vazia se ocorrer algum erro ao ler o arquivo
    
def salvar_usuario(usuario):
    # Carrega os usuários existentes
    usuarios = carregar_usuarios()

    try:
        # Adiciona o novo usuário à lista
        usuarios.append(usuario)

        # Salva a lista atualizada de usuários no arquivo 'usuarios.json'
        with open("usuarios.json", "w", encoding="utf-8") as arquivo:
            json.dump(usuarios, arquivo, indent=4)

        return True  # Retorna True se o salvamento for bem-sucedido
    except:
        return False  # Retorna False se ocorrer um erro ao salvar

def deletar_usuario(id):
    usuarios = carregar_usuarios()
    usuarios_filtrados = [u for u in usuarios if u.get("id") != id]

    if len(usuarios) == len(usuarios_filtrados):
        return False  # Nenhum usuário foi removido

    try:
        with open("usuarios.json", "w", encoding="utf-8") as arquivo:
            json.dump(usuarios_filtrados, arquivo, indent=4)
        return True
    except:
        return False

@app.route("/")
def home():
    # Renderiza a página inicial com o formulário de cadastro
    return render_template("cadastro-usuario.html")

@app.route("/cadastro-usuario", methods=["POST"])
def cadastrar_usuario():
    # Recupera os dados enviados pelo formulário HTML
    nome = request.form.get("nome")
    cpf = request.form.get("cpf")
    email = request.form.get("email")
    idade = request.form.get("idade")
    senha = request.form.get("senha")

    # Cria um dicionário com os dados do novo usuário
    usuario = {
        "id": str(uuid.uuid4()),
        "nome": nome,
        "cpf": cpf,
        "email": email,
        "idade": idade,
        "senha": senha,
    }

    # Tenta salvar o novo usuário no arquivo JSON
    status = salvar_usuario(usuario)

    # Verifica se o usuário foi salvo com sucesso e retorna a mensagem adequada
    if status:
        return f"Usuário '{usuario['nome']}' cadastrado com sucesso!"
    else:
        return "Não foi possível cadastrar o usuário"

@app.route("/usuarios/json")
def buscar_usuarios_json():
    usuarios = carregar_usuarios()
    return jsonify(usuarios)

@app.route("/usuarios")
def buscar_usuarios():
    usuarios = carregar_usuarios()
    return render_template("usuarios.html", usuarios=usuarios)

@app.route("/usuarios/<id>", methods=["DELETE"])    
def excluir_usuario(id):
    sucesso = deletar_usuario(id)

    if sucesso:
        return jsonify({"mensagem": f"Usuário deletado com sucesso."}), 200
    else:
        return jsonify({"erro": "Usuário não encontrado."}), 404

if __name__ == '__main__':
    app.run(debug=True)