document.addEventListener('DOMContentLoaded', function () {
    var sellers = window.sellers;
    var pedidos = window.pedidos;

    var data = sellers.map(function (seller, index) {
        return {
            name: seller,
            value: pedidos[index]
        };
    });

    var chartDom = document.getElementById('container');
    var myChart = echarts.init(chartDom);
    var option;

    option = {
        title: {
            text: 'Pedidos Hoje por Seller',
            left: 'center',
            textStyle: {
                fontSize: 18,
                fontFamily: 'Roboto, sans-serif',
                color: '#4A2F0D',
                fontWeight: 'bold'
            }
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        grid: {
            left: '5%',
            right: '5%',
            bottom: '5%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            data: data.map(item => item.name),
            axisLabel: {
                rotate: 45,
                fontSize: 12,
                fontFamily: 'Roboto, sans-serif',
                color: '#4A2F0D',
                fontWeight: 'bold'
            },
            axisLine: {
                lineStyle: {
                    color: '#4A2F0D'
                }
            }
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                fontSize: 12,
                fontFamily: 'Roboto, sans-serif',
                color: '#4A2F0D',
                fontWeight: 'bold'
            },
            axisLine: {
                lineStyle: {
                    color: '#4A2F0D'
                }
            },
            splitLine: {
                show: false
            }
        },
        series: [
            {
                name: 'Pedidos',
                type: 'bar',
                barWidth: '50%',
                data: data.map(item => ({
                    value: item.value,
                    itemStyle: {
                        color: item.value >= 20 ? '#F59D2A' : item.value >= 10 ? '#FEC172' : '#FDE6CA'
                    }
                })),
                label: {
                    show: true,
                    position: 'top',
                    fontSize: 15,
                    fontFamily: 'Roboto, sans-serif',
                    color: '#626266'
                }
            }
        ]
    };

    option && myChart.setOption(option);
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
        cover.textContent = `${numericValue.toFixed(2).replace('.', ',')}%`;
        let existingLabels = gauge.parentElement.querySelector(".gauge__labels");
        if (existingLabels) {
            existingLabels.remove();
        }

        let labelsContainer = document.createElement("div");
        labelsContainer.classList.add("gauge__labels");
        gauge.parentElement.appendChild(labelsContainer);

    }

    setGaugeValue("gauge-monthly", monthly_meta_percentage);
    setGaugeValue("gauge-daily", daily_meta_percentage);
    setGaugeValue("gauge-sao-paulo", monthly_sao_paulo_meta_percentage);
    setGaugeValue("gauge-campinas", monthly_campinas_meta_percentage);
    setGaugeValue("gauge-belo-horizonte", monthly_belo_horizonte_meta_percentage);

});