document.getElementById("dynamic_form").addEventListener("submit", async function (e) {
  e.preventDefault(); // Stop form submission until we check
    const cuenta_de_banco=document.getElementById("id_cuenta_de_banco").value;
    const canal_de_venta=document.getElementById("id_canal_de_venta").value;
    if(cuenta_de_banco==="" && canal_de_venta===""){
        window.dispatchEvent(new CustomEvent('show-warning', {
            detail: 'Favor de ingresar una cuenta de banco o un canal de venta.'  
        }));
        warningAlert.style.display = 'flex';
        warningAlert.style.opacity = '1'; 
        setTimeout(function() {
            warningAlert.style.opacity = '0';  
            setTimeout(function() {
                warningAlert.style.display = 'none';
            }, 1000);  
        }, 3000);
    }else{
        e.target.submit();
    }

});