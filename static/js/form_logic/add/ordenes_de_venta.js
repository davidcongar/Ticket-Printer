
  document.getElementById("dynamic_form").addEventListener("submit", async function (e) {
    e.preventDefault(); // Stop form submission until we check
    try {
      const queryString = window.location.search;
      const urlParams = new URLSearchParams(queryString);
      const id_record = urlParams.get('id'); 
      if(id_record==null){
        // Example fetch (replace with your own API/endpoint)
          const id_sucursal=document.getElementById("id_sucursal").value
          const response = await fetch(`/ordenes_de_venta/validate_before_submit/${id_sucursal}`, {method: "GET",});
          const data = await response.json();
          if (data.status == 1 || record_edit!='') {
            e.target.submit();
          } else {
                  window.dispatchEvent(new CustomEvent('show-warning', {
                      detail: 'No se ha registrado el turno del día actual de la sucursal o ya se finalizo el turno. Favor de revisar.'  
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
      }else{
                    e.target.submit();
      }

    } catch (error) {
      console.error("Error fetching data:", error);
      alert("Something went wrong while validating. Please try again.");
    }
  });