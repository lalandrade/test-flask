# Importa as bibliotecas necessárias do Flask e módulos padrão do Python
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
import os
import uuid
import bcrypt

# Inicializa a aplicação Flask
app = Flask(__name__)
app.secret_key = "sua_chave_super_secreta"  # chave necessária para sessão

class Usuario:
    def __init__(self, nome, cpf, email, idade, senha,perfil, id=None):
        self.id = id or str(uuid.uuid4())
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.idade = idade
        # senha já é armazenada com hash
        self.senha = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        self.perfil = perfil  # admin ou user

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cpf": self.cpf,
            "email": self.email,
            "idade": self.idade,
            "senha": self.senha,
            "perfil": self.perfil
        }


class UsuarioRepository:
    ARQUIVO = "usuarios.json"

    @classmethod
    def carregar(cls):
        if os.path.exists(cls.ARQUIVO):
            with open(cls.ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    @classmethod
    def salvar(cls, usuarios):
        with open(cls.ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(usuarios, f, indent=4)

    @classmethod
    def adicionar(cls, usuario: Usuario):
        usuarios = cls.carregar()
        usuarios.append(usuario.to_dict())
        cls.salvar(usuarios)

    @classmethod
    def buscar_por_email(cls, email):
        usuarios = cls.carregar()
        for u in usuarios:
            if u["email"] == email:
                return u
        return None

    @classmethod
    def deletar(cls, id):
        usuarios = cls.carregar()
        filtrados = [u for u in usuarios if u["id"] != id]
        if len(usuarios) == len(filtrados):
            return False
        cls.salvar(filtrados)
        return True

    @classmethod
    def atualizar(cls, usuario_edit):
        usuarios = cls.carregar()
        for u in usuarios:
            if u["id"] == usuario_edit.get("id"):
                u.update(usuario_edit)
                cls.salvar(usuarios)
                return True
        return False


# ---------------- ROTAS ---------------- #

@app.route("/")
def home():
    return render_template("cadastro-usuario.html")

@app.route("/login")
def login_get():
    return render_template("login.html")


@app.route("/cadastro-usuario", methods=["POST"])
def cadastrar_usuario():
    usuario = Usuario(
        nome=request.form.get("nome"),
        cpf=request.form.get("cpf"),
        email=request.form.get("email"),
        idade=request.form.get("idade"),
        senha=request.form.get("senha"),
        perfil=request.form.get("perfil")
    )
    UsuarioRepository.adicionar(usuario)
    return f"Usuário '{usuario.nome}' cadastrado com sucesso!"


# ---------- LOGIN / LOGOUT ---------- #
@app.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    senha = request.form.get("senha")

    usuario = UsuarioRepository.buscar_por_email(email)
    if usuario and bcrypt.checkpw(senha.encode("utf-8"), usuario["senha"].encode("utf-8")):
        # salvar sessão
        session["id_usuario"] = usuario["id"]
        session["perfil"] = usuario["perfil"]
        return f"Login realizado com sucesso! Bem-vindo, {usuario['nome']}."
    return "Email ou senha inválidos", 401


@app.route("/logout")
def logout():
    session.clear()
    return "Usuário deslogado!"


# ---------- ROTAS PROTEGIDAS ---------- #
@app.route("/usuarios/json")
def buscar_usuarios_json():
    if "id_usuario" not in session:
        return "Acesso negado. Faça login.", 401
    if session["perfil"] != "admin":
        return "Acesso negado. Área de administração.", 401
    return jsonify(UsuarioRepository.carregar())


@app.route("/usuarios")
def buscar_usuarios():
    if "id_usuario" not in session:
        return "Acesso negado. Faça login.", 401
    if session["perfil"] != "admin":
        return "Acesso negado. Área de administração.", 401
    usuarios = UsuarioRepository.carregar()
    return render_template("usuarios.html", usuarios=usuarios)


@app.route("/usuarios/<id>", methods=["DELETE"])
def excluir_usuario(id):
    # Apenas admin pode deletar
    if session.get("perfil") != "admin":
        return "Acesso negado. Apenas administradores podem deletar usuários.", 403
    if UsuarioRepository.deletar(id):
        return jsonify({"mensagem": "Usuário deletado com sucesso."}), 200
    return jsonify({"erro": "Usuário não encontrado."}), 404


@app.route("/usuarios/", methods=["PUT"])
def atualizar_usuario():
    if "id_usuario" not in session:
        return "Acesso negado. Faça login.", 401

    usuario_edit = request.get_json()
    if UsuarioRepository.atualizar(usuario_edit):
        return jsonify({"mensagem": "Usuário atualizado com sucesso"}), 200
    return jsonify({"erro": "Não foi possível salvar as modificações"}), 404


# Área restrita para admins
@app.route("/admin")
def admin_area():
    if session.get("perfil") != "admin":
        return redirect(url_for("home"))
    return "Área do administrador"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)