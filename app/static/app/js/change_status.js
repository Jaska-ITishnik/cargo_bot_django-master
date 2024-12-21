document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".change-status").forEach(function (link) {
        link.addEventListener("click", function (event) {
            event.preventDefault();  // Prevent the default action

            const productId = this.dataset.id;
            const field = this.dataset.field;
            const value = this.dataset.value === "true";

            fetch("{% url 'change_product_status' %}", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": "{{ csrf_token }}",
                },
                body: JSON.stringify({product_id: productId, field: field, value: !value}),
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.success) {
                        // Update button text and style
                        this.textContent = value ? "Kelgan" : "Kelmagan";
                        this.style.backgroundColor = value ? "#9f0000" : "#00ff00";
                        this.dataset.value = !value;
                    } else {
                        alert("Failed to update status.");
                    }
                })
                .catch((error) => console.error("Error:", error));
        });
    });
});
