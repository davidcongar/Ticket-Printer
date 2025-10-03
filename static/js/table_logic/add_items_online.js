async function get_data(categoria,id_pedido) {
    try {
        const path = `/pedidos_en_linea/menu_data/${categoria}/${id_pedido}`;
        const response = await fetch(path);
        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.statusText}`);
        }

        const data = await response.json();
        const container = document.getElementById('container');

        // Clear previous content
        container.innerHTML = "";
        container.className = "grid grid-cols-1 sm:grid-cols-3 gap-6 p-4";

        data.items.forEach((item) => {
            const card = document.createElement('div');
            card.className = "bg-white dark:bg-dark dark:border-gray/20 border-2 border-lightgray/10 p-5 rounded-lg flex flex-col justify-between";

            // --- Top content ---
            const topContent = document.createElement('div');

            const name = document.createElement('h2');
            name.className = "text-lg font-semibold text-gray-900 dark:text-white mb-3 truncate";
            name.style="white-space: normal;"
            name.textContent = item.nombre || "Sin nombre";
            topContent.appendChild(name);

            const img = document.createElement('img');
            img.src = item.image_url ? "/static/images/menu/" + item.image_url : "/static/example.jpg";
            img.alt = item.nombre || "Imagen del producto";
            img.className = "w-full h-48 object-cover rounded-xl mb-4";
            topContent.appendChild(img);

            const descripcion = document.createElement('p');
            descripcion.className = "text-sm text-gray-600 dark:text-gray-400 mb-2";
            descripcion.textContent = item.descripcion || "Sin descripción disponible";
            topContent.appendChild(descripcion);

            const price = document.createElement('p');
            price.className = "text-lg font-semibold text-green-600 dark:text-green-400";
            price.textContent = `Precio: $${item.precio_unitario || 0}`;
            topContent.appendChild(price);

            card.appendChild(topContent);

            // --- Bottom content ---
            const bottomContent = document.createElement('div');
            bottomContent.className = "mt-6 flex items-center justify-between p-5";

            const order_button = document.createElement('button');
            order_button.type = "button";
            order_button.textContent = "Agregar";
            order_button.className = "btn flex-1 bg-primary border border-primary rounded-md text-white transition-all duration-300 hover:bg-primary/[0.85] hover:border-primary/[0.85]"
            order_button.addEventListener("click", () => {
                openActions(item.id, id_pedido);
            });
            bottomContent.appendChild(order_button);
            card.appendChild(bottomContent);
            container.appendChild(card);



        });
    } catch (error) {
        console.error("Error fetching or processing data:", error);
        return null;
    }
}

get_data('todos',id_pedido);

async function openActions(id_menu,id_pedido) {
        showLoader();
        const addButton = document.querySelector('button[data-action="add"]');
        const cancelButton = document.querySelector('button[data-action="cancel"]');
        if (cancelButton) {
            cancelButton.addEventListener("click", closeActions);
        }
        addButton.onclick = async () => {
            // Collect quantity
            const qtyInput = document.querySelector("#modal_content input[type='number']");
            const quantity = qtyInput ? parseInt(qtyInput.value) || 1 : 1;
            // Collect selected mods
            const selectedMods = Array.from(
                document.querySelectorAll("#modal_content input[name='mod-selection']:checked")
            ).map(el => el.value);

            // Collect selected add-ons
            const selectedAddons = Array.from(
                document.querySelectorAll("#modal_content input[name='addon-selection']:checked")
            ).map(el => el.value);

            // Collect notes
            const notesInput = document.querySelector("#modal_content textarea");
            const notes = notesInput ? notesInput.value.trim() : "";

            // Build payload
            const payload = {
                id_menu,
                id_pedido,
                quantity,
                mods: selectedMods,
                add_ons: selectedAddons,
                notes
            };

            try {
                const response = await fetch(`/pedidos_en_linea/add_item`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        'X-CSRFToken': '{{ csrf_token() }}',
                    },
                    body: JSON.stringify(payload),
                });

                if (!response.ok) {
                    throw new Error(`Error ${response.status}`);
                }

                const result = await response.json();
                const importeSpan = document.getElementById("importe");
                importeSpan.innerHTML='$'+result.importe
                closeActions();
                checkImporte();
            } catch (err) {
                console.error("Error sending item:", err);
            }
        };
        const data = await get_record(id_menu);
        const popupActions = document.getElementById('modal');
        popupActions.classList.remove('hidden');
        hideLoader();
}

function closeActions() {
        const popupActions = document.getElementById('modal');
        const container = document.getElementById('modal_content');
        container.innerHTML = ''; 
        popupActions.classList.add('hidden');
}
async function get_record(id_menu) {
    try {
        const path = `/pedidos_en_linea/item_data/${id_menu}/${id_pedido}`;
        const response = await fetch(path);
        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.statusText}`);
        }
        const data = await response.json();

        const modal_content = document.getElementById('modal_content');
        modal_content.innerHTML = ""; 

        menu = data.item[0];

        // --- Top section with title + quantity ---
        const top = document.createElement('div');
        top.className =
        "flex bg-white dark:bg-dark items-center border-b border-lightgray/10 dark:border-gray/20 justify-between px-5 py-3";

        // Wrapper for name + description
        const textWrapper = document.createElement('div');
        textWrapper.className = "flex flex-col";  // stack vertically

        const name = document.createElement('h5');
        name.className = "font-semibold text-lg text-gray-900 dark:text-white";
        console.log(menu)
        name.textContent = menu.nombre + ' ' + money_format(menu.precio_unitario) || "Sin nombre";

        const descripcion = document.createElement('p');
        descripcion.className = "text-sm text-gray-600 dark:text-gray-300"; // smaller style for description
        descripcion.textContent = menu.descripcion || "Sin descripción";

        // append name + description inside wrapper
        textWrapper.append(name, descripcion);

        // Quantity controls
        const qtyWrapper = document.createElement('div');
        qtyWrapper.className = "flex items-center gap-2";

        const minusBtn = document.createElement('button');
        minusBtn.type = "button";
        minusBtn.textContent = "−";
        minusBtn.className =
        "w-8 h-8 flex items-center justify-center rounded-md border border-gray-300 dark:border-gray/20 " +
        "bg-white dark:bg-dark text-gray-900 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700";

        const qtyInput = document.createElement('input');
        qtyInput.type = "number";
        qtyInput.value = 1;
        qtyInput.min = 1;
        qtyInput.className =
        "w-12 text-center border border-gray-300 dark:border-gray/20 rounded-md " +
        "bg-white dark:bg-dark text-gray-900 dark:text-white";

        const plusBtn = document.createElement('button');
        plusBtn.type = "button";
        plusBtn.textContent = "+";
        plusBtn.className =
        "w-8 h-8 flex items-center justify-center rounded-md border border-gray-300 dark:border-gray/20 " +
        "bg-white dark:bg-dark text-gray-900 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700";

        minusBtn.addEventListener("click", () => {
        let val = parseInt(qtyInput.value) || 1;
        if (val > 1) qtyInput.value = val - 1;
        });
        plusBtn.addEventListener("click", () => {
        let val = parseInt(qtyInput.value) || 1;
        qtyInput.value = val + 1;
        });

        qtyWrapper.append(minusBtn, qtyInput, plusBtn);

        // Put text on the left, quantity controls on the right
        top.append(textWrapper, qtyWrapper);

        // --- Modificaciones (only if there are items) ---
        let mods;
        if (data.mods && data.mods.length > 0) {
            mods = document.createElement('div');
            mods.className = "p-5";

            const title = document.createElement('h3');
            title.textContent = 'Modificaciones';
            title.className = "text-lg font-semibold mb-3 p-2 text-gray-900 dark:text-white";
            mods.appendChild(title);

            const grid = document.createElement('div');
            grid.className = "grid grid-cols-1 sm:grid-cols-3 gap-6";
            mods.appendChild(grid);

            data.mods.forEach((item) => {
                const wrapper = document.createElement('div');
                wrapper.className = "relative budget-input";

                const label = document.createElement('label');
                label.className =
                    "flex cursor-pointer rounded-lg justify-between bg-white dark:bg-dark " +
                    "dark:border-gray/20 border-2 border-lightgray/10 items-start gap-4 p-5 relative";

                const leftDiv = document.createElement('div');
                leftDiv.className = "relative z-10 text-sm font-semibold w-full text-gray-900 dark:text-white";

                const innerDiv = document.createElement('div');
                innerDiv.className = "flex items-center gap-3 flex-1";
                innerDiv.textContent = item.nombre;
                leftDiv.appendChild(innerDiv);

                const input = document.createElement('input');
                input.type = "checkbox";
                input.name = "mod-selection";
                input.value = item.nombre;
                input.className = "form-checkbox relative hidden z-10 peer";

                const glowSpan = document.createElement('span');
                glowSpan.className =
                    "rounded-lg border-2 border-transparent peer-checked:border-primary/20 " +
                    "peer-checked:bg-primary/[8%] absolute top-0 left-0 z-0 w-full h-full";

                label.append(leftDiv, input, glowSpan);
                wrapper.appendChild(label);
                grid.appendChild(wrapper);
            });
        }
        let add_ons;
        if (data.add_ons && data.add_ons.length > 0) {
            add_ons = document.createElement('div');
            add_ons.className = "p-5";

            const title_addons = document.createElement('h3');
            title_addons.textContent = 'Adiciones';
            title_addons.className = "text-lg font-semibold mb-3 p-2 text-gray-900 dark:text-white";
            add_ons.appendChild(title_addons);

            const grid_addons = document.createElement('div');
            grid_addons.className = "grid grid-cols-1 sm:grid-cols-3 gap-6";
            add_ons.appendChild(grid_addons);

            data.add_ons.forEach((item) => {
                const wrapper = document.createElement('div');
                wrapper.className = "relative budget-input";

                const label = document.createElement('label');
                label.className =
                    "flex cursor-pointer rounded-lg justify-between bg-white dark:bg-dark " +
                    "dark:border-gray/20 border-2 border-lightgray/10 items-start gap-4 p-5 relative";

                const leftDiv = document.createElement('div');
                leftDiv.className = "relative z-10 text-sm font-semibold w-full text-gray-900 dark:text-white";

                const innerDiv = document.createElement('div');
                innerDiv.className = "flex items-center gap-3 flex-1";
                innerDiv.textContent = item.nombre+' +'+ money_format(item.precio_unitario);
                leftDiv.appendChild(innerDiv);

                const input = document.createElement('input');
                input.type = "checkbox";
                input.name = "addon-selection";
                input.value = item.id;
                input.className = "form-checkbox relative hidden z-10 peer";

                const glowSpan = document.createElement('span');
                glowSpan.className =
                    "rounded-lg border-2 border-transparent peer-checked:border-primary/20 " +
                    "peer-checked:bg-primary/[8%] absolute top-0 left-0 z-0 w-full h-full";

                label.append(leftDiv, input, glowSpan);
                wrapper.appendChild(label);
                grid_addons.appendChild(wrapper);
            });
        }

        // --- Notes textarea ---
        const notesWrapper = document.createElement('div');
        notesWrapper.className = "p-5";

        const notesLabel = document.createElement('label');
        notesLabel.textContent = "Notas";
        notesLabel.className = "block text-sm font-semibold mb-2 text-gray-900 dark:text-white p-2";

        const notesInput = document.createElement('textarea');
        notesInput.className =
            "w-full border border-gray-300 dark:border-gray/20 rounded-md p-2 " +
            "bg-white dark:bg-dark text-gray-900 dark:text-white focus:ring-primary focus:border-primary";
        notesInput.rows = 3;
        notesInput.placeholder = "Escribe notas adicionales aquí...";

        notesWrapper.append(notesLabel, notesInput);

        // --- Attach to modal ---
        modal_content.appendChild(top);
        if (mods) modal_content.appendChild(mods);
        if (add_ons) modal_content.appendChild(add_ons);
        modal_content.appendChild(notesWrapper);
    } catch (error) {
        console.error("Error fetching or processing data:", error);
        return null;
    }
}
