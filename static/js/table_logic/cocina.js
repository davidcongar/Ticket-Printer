async function get_data() {
    try {
        const path = `/cocina/data`;
        const response = await fetch(path);
        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.statusText}`);
        }

        const data = await response.json();
        const order_container = document.getElementById('order_container');
        const order_count = document.getElementById('order_count');

        // Clear any previous content
        order_container.innerHTML = "";
        order_count.innerHTML = "";
        let count = 0;

        data['items'].forEach((item, index) => {
            // Create wrapper div
            const wrapper = document.createElement('div');
            wrapper.className = "bg-white dark:bg-dark dark:border-gray/20 border-2 border-lightgray/10 rounded-lg overflow-hidden my-3 w-full max-w-xl";

            // Header
            const header = document.createElement('div');
            header.className = "flex bg-white dark:bg-dark items-center border-b border-lightgray/10 dark:border-gray/20 justify-between px-5 py-3";

            header.innerHTML = `
                <div class="space-y-1">
                    <h5 class="font-semibold text-lg">
                        Orden: <span>${item.orden}</span>
                    </h5>                        
                    <h1 class="font-normal text-sm">
                        Canal de venta: <span>${item.canal ? item.canal : ""}</span>
                    </h1>
                    <h1 class="font-normal text-sm">
                        Notas: <span>${item.notas ? item.notas : ""}</span>
                    </h1>
                </div>
            `;

            // Content
            const content = document.createElement('div');
            content.className = "p-5 space-y-4";

            // Create table
            const table = document.createElement("table");
            table.className = "overflow-auto w-full table-striped";
            table.id = `modal_content_${index}`;
            table.innerHTML = `
                <thead>
                    <tr>
                        <th>Producto</th>
                        <th>Notas</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody></tbody>
            `;

            const tbody = table.querySelector("tbody");

            // Add rows with buttons
            item.productos.forEach(prod => {
                const tr = document.createElement("tr");

                tr.innerHTML = `
                    <td>${prod.cantidad} X ${prod.nombre}</td>
                    <td style="white-space: normal;">${prod.comensal},${prod.complementos},${prod.modificaciones.replace(/[{}"]/g, '').split(',').map(s => s.trim()).join(', ')},${prod.notas}</td>
                `;

                // Add button cell
                const tdBtn = document.createElement("td");
                const button = document.createElement("button");
                button.type = "button";
                button.textContent = "Preparado";
                button.className =
                    "btn border text-primary border-transparent rounded-md transition-all duration-300 hover:text-white hover:bg-primary bg-primary/10";

                button.addEventListener("click", async (e) => {
                    e.preventDefault();
                    if (item.canal && item.canal.includes("Mesa")) {
                        await fetch(`/cocina/item_prepared/pedido_de_mesas/${encodeURIComponent(prod.id)}`);
                    } else {
                        await fetch(`/cocina/item_prepared/orden_de_venta/${encodeURIComponent(prod.id)}`);
                    }
                    get_data();
                });

                tdBtn.appendChild(button);
                tr.appendChild(tdBtn);

                tbody.appendChild(tr);
            });

            content.appendChild(table);

            // Assemble card
            wrapper.appendChild(header);
            wrapper.appendChild(content);

            // Append to container
            order_container.appendChild(wrapper);
            count = count + 1;
        });

        order_count.innerHTML = count;

    } catch (error) {
        console.error("Error fetching or processing data:", error);
        return null;
    }
}

get_data();
setInterval(get_data, 10000);
