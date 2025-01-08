document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.status-change-button').forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            const url = this.getAttribute('data-url');

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Update UI dynamically based on new status
                        const statusElement = document.querySelector(`#status-${data.product_id}`);
                        if (statusElement) {
                            statusElement.innerHTML = data.status_html;
                        }
                    } else {
                        console.error('Failed to update status:', data.error);
                    }
                })
                .catch(error => console.error('Error:', error));
        });
    });
});
