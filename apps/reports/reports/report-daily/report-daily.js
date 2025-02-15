document.addEventListener('DOMContentLoaded', function () {
    var sellers = window.sellers;
    var pedidos = window.pedidos;

    var data = sellers.map(function (seller, index) {
        var value = pedidos[index];
        var color;
        if (value >= 20) {
            color = '#F59D2A';
        } else if (value >= 10 && value < 20) {
            color = '#FEC172';
        } else {
            color = '#FDE6CA';
        }
        return { name: seller, y: value, color: color };
    });

    Highcharts.chart('container', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Pedidos Hoje por Seller',
            style: {
                fontSize: '18px',
                fontFamily: 'Roboto, sans-serif',
                color: '#4A2F0D',
                weight: 'bold'
            }
        },
        credits: {
            enabled: false
        },
        xAxis: {
            title: {
                text: 'Seller',
                style: {
                    fontFamily: 'Roboto, sans-serif',
                    color: '#4A2F0D',
                    weight: 'bold'
                }

            },
            type: 'category',
            labels: {
                autoRotation: [-45, -90],
                style: {
                    fontSize: '12px',
                    fontFamily: 'Roboto, sans-serif'
                }
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Quantidade de Pedidos',
                style: {
                    fontFamily: 'Roboto, sans-serif',
                    color: '#4A2F0D',
                    weight: 'bold'
                }
            }
        },
        legend: {
            enabled: false
        },
        tooltip: {
            pointFormat: '<b>{point.y}</b> pedidos'
        },
        series: [{
            name: 'Pedidos',
            data: data,
            dataLabels: {
                enabled: true,
                rotation: 0,
                color: '#626266',
                inside: false,
                verticalAlign: 'bottom',
                format: '{point.y}',
                style: {
                    fontSize: '15px',
                    fontFamily: 'Roboto, sans-serif',
                    textOutline: 'none'
                },
                overflow: 'none',
                crop: false
            }
        }]
    });
});

document.addEventListener('DOMContentLoaded', function () {
    function setGaugeValue(gaugeId, value) {
        const gauge = document.getElementById(gaugeId);
        if (!gauge) return;

        const fill = gauge.querySelector(".gauge__fill");
        const cover = gauge.querySelector(".gauge__cover");

        let numericValue = parseFloat(value);
        if (isNaN(numericValue) || numericValue < 0) {
            numericValue = 0;
        } else if (numericValue > 100) {
            numericValue = 100;
        }

        let rotation = (numericValue / 100) * 180;
        fill.style.transform = `rotate(${rotation}deg)`;
        cover.textContent = `${numericValue.toFixed(2)}%`;
    }

    setGaugeValue("gauge-monthly", monthly_meta_percentage);
    setGaugeValue("gauge-daily", daily_meta_percentage);
});