document.addEventListener('DOMContentLoaded', function() {
    const roleSelect = document.getElementById('id_role');
    const modal = document.getElementById('admin-modal');
    const confirmBtn = document.getElementById('confirm-btn');
    const cancelBtn = document.getElementById('cancel-btn');

    // Ao mudar a seleção, mostra/esconde o modal
    roleSelect.addEventListener('change', function() {
        if (this.value === 'ADMIN_TEACHER') {
            modal.classList.remove('hidden');
        } else {
            modal.classList.add('hidden');
        }
    });

    // Ao cancelar, volta a seleção para 'Professor'
    cancelBtn.addEventListener('click', function() {
        roleSelect.value = 'REGULAR_TEACHER';
        modal.classList.add('hidden');
    });

    // Ao confirmar, verifica os campos e envia o formulário
    confirmBtn.addEventListener('click', function() {
        const user = document.getElementById('admin_user').value;
        const password = document.getElementById('admin_password').value;
        if (!user || !password) {
            alert('Por favor, insira o usuário e senha de administrador.');
            return;
        }
        // Se tudo ok, fecha o modal e envia o form
        modal.classList.add('hidden');
        // Envia o formulário
        document.querySelector('form').submit();
    });
});