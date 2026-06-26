// ==============================
// EIRILAR SHIELD - DASHBOARD JS
// ==============================

// 🔴🔵🟢🟡 BLOQUEAR / DESBLOQUEAR / ANALISE
function acao(tipo, id) {
    fetch(`/cliente/${tipo}/${id}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(r => r.json())
    .then(res => {
        alert("Status atualizado: " + res.status);
        location.reload();
    })
    .catch(err => {
        console.error("Erro ação:", err);
        alert("Erro ao executar ação");
    });
}

// 🔵 DETALHES (MODAL COMPLETO)
function detalhes(id) {
    fetch(`/cliente/detalhes/${id}`)
    .then(r => r.json())
    .then(c => {

        const html = `
            <div style="font-size:14px;line-height:1.6">

                <div><b>Nome:</b> ${c.nome}</div>
                <div><b>CPF:</b> ${c.cpf}</div>
                <div><b>Telefone:</b> ${c.telefone}</div>
                <div><b>IP:</b> ${c.ip}</div>
                <div><b>Cidade:</b> ${c.cidade} - ${c.estado}</div>
                <div><b>Score de Risco:</b> ${c.score}</div>

                <hr>

                <div><b>Forma de Pagamento:</b> ${c.forma_pagamento}</div>

                <hr>

                <div>
                    ${c.score >= 70 ? "🔴 Cliente de ALTO risco" :
                      c.score >= 40 ? "🟡 Cliente em análise" :
                      "🟢 Cliente seguro"}
                </div>

            </div>
        `;

        document.getElementById("modalBody").innerHTML = html;

        new bootstrap.Modal(
            document.getElementById("modalCliente")
        ).show();
    })
    .catch(err => {
        console.error("Erro detalhes:", err);
        alert("Erro ao carregar detalhes");
    });
}

// 📞 LIGAR CLIENTE (SIMULAÇÃO OU INTEGRAÇÃO FUTURA)
function ligar(id) {
    fetch(`/cliente/ligar/${id}`, {
        method: "POST"
    })
    .then(r => r.json())
    .then(res => {
        alert("📞 Ligando para: " + res.telefone);
    })
    .catch(err => {
        console.error("Erro ligação:", err);
        alert("Erro ao ligar para cliente");
    });
}

// 🔎 BUSCA (OPCIONAL FUTURO)
function buscarClientes(valor) {
    const cards = document.querySelectorAll(".client-card");

    cards.forEach(card => {
        const texto = card.innerText.toLowerCase();

        if (texto.includes(valor.toLowerCase())) {
            card.style.display = "block";
        } else {
            card.style.display = "none";
        }
    });
}
