// ==============================
// EIRILAR SHIELD - DASHBOARD JS
// VERSÃO PROFISSIONAL
// ==============================


// ==============================
// 🔧 HELPER FETCH POST
// ==============================
async function post(url) {
    const r = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
    });

    return r.json();
}


// ==============================
// 🔴 BLOQUEAR
// ==============================
async function bloquear(id) {
    const res = await post(`/cliente/bloquear/${id}`);

    toast("🔴 Cliente bloqueado");
    atualizarStatusLocal(id, "bloqueado");
}


// ==============================
// 🟢 DESBLOQUEAR
// ==============================
async function desbloquear(id) {
    const res = await post(`/cliente/desbloquear/${id}`);

    toast("🟢 Cliente desbloqueado");
    atualizarStatusLocal(id, "ativo");
}


// ==============================
// 🟡 EM ANÁLISE
// ==============================
async function analise(id) {
    const res = await post(`/cliente/analise/${id}`);

    toast("🟡 Cliente em análise");
    atualizarStatusLocal(id, "analise");
}


// ==============================
// 🔵 DETALHES (MODAL PROFISSIONAL)
// ==============================
async function detalhes(id) {
    const r = await fetch(`/cliente/detalhes/${id}`);
    const c = await r.json();

    const html = `
        <div style="font-size:14px;line-height:1.8">

            <p><b>Nome:</b> ${c.nome}</p>
            <p><b>CPF:</b> ${c.cpf}</p>
            <p><b>Telefone:</b> ${c.telefone}</p>
            <p><b>IP:</b> ${c.ip}</p>
            <p><b>Cidade:</b> ${c.cidade} - ${c.estado}</p>
            <p><b>Score:</b> ${c.score}</p>
            <p><b>Pagamento:</b> ${c.forma_pagamento}</p>

            <hr>

            <h6>
                ${
                    c.score >= 70 ? "🔴 ALTO RISCO" :
                    c.score >= 40 ? "🟡 MÉDIO RISCO" :
                    "🟢 BAIXO RISCO"
                }
            </h6>
        </div>
    `;

    document.getElementById("modalBody").innerHTML = html;

    const modal = new bootstrap.Modal(
        document.getElementById("modalCliente")
    );

    modal.show();
}


// ==============================
// 📞 LIGAR CLIENTE
// ==============================
async function ligar(id) {
    const res = await post(`/cliente/ligar/${id}`);

    toast("📞 Ligando para " + res.telefone);
}


// ==============================
// 🔎 BUSCA CLIENTES
// ==============================
function buscarClientes(valor) {
    document.querySelectorAll(".client-card").forEach(card => {
        card.style.display = card.innerText.toLowerCase()
            .includes(valor.toLowerCase()) ? "block" : "none";
    });
}


// ==============================
// 🔁 ATUALIZA STATUS VISUAL SEM RELOAD
// ==============================
function atualizarStatusLocal(id, status) {
    const card = document.querySelector(`[data-id="${id}"]`);

    if (!card) return;

    const badge = card.querySelector(".badge");

    if (!badge) return;

    if (status === "bloqueado") {
        badge.className = "badge bg-danger";
        badge.innerText = "Bloqueado";
    }

    if (status === "ativo") {
        badge.className = "badge bg-success";
        badge.innerText = "Ativo";
    }

    if (status === "analise") {
        badge.className = "badge bg-warning text-dark";
        badge.innerText = "Análise";
    }
}


// ==============================
// 🔔 TOAST SIMPLES (UI PROFISSIONAL)
// ==============================
function toast(msg) {

    let el = document.createElement("div");

    el.innerText = msg;

    el.style.position = "fixed";
    el.style.bottom = "20px";
    el.style.right = "20px";
    el.style.background = "#111";
    el.style.color = "#fff";
    el.style.padding = "12px 16px";
    el.style.borderRadius = "10px";
    el.style.zIndex = 9999;

    document.body.appendChild(el);

    setTimeout(() => el.remove(), 2500);
}
