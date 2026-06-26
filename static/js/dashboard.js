// ==============================
// EIRILAR SHIELD - DASHBOARD JS FIXED
// ==============================


// ==============================
// 🔧 FETCH BASE
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
    await post(`/cliente/bloquear/${id}`);
    toast("🔴 Cliente bloqueado");

    atualizarBadge(id, "bloqueado");
}


// ==============================
// 🟢 DESBLOQUEAR
// ==============================
async function desbloquear(id) {
    await post(`/cliente/desbloquear/${id}`);
    toast("🟢 Cliente desbloqueado");

    atualizarBadge(id, "ativo");
}


// ==============================
// 🟡 ANÁLISE
// ==============================
async function analise(id) {
    await post(`/cliente/analise/${id}`);
    toast("🟡 Cliente em análise");

    atualizarBadge(id, "analise");
}


// ==============================
// 🔵 DETALHES (MODAL)
// ==============================
async function detalhes(id) {
    const r = await fetch(`/cliente/detalhes/${id}`);
    const c = await r.json();

    const html = `
        <div style="font-size:14px;line-height:1.8">

            <div><b>Nome:</b> ${c.nome || ""}</div>
            <div><b>CPF:</b> ${c.cpf || ""}</div>
            <div><b>Telefone:</b> ${c.telefone || ""}</div>
            <div><b>IP:</b> ${c.ip || ""}</div>
            <div><b>Cidade:</b> ${c.cidade || ""} - ${c.estado || ""}</div>
            <div><b>Score:</b> ${c.score || 0}</div>
            <div><b>Pagamento:</b> ${c.forma_pagamento || ""}</div>

            <hr>

            <b>
                ${
                    (c.score >= 70) ? "🔴 ALTO RISCO" :
                    (c.score >= 40) ? "🟡 MÉDIO RISCO" :
                    "🟢 BAIXO RISCO"
                }
            </b>

        </div>
    `;

    document.getElementById("modalBody").innerHTML = html;

    const modal = new bootstrap.Modal(
        document.getElementById("modalCliente")
    );

    modal.show();
}


// ==============================
// 📞 LIGAR
// ==============================
async function ligar(id) {
    const r = await post(`/cliente/ligar/${id}`);
    toast("📞 Ligando para " + r.telefone);
}


// ==============================
// 🔎 BUSCA
// ==============================
function buscarClientes(valor) {
    document.querySelectorAll(".client-card").forEach(card => {
        card.style.display =
            card.innerText.toLowerCase().includes(valor.toLowerCase())
                ? "block"
                : "none";
    });
}


// ==============================
// 🎯 ATUALIZAR BADGE (VISUAL)
// ==============================
function atualizarBadge(id, status) {
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
// 🔔 TOAST
// ==============================
function toast(msg) {
    const el = document.createElement("div");

    el.innerText = msg;
    el.style.position = "fixed";
    el.style.bottom = "20px";
    el.style.right = "20px";
    el.style.background = "#111";
    el.style.color = "#fff";
    el.style.padding = "12px 16px";
    el.style.borderRadius = "10px";
    el.style.zIndex = 9999;
    el.style.fontSize = "13px";

    document.body.appendChild(el);

    setTimeout(() => el.remove(), 2500);
}
