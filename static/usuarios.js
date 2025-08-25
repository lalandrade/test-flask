// Função para excluir um usuário
function excluirUsuario(id, cpf) {
    // Pergunta ao usuário se ele tem certeza que quer excluir
    if (!confirm(`Tem certeza que deseja excluir o usuário com CPF ${cpf}?`)) {
        return; // Sai da função se o usuário cancelar
    }

    // Faz a requisição para a rota DELETE do backend
    fetch(`/usuarios/${id}`, {
        method: 'DELETE' // Método HTTP DELETE
    })
    // Captura a resposta da requisição
    .then(response => {
        // Converte a resposta para JSON
        return response.json().then(data => {
            // Se a resposta não for OK, lança um erro
            if (!response.ok) {
                throw new Error(data.erro || "Erro desconhecido")
            }
            // Retorna os dados
            return data;
        });
    })
    // Manipula os dados retornados
    .then(data => {
        alert(data.mensagem) // Mostra mensagem de sucesso
        const linha = document.getElementById('linha-' + id) // Seleciona a linha da tabela
        if (linha) linha.remove(); // Remove a linha da tabela
    })
    // Captura qualquer erro que ocorra na requisição
    .catch(error => {
        console.error("Erro na requisição", error) // Log no console
        alert("Erro ao excluir usuário: " + error.message) // Alerta o usuário
    });
}

// Função para preencher o formulário de atualização com os dados do usuário
function preencherFormulario(button) {
    // Converte os dados do atributo data-usuario de JSON para objeto JS
    var usuario = JSON.parse(button.getAttribute('data-usuario'));
    // Preenche os campos do formulário
    document.getElementById('id').value = usuario.id;
    document.getElementById('nome').value = usuario.nome;
    document.getElementById('email').value = usuario.email;
    document.getElementById('idade').value = usuario.idade;
    document.getElementById('cpf').value = usuario.cpf;
}

// Função para atualizar os dados de um usuário
function atualizarUsuario() {
    // Confirmação com o usuário antes de atualizar
    if (!confirm("Tem certeza que deseja alterar os dados do usuário?")) {
        return; // Sai da função se o usuário cancelar
    }

    // Seleciona o formulário de atualização
    const form = document.getElementById("form-atualizar-usuario");

    // Captura o evento de submit do formulário
    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Impede que a página recarregue

        // Captura os valores dos inputs do formulário
        const id = document.getElementById("id").value;
        const nome = document.getElementById("nome").value;
        const email = document.getElementById("email").value;
        const idade = document.getElementById("idade").value;
        const cpf = document.getElementById("cpf").value;

        // Monta um objeto com os dados do usuário
        const usuario = {
            id: id,
            nome: nome,
            email: email,
            idade: idade,
            cpf: cpf
        };

        // Exibe no console para conferência
        console.log("Usuário atualizado:", usuario);

        // Envia os dados para a rota PUT do backend
        fetch(`/usuarios/`, {
            method: "PUT", // Método HTTP PUT para atualização
            headers: {
                "Content-Type": "application/json" // Tipo de conteúdo JSON
            },
            body: JSON.stringify(usuario) // Converte objeto para JSON
        })
        // Captura a resposta da requisição
        .then(response => {
            response.json() // Converte para JSON
            alert("Usuário atualizado com sucesso!"); // Mensagem de sucesso
            location.reload(); // Recarrega a página para atualizar a tabela
        })
        // Captura erros na requisição
        .catch(error => {
            console.error("Erro ao atualizar:", error) // Log no console
        });
    });
}