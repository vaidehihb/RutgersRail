$(document).ready(function () {
   linechartdata = {
        'filters':[{
                'column' : 'Year',
                'type' : 'range',
                'params': {
                    'min_val' : 1990,
                    'max_val' : 2000,
                    'include_max' : true,
                    'include_min' : true
                }
        }],
        'groupbycolumns':['Year'],
        'columnsToRetain': []
   };

   piechartdata = {
        'filters':[{
                'column' : 'Year',
                'type' : 'range',
                'params': {
                    'min_val' : 1990,
                    'max_val' : 2000,
                    'include_max' : true,
                    'include_min' : true
                }
        }],
        'groupbycolumns':['Platform'],
        'columnsToRetain': [],
        'aggregate': ['Platform']
   };


   $.ajax({
        url: '/linechart',
        type:'POST',
        data: JSON.stringify(linechartdata),
        contentType: "application/json",
        complete: function (lineresult) {
            lineresult = $.parseJSON(lineresult.responseText);
//            console.log(res['NA_Sales']);
//            console.log(res['EU_Sales']);
//            console.log(res['Global_Sales']);
            Highcharts.chart('line', {
            'type': 'line',

    title: {
        text: 'Sales by Year'
    },

    subtitle: {
        text: ''
    },
		xAxis: {
                    categories: lineresult['Year'],
                    title: {
                        text: 'Years'
                    }
                },
    yAxis: {
        title: {
            text: 'Sales'
        }
    },
    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle'
    },

    plotOptions: {
        series: {
            label: {
                connectorAllowed: false
            },
            pointStart: lineresult['Year'][0]
        }
    },

    series: [{
                    name: 'NA Sales',
                    data: lineresult['NA_Sales']
                }, {
                    name: 'EU_Sales	',
                    data: lineresult['EU_Sales']
                }, {
                    name: 'JP_Sales',
                    data: lineresult['JP_Sales']
                }, {
                    name: 'Other_Sales',
                    data: lineresult['Other_Sales']
                }, {
                    name: 'Global_Sales',
                    data: lineresult['Global_Sales']
                }],

    responsive: {
        rules: [{
            condition: {
                maxWidth: 500
            },
            chartOptions: {
                legend: {
                    layout: 'horizontal',
                    align: 'center',
                    verticalAlign: 'bottom'
                }
            }
        }]
    }

});
}});
//
$.ajax({
        url: '/piechart',
        type:'POST',
        data: JSON.stringify(piechartdata),
        contentType: "application/json",
        complete: function (pieresult) {
            pieresult = $.parseJSON(pieresult.responseText);
//
seriesdata = [];
$.each(pieresult['Total'], function(index, element) {
    t = {
            name: pieresult['Platform'][index],
            y: element,
            sliced: true,
            selected: true
        };
    seriesdata.push(t);
});

Highcharts.chart('pie', {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie'
    },
    title: {
        text: 'Sales by Genre'
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: false,

            },
            showInLegend: true
        },
        series: {
                dataLabels: {
                    enabled: true,
                    formatter: function() {
                        return Math.round(this.percentage*100)/100 + ' %';
                    },
                    distance: -30,
                    color:'blue'
                }
            }
    },
    series: [{
        name: 'Sales',
        colorByPoint: true,
        data: seriesdata
    }]
});
   }});
});