$(document).ready(function() {
    buildJobTitleChart(2014, "Top", 10);

    //Event listeners
    $('#years').change(function() {
        $('#graphs').hide();
        $('#gif').show();

        var year = $('#years').val();
        var topBottom = $('#topBottom').val();
        var limit = $('#limit').val();

        buildJobTitleChart(year, topBottom, limit);
    });
    $('#topBottom').change(function() {
        $('#graphs').hide();
        $('#gif').show();

        var year = $('#years').val();
        var topBottom = $('#topBottom').val();
        var limit = $('#limit').val();

        buildJobTitleChart(year, topBottom, limit);
    });
    $('#limit').change(function() {
        $('#graphs').hide();
        $('#gif').show();

        var year = $('#years').val();
        var topBottom = $('#topBottom').val();
        var limit = $('#limit').val();

        buildJobTitleChart(year, topBottom, limit);
    });
});

function buildJobTitleChart(year, topBottom, limit) {
    d3.json(`/jobTitles/${year}/${topBottom}`).then((data) => {

        var height = 45;
        if (limit == 5) {
            height = 75;
        }

        // Sort the data array using the Salary
        data = Object.entries(data).sort(function(a, b) {
            return parseFloat(b.Mean_Salary) - parseFloat(a.Mean_Salary);
        });

        // Slice the first 10 objects for plotting
        data = data.slice(0, limit);

        // Reverse the array due to Plotly's defaults
        data = data.reverse();

        //var objs = Object.values(data);

        var jobTitle = [];
        var meanPay = [];
        for (var i = 0; i < data.length; i++) {
            jobTitle.push(data[i][1].JobTitle);
            meanPay.push(data[i][1].Mean_Salary);
        }

        // Trace1 for the Data
        var trace1 = {
            x: meanPay,
            y: jobTitle,
            text: jobTitle,
            name: "Salary",
            type: "bar",
            orientation: "h",
            marker: {
                color: 'rgb(255,80,0)',
                line: { color: 'transparent' }
            }

        };

        // data
        var data = [trace1];

        // Apply the group bar mode to the layout
        var layout = {
            autosize: false,
            height: limit * height,
            width: 1000,
            title: "Mean Salaries by Job Title",
            xaxis: { title: "Average Salary ($)" },
            margin: {
                l: 300,
                r: 100,
                t: 100,
                b: 100
            },
            titlefont: {
                size: 25,
                family: 'Bold',
                color: 'Black'
            },
            font: {
                family: 'Bold',
                size: 17,
                color: 'Black'
            }
        };

        // Render the plot to the div tag with id "plot"
        Plotly.newPlot("plot", data, layout);

        $('#graphs').show();
        $('#gif').hide();
    });
}