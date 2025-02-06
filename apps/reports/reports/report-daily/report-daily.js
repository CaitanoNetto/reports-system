document.addEventListener("DOMContentLoaded", function () {
    var sellers = window.sellers;
    var pedidos = window.pedidos;

    var data = sellers.map(function (seller, index) {
        var value = pedidos[index];
        var color = value >= 20 ? "#F59D2A" : (value >= 10 ? "#FEC172" : "#FDE6CA");
        return { name: seller, y: value, color: color };
    });

    Highcharts.chart("container", {
        chart: { type: "column" },
        title: { text: "Pedidos Hoje por Seller", style: { fontSize: "18px", fontFamily: "Roboto, sans-serif", color: "#4A2F0D", fontWeight: "bold" } },
        credits: { enabled: false },
        xAxis: { type: "category", title: { text: "Seller", style: { fontFamily: "Roboto, sans-serif", color: "#4A2F0D", fontWeight: "bold" } }, labels: { autoRotation: [-45, -90], style: { fontSize: "12px", fontFamily: "Roboto, sans-serif" } } },
        yAxis: { min: 0, title: { text: "Quantidade de Pedidos", style: { fontFamily: "Roboto, sans-serif", color: "#4A2F0D", fontWeight: "bold" } } },
        legend: { enabled: false },
        tooltip: { pointFormat: "<b>{point.y}</b> pedidos" },
        series: [{
            name: "Pedidos",
            data: data,
            dataLabels: { enabled: true, color: "#626266", inside: false, verticalAlign: "bottom", format: "{point.y}", style: { fontSize: "15px", fontFamily: "Roboto, sans-serif", textOutline: "none" } }
        }]
    });
});