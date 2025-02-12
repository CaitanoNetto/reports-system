document.addEventListener('DOMContentLoaded', function () {
    if (Array.isArray(window.sellers) && window.sellers.length > 0 && Array.isArray(window.pedidos) && window.pedidos.length > 0) {
        var data = window.sellers.map(function (seller, index) {
            var value = window.pedidos[index] || 0;
            var color = value >= 20 ? '#F59D2A' : value >= 10 ? '#FEC172' : '#FDE6CA';
            return { name: seller, y: value, color: color };
        });

        Highcharts.chart('container', {
            chart: { type: 'column' },
            title: { text: 'Pedidos Hoje por Seller', style: { fontSize: '18px', fontFamily: 'Roboto, sans-serif', color: '#4A2F0D', fontWeight: 'bold' } },
            credits: { enabled: false },
            xAxis: { type: 'category', labels: { autoRotation: [-45, -90], style: { fontSize: '12px', fontFamily: 'Roboto, sans-serif' } } },
            yAxis: { min: 0, title: { text: 'Quantidade de Pedidos', style: { fontFamily: 'Roboto, sans-serif', color: '#4A2F0D', fontWeight: 'bold' } } },
            legend: { enabled: false },
            tooltip: { pointFormat: '<b>{point.y}</b> pedidos' },
            series: [{ name: 'Pedidos', data: data }]
        });
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const gaugeOptions = {
        chart: { type: 'solidgauge' },
        title: null,
        pane: { center: ['50%', '85%'], size: '140%', startAngle: -90, endAngle: 90 },
        yAxis: { min: 0, max: window.totalMeta, title: { text: 'Entregas' } },
        series: [{ name: 'Entregas', data: [window.deliveredPercentage] }]
    };

    Highcharts.chart('container-speed', gaugeOptions);
    Highcharts.chart('container-rpm', { ...gaugeOptions, yAxis: { min: 0, max: window.newDailyMetaValue, title: { text: 'Meta Diária' } } });
});
