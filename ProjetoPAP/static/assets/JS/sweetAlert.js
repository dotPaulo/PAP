document.addEventListener('DOMContentLoaded', function () {
    // Mostrar mensagens com SweetAlert se existirem no DOM
    const alertBox = document.getElementById('swal-messages');
    if (alertBox) {
        const type = alertBox.dataset.type;
        const message = alertBox.dataset.message;

        if (type && message) {
            Swal.fire({
                icon: type === 'success' ? 'success' : 'error',
                title: message,
                timer: 2000,
                showConfirmButton: false
            });
        }
    }

    // Confirmação antes de deletar o filme
    const deleteForm = document.getElementById('delete-movie-form');

    if (deleteForm) {
        deleteForm.addEventListener('submit', function (e) {
            e.preventDefault();

            Swal.fire({
                title: 'Tem certeza?',
                text: 'Essa ação irá deletar permanentemente o filme.',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#d33',
                cancelButtonColor: '#6c757d',
                confirmButtonText: 'Sim, deletar!',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) {
                    deleteForm.submit();
                }
            });
        });
    }
});
