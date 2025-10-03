
  document.getElementById("dynamic_form").addEventListener("submit", async function (e) {
    e.preventDefault(); // Stop form submission until we check
    try {
        const id_area_de_sucursal=document.getElementById("id_area_de_sucursal").value
        const numero_de_mesa=document.getElementById("numero_de_mesa").value
        const response = await fetch(`/mesas/validate_before_submit/${id_area_de_sucursal}/${numero_de_mesa}`, {method: "GET",});
        const data = await response.json();
        if (data.status == 1 || record_edit!='') {
            e.target.submit();
        } else {
                window.dispatchEvent(new CustomEvent('show-warning', {
                    detail: 'Ya existe una mesa para la sucursal y área de sucursal.'  
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