document.addEventListener('alpine:init', () => {
    Alpine.store('modalData', { record: {} });
});
function redirectActions(url) {
        if (url.includes("delete")) {
            // Para eliminación se confirma y se envía por POST
            if (confirm('¿Quieres eliminar el registro seleccionado?')) {
                const form = document.getElementById('action_buttons');
                form.action = url;
                form.method = "POST";
                form.submit();
            }
        } else if (url.includes("download_pdf")) {
            // Para descargar PDF se utiliza fetch y se procesa la descarga
            fetch(url, { 
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
				    },
                })
                .then(response => {
                    if (response.ok) {
                        return response.blob();
                    } else {
                        throw new Error("No se pudo descargar el archivo.");
                    }
                })
                .then(blob => {
                    const downloadUrl = window.URL.createObjectURL(blob);
                    const a = document.createElement("a");
                    a.href = downloadUrl;
                    a.download = `${url.split("=")[2]}.pdf`;
                    document.body.appendChild(a);
                    a.click();
                    a.remove();
                    window.location.reload();
                })
                .catch(error => {
                    alert("Error al descargar el archivo: " + error.message);
                });
        } else {
            window.location.href = url;
        }
}
function formatCurrency(value) {
        // Ensure it's a valid number, then format it as currency
        return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value);
}
function formatNumber(value) {
        // Format number with commas as thousands separators
        return new Intl.NumberFormat('en-US').format(value);
}
function titleFormat(value) {
  const replacements = {
    "id": "ID",
        "visualizacion": "visualización",
        "creacion": "creación",
        "descripcion": "descripción",
        "informacion": "información",
        "categoria": "categoría",
        "menu": "menú",
        "telefono": "teléfono",
        "razon": "razón",
        "metodo": "método",
        "transito": "tránsito",
        "periodico": "periódico",
        "genero":"género",
        "direccion":"dirección",
        "codigo":"código",
        "contratacion":"contratación",
        "numero":"número",
        "razon":"razón",
        "direccion":"dirección",
        "nomina":"nómina",
        "electronico":"electrónico",
        "ultimo":"último",
        "sesion":"sesión",
        "metodo":"método",
        "comision":"comisión",
        "codigo":"código",
        "actualizacion": "actualización",
        "ejecucion": "ejecución",
        "dias":"días",
        "transito": "tránsito",
  };


  // Check for exact match
  if (replacements[value]) {
    return replacements[value].charAt(0).toUpperCase() + replacements[value].slice(1);
  }

  // Replace underscores with spaces
  let formatted = value.replace("_nombre_completo", "").replace("_nombre", "").replace(/_/g, " ");
  // Remove "id " prefix if present
  if (formatted.startsWith("id ")) {
    formatted = formatted.slice(3);
  }

  // Replace words with accented versions if needed
  for (let k in replacements) {
    const regex = new RegExp(`\\b${k}\\b`, "i");
    if (regex.test(formatted)) {
      formatted = formatted.replace(regex, replacements[k]);
    }
  }
  formatted = formatted.charAt(0).toUpperCase() + formatted.slice(1);

  return formatted;
}
async function openActions(form, recordId,estatus) {
        showLoader();
        //document.getElementById('id_registro').textContent=recordId;
        document.getElementById('estatus').textContent = estatus;

        const updateButton = document.querySelector('button[data-action="actualizar"]');
        const deleteButton = document.querySelector('button[data-action="delete"]');
        const downloadButton = document.querySelector('button[data-action="descargar"]');

        if (updateButton) {
            updateButton.setAttribute('onclick', `redirectActions('/${form}/form?id=${recordId}')`);
        }

        if (deleteButton) {
            deleteButton.setAttribute('onclick', `redirectActions('/${form}/delete?id=${recordId}')`);
        }

        if (downloadButton) {
            downloadButton.setAttribute('onclick', `redirectActions('/files/download_pdf?table=${form}&id=${recordId}')`);
        }

        const data = await get_record(form, recordId);
        const popupActions = document.getElementById('modal');
        Alpine.store('modalData').record = data;
        popupActions.classList.remove('hidden');
        hideLoader();
}

function closeActions() {
        const popupActions = document.getElementById('modal');
        const container = document.getElementById('modal_content');
        container.innerHTML = ''; 
        popupActions.classList.add('hidden');
}
async function get_record(form, recordId) {
        try {
            const path = `/${form}/data/${recordId}`;
            const response = await fetch(path);
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.statusText}`);
            }
            const data = await response.json();
            const record = data[0]; // first record
            const recordObj = Object.fromEntries(record);

            const modal_content = document.getElementById('modal_content');
            modal_content.innerHTML = '<tbody></tbody>';
            const tbody_modal_content = modal_content.querySelector("tbody");
            try {
                modal_content_relationship = document.getElementById('modal_content_relationship');
                modal_content_relationship.innerHTML = '<tbody></tbody>';
                tbody_modal_content_relationship = modal_content_relationship.querySelector("tbody");
            } catch (error) {
                console.error("Error accessing modal_content_relationship:", error);
            }


            for (const [key, rawValue] of Object.entries(recordObj)) {
                let value = rawValue;
                if(key==='id_visualizacion'){
                    document.getElementById('id_registro').textContent=value;
                }

                if (/(importe|monto|precio|subtotal|descuentos|propina|comisiones|otros_costos|costo_de_envio)/i.test(key) && !isNaN(value)) {
                    value = formatCurrency(value);
                } else if (!isNaN(value)) {
                    value = formatNumber(value);
                }
                const tr = document.createElement('tr');


                if(String(value).includes('/dynamic')){
                    tr.innerHTML = `<td style="border-right: 1px solid #ccc; padding: 8px;">${titleFormat(key)}</td>
                    <td style="text-align: center;">
                        <button type="submit"
                            @click.stop="window.location.href='${value}'"
                            class="btn border text-primary border-transparent rounded-md transition-all duration-300 hover:text-white hover:bg-primary bg-primary/10">
                            Ver
                        </button>
                    </td>`;
                    tbody_modal_content_relationship.appendChild(tr);
                }else if(key!=='id'){
                    tr.innerHTML = `<td style="border-right: 1px solid #ccc; padding: 8px; ">${titleFormat(key)}</td><td style="word-break: break-word; white-space: normal; overflow-wrap: anywhere; max-width: 300px;">${value}</td>`;
                    tbody_modal_content.appendChild(tr);
                }
            }



            return recordObj;
        } catch (error) {
            console.error("Error fetching or processing data:", error);
            return null; 
        }
}