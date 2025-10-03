function today() {
  const d = new Date();
  return d.toISOString().split("T")[0]; // "YYYY-MM-DD"
}
  document.getElementById("dynamic_form").addEventListener("submit", async function (e) {
    e.preventDefault(); // Stop form submission until we check

    try {
      // Example fetch (replace with your own API/endpoint)
      const id_sucursal=document.getElementById("id_sucursal").value
        const response = await fetch(`/turnos_de_operacion/validate_before_submit/${id_sucursal}/${encodeURIComponent(today())}`, {
            method: "GET",
            });
        const data = await response.json();
        if (data.status==1) {
            e.target.submit();
        } else {
                window.dispatchEvent(new CustomEvent('show-warning', {
                    detail: 'Ya existe un registro de la sucursal y fecha ingresada.'  
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