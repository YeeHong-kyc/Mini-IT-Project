// Main JavaScript for Tracker

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // QR code download button enhancement
    document.querySelectorAll('.download-qr').forEach(button => {
        button.addEventListener('click', function() {
            const itemName = this.dataset.itemName;
            this.textContent = 'Downloading...';
            setTimeout(() => {
                this.textContent = 'Download QR Code';
            }, 2000);
        });
    });

    // Scan history table sorting
    const sortTable = (table, column, asc = true) => {
        const dirModifier = asc ? 1 : -1;
        const tBody = table.tBodies[0];
        const rows = Array.from(tBody.querySelectorAll('tr'));

        const sortedRows = rows.sort((a, b) => {
            const aColText = a.querySelector(`td:nth-child(${column + 1})`).textContent.trim();
            const bColText = b.querySelector(`td:nth-child(${column + 1})`).textContent.trim();

            return aColText > bColText ? (1 * dirModifier) : (-1 * dirModifier);
        });

        while (tBody.firstChild) {
            tBody.removeChild(tBody.firstChild);
        }

        tBody.append(...sortedRows);

        table.querySelectorAll('th').forEach(th => th.classList.remove('th-sort-asc', 'th-sort-desc'));
        table.querySelector(`th:nth-child(${column + 1})`).classList.toggle('th-sort-asc', asc);
        table.querySelector(`th:nth-child(${column + 1})`).classList.toggle('th-sort-desc', !asc);
    };

    document.querySelectorAll('.sortable th').forEach(headerCell => {
        headerCell.addEventListener('click', () => {
            const tableElement = headerCell.parentElement.parentElement.parentElement;
            const headerIndex = Array.prototype.indexOf.call(headerCell.parentElement.children, headerCell);
            const currentIsAsc = headerCell.classList.contains('th-sort-asc');

            sortTable(tableElement, headerIndex, !currentIsAsc);
        });
    });
});