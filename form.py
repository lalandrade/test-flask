from flask import Flask, render_template, request, jsonify
import json, os

app = Flask(__name__)

# Função para carregar usuários
def carregar_usuarios():
    try:
        if os.path.exists("usuarios.json"):
            with open("usuarios.json", "r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        else:
            return []
    except Exception as erro:
        print(f"Erro ao carregar os usuários: {erro}")
        return []

# Função para salvar usuários
def salvar_usuarios(usuario):
    usuarios = carregar_usuarios()
    try:
        usuarios.append(usuario)
        with open("usuarios.json", "w", encoding="utf-8") as arquivo:
            json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)
        return True
    except Exception as erro:
        print(f"Erro ao salvar usuário: {erro}")
        return False

@app.route("/")
def home():
    return render_template("cadastro_usuario.html")

@app.route("/cadastro-usuario.html", methods=["POST"])
def cadastro_usuario():
    nome = request.form.get("nome")
    email = request.form.get("email")
    idade = request.form.get("idade")
    senha = request.form.get("senha")

    usuario = {"nome": nome, "email": email, "idade": idade, "senha": senha}
    status = salvar_usuarios(usuario)

    if status:
        return "Usuário cadastrado com sucesso!"
    else:
        return "Erro ao cadastrar o usuário!"

# Rota para retornar todos os usuários em JSON
@app.route("/usuarios-json")
def usuarios_json():
    usuarios = carregar_usuarios()
    return jsonify(usuarios)

# Rota para exibir todos os usuários em uma tabela HTML
@app.route("/usuarios-html")
def usuarios_html():
    usuarios = carregar_usuarios()
    return render_template("usuarios.html", usuarios=usuarios)

if __name__ == "__main__":
    app.run(debug=True)
