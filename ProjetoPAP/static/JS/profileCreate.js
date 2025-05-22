const form = document.getElementById("profileForm");
  const roleSelect = document.getElementById("id_role");
  const modal = document.getElementById("adminModal");
  const adminPasswordInput = document.getElementById("adminPassword");
  const errorMsg = document.getElementById("adminError");

  form.addEventListener("submit", function(e) {
    if (roleSelect.value === "Administrador") {
      e.preventDefault(); // Impede o envio até validar
      modal.classList.remove("hidden");
    }
  });

  function closeModal() {
    modal.classList.add("hidden");
    adminPasswordInput.value = '';
    errorMsg.classList.add("hidden");
  }

  function verifyPassword() {
    const senha = adminPasswordInput.value;

    fetch("{% url 'verificar_admin' %}", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": "{{ csrf_token }}"
      },
      body: new URLSearchParams({ senha: senha })
    })
    .then(res => res.json())
    .then(data => {
      if (data.status === "ok") {
        modal.classList.add("hidden");
        form.submit();
      } else {
        errorMsg.textContent = data.mensagem;
        errorMsg.classList.remove("hidden");
      }
    });
  }