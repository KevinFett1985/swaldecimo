document.addEventListener('keyup', e => {
    if (e.target.matches('#buscador')) {
        const searchTerm = e.target.value.trim().toLowerCase();

        // Buscar en la tabla si existe
        const table = document.querySelector('.tabla');
        if (table) {
            const tableRows = table.querySelectorAll('tbody tr');
            tableRows.forEach(row => {
                let rowVisible = false;
                Array.from(row.cells).forEach(cell => {
                    const cellContent = cell.textContent.trim().toLowerCase();
                    if (cellContent.includes(searchTerm)) {
                        rowVisible = true;
                    }
                });
                row.style.display = rowVisible ? '' : 'none';
            });
        }

        // Buscar en las tarjetas
        const cards = document.querySelectorAll('.card');
        cards.forEach(card => {
            const cardContent = card.querySelector('.card-body').textContent.toLowerCase();
            const matches = cardContent.includes(searchTerm);
            card.style.display = matches ? '' : 'none';
        });
    }
});
