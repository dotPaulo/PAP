document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("togglePassword");
    const passwordInput = document.getElementById("password");

    toggleBtn.addEventListener("click", function () {
        const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
        passwordInput.setAttribute("type", type);

        // Alterna o ícone entre 👁️ e 🙈
        toggleBtn.textContent = type === "password" ? "👁️" : "🙈";
    });
});