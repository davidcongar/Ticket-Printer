async function get_data(area,id_empresa) {
    try {
        const path = `/pedidos_de_mesa/table_orders_data/${area}/${id_empresa}`;
        const response = await fetch(path);
        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.statusText}`);
        }

        const data = await response.json();
        const container = document.getElementById('container');

        // Clear previous content
        container.innerHTML = "";
        container.className = "grid grid-cols-1 sm:grid-cols-3 gap-6 overflow-y-auto max-h-[calc(100vh-188px)]";

        data.items.forEach((item) => {
            const card = document.createElement('div');
            card.className = "bg-white dark:bg-dark dark:border-gray/20 border-2 border-lightgray/10 p-5 rounded-lg flex flex-col justify-between";

            // --- Top content ---
            const topContent = document.createElement('div');
            const name = document.createElement('h2');
            name.className = "text-lg font-semibold text-gray-900 dark:text-white mb-3 truncate";
            name.textContent = "Mesa 0"+item.numero_de_mesa;
            topContent.appendChild(name);

            const area = document.createElement('h2');
            area.className = "text-sm text-gray-900 dark:text-white mb-3 truncate";
            area.textContent = item.area;
            topContent.appendChild(area);

            const comensales = document.createElement('div');
            comensales.className = "flex items-center gap-2 p-2";

            comensales.innerHTML = `
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none"
                    xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="6" r="4" stroke="currentColor" stroke-width="1.5"/>
                    <path d="M18 9C19.6569 9 21 7.88071 21 6.5C21 5.11929 19.6569 4 18 4"
                        stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                    <path d="M6 9C4.34315 9 3 7.88071 3 6.5C3 5.11929 4.34315 4 6 4"
                        stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                    <ellipse cx="12" cy="17" rx="6" ry="4" stroke="currentColor" stroke-width="1.5"/>
                    <path d="M20 19C21.7542 18.6153 23 17.6411 23 16.5C23 15.3589 21.7542 14.3847 20 14"
                        stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                    <path d="M4 19C2.24575 18.6153 1 17.6411 1 16.5C1 15.3589 2.24575 14.3847 4 14"
                        stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
                <span>${item.numero_de_comensales}</span>
            `;
            topContent.appendChild(comensales);
            const tiempo = document.createElement('div');
            tiempo.className = "flex items-center gap-2 p-2";

            tiempo.innerHTML = `
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.5"/>
                <path d="M12 8V12L14.5 14.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>${item.tiempo}</span>
            `;
            topContent.appendChild(tiempo);

            card.appendChild(topContent);
            // --- Bottom content ---
            const bottomContent = document.createElement('div');
            bottomContent.className = "mt-6 flex items-center justify-between gap-6";

            const order_button = document.createElement('button');
            order_button.type = "button";
            order_button.textContent = "Ordenar";
            order_button.className = "btn h-[52px] uppercase flex-1 bg-primary border border-primary rounded-md text-white transition-all duration-300 hover:bg-primary/[0.85] hover:border-primary/[0.85]"
            order_button.addEventListener("click", () => {
                window.location.href = `/pedidos_de_mesa/add_items/${item.id}`;
            });
            const close_button = document.createElement('button');
            close_button.type = "button";
            close_button.textContent = "Cuenta";
            close_button.className = "btn  h-[52px] uppercase flex-1 bg-success border border-success rounded-md text-white transition-all duration-300 hover:bg-success/[0.85] hover:border-success/[0.85]"
            close_button.addEventListener("click", () => {
                window.location.href = `/pedidos_de_mesa/invoice/${item.id}`;
            });
            bottomContent.appendChild(order_button);
            bottomContent.appendChild(close_button);
            card.appendChild(bottomContent);
            container.appendChild(card);
        });
    } catch (error) {
        console.error("Error fetching or processing data:", error);
        return null;
    }
}

get_data('todas',id_empresa);
