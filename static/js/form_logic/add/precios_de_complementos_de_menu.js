
  document.getElementById("dynamic_form").addEventListener("submit", async function (e) {
    e.preventDefault(); // Stop form submission until we checka

    try {
      // Example fetch (replace with your own API/endpoint)

        const id_canal_de_venta=document.getElementById("id_canal_de_venta").value
        const id_complemento_de_menu=document.getElementById("id_complemento_de_menu").value
        const response = await fetch(`/precios_de_complementos_de_menu/validate_before_submit/${id_canal_de_venta}/${id_complemento_de_menu}`, {method: "GET",});
        const data = await response.json();
        if (data.status == 1 || record_edit!='') {
            e.target.submit();
        } else {
                window.dispatchEvent(new CustomEvent('show-warning', {
                    detail: 'Ya existe un precio de la sucursal, canal de venta y del complemento de menu.'  
                }));
                warningAlert.style.display = 'flex';
                warningAlert.style.opacity = '1'; 
                setTimeout(function() {
                    warningAlert.style.opacity = '0';  
                    setTimeout(function() {
                        warningAlert.style.display = 'none';
                    }, 1000);  
                }, 3000);
        }

    } catch (error) {
      console.error("Error fetching data:", error);
      alert("Something went wrong while validating. Please try again.");
    }
  });