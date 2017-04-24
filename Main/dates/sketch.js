var h, w;
var file;
var urlOfFile;
var dataArray = [];

function setup() {
    h = windowHeight;
    w = windowWidth;
    //to get informations
    urlOfFile = "http://tom.moulard.org/dates/date.txt";
    postFix = "./date.php?filename=usdeur.json&callback=?";
    localFile = "./date.csv";
    fillArray(urlOfFile);

    //to set the graph
    //$.getJSON("https://www.highcharts.com/samples/data/jsonp.php?filename=usdeur.json&callback=?", function(data) {
    //$.getJSON(postFix, function (data) {
    //$.getJSON(urlOfFile, function (data) {
    $.get(localFile, function (csv) {
        console.log(data)
        Highcharts.chart("container", {
            chart: {
                zoomType: "x"
            },
            title: {
                text: "Date of self update"
            },
            subtitle: {
                text: document.ontouchstart === undefined ?
                    "Click and drag in the plot area to zoom in" : "Pinch the chart to zoom in"
            },
            xAxis: {
                type: "datetime"
            },
            yAxis: {
                title: {
                    text: "Seconds"
                }
            },
            legend: {
                enabled: false
            },
            data: {
                csv: csv
            },
            plotOptions: {
                area: {
                    fillColor: {
                        linearGradient: {
                            x1: 0,
                            y1: 0,
                            x2: 0,
                            y2: 1
                        },
                        stops: [
                            [0, Highcharts.getOptions().colors[0]],
                            [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get("rgba")]
                        ]
                    },
                    marker: {
                        radius: 2
                    },
                    lineWidth: 2,
                    states: {
                        hover: {
                            lineWidth: 1
                        }
                    },
                    threshold: null
                }
            },
            series: [{
                type: "area",
                name: "Seconds",
                data: data
            }]
        });
    });
}

function fillArray(url){
    // This function will fill the array with some data collected on url
    // With a json formating
    // Getting raw data
    var rawData = "";
    var splitedData = [];
    // Parsing it and inserting it inside the array
    for (var i = splitedData.length - 1; i >= 0; i--) {
    }
}