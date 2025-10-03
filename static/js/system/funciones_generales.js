// capitaliza nombres
function capitalizeWords(str) {
    return str.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}
// funcion para obtener el lunes de hace dos semanas
function getMondayOfTwoWeeksAgo() {
    const today = new Date();
    // Subtract 14 days (2 weeks)
    const twoWeeksAgo = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 14);
    // Get the day of week (0 = Sunday, 1 = Monday, ..., 6 = Saturday)
    const day = twoWeeksAgo.getDay();
    // Calculate difference to get to Monday (if Sunday, go back 6 days; else, go back (day-1) days)
    const diffToMonday = day === 0 ? -6 : 1 - day;
    const monday = new Date(twoWeeksAgo);
    monday.setDate(twoWeeksAgo.getDate() + diffToMonday);
    // Return as YYYY-MM-DD
    return monday.toISOString().split('T')[0];
}
function money_format(value) {
    return `$${new Intl.NumberFormat().format(value)}`;
}
// funcion para obtener un valor de un sql
function obtener_valor(selector,columnName,path,format) {
    fetch(path)
    .then(response => {
        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        document.querySelector(selector).textContent=''
        if (format === 'currency') {
            document.querySelector(selector).textContent = money_format(data[0][columnName]);
        } else if (format === 'percent') {
            // Assume value is stored as a number like 0.35 → show "35%"
            let val = data[0][columnName];
            if (val !== null && val !== undefined) {
                val=Number(val)
                document.querySelector(selector).textContent = val.toFixed(0) + '%';
            }
        } else {
            document.querySelector(selector).textContent = data[0][columnName];
        }
    })
    .catch(error => {
        console.error("Error fetching or processing data:", error);
    });
};