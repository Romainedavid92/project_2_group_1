// d3.json("/teams/2016").then((teams) => {
//     Object.values(teams).forEach(team => {
//         Object.entries(team).forEach(([key, value]) => {
//             console.log(`${key}:${value}`)
//         });
//     });
// });

// d3.json("/people").then((teams) => {
//     Object.values(teams).forEach(team => {
//         Object.entries(team).forEach(([key, value]) => {
//             console.log(`${key}:${value}`)
//         });
//     });
// });

$(document).ready(function() {
    buildCharts();
});

function buildCharts(year) {
    d3.json(`/salaries/`).then((data) => {
        var objs = Object.values(data);

        var years = [];
        var totalPay = [];
        var empName = [];
        for (var i = 0; i < objs.length; i++) {
            years.push(objs[i].Year);
            totalPay.push(objs[i].TotalPay);
            empName.push(objs[i].EmployeeName);
        }

        // Build a Bubble Chart
        var bubbleLayout = {
            margin: { t: 0 },
            hovermode: "closest",
            xaxis: { title: "Year" },
            yaxis: { title: "Total Pay" }
        };
        var bubbleData = [{
            x: years,
            y: totalPay,
            text: empName,
            mode: "markers",
            marker: {
                size: 10,
                color: year,
                colorscale: "Earth"
            }
        }];

        Plotly.newPlot("bubble", bubbleData, bubbleLayout);
    });
}