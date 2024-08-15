// Global variable to store the chart instance
var myChart;
var temp_list = [];
var humid_list = [];
var shock_list = [];
var light_list = [];
var time_labels = [];

function create_time(start) {
    time_labels.push(start)
    console.log(time_labels)
}

function filter_actions(id) {
    var button_option = id;
    console.log(button_option);

    window.chartColors = {
        red: 'rgb(255, 99, 132)',
        orange: 'rgb(255, 159, 64)',
        yellow: 'rgb(255, 205, 86)',
        green: 'rgb(75, 192, 192)',
        blue: 'rgb(54, 162, 235)',
        purple: 'rgb(153, 102, 255)',
        grey: 'rgb(201, 203, 207)'
    };

    var rm1 = true;
    var rm2 = true;
    var rm3 = true;
    var rm4 = true;

    if (button_option == 'option1') {
        rm2 = false;
        rm3 = false;
        rm4 = false
    } else if (button_option == 'option2') {
        rm1 = false;
        rm3 = false;
        rm4 = false;
    } else if (button_option == 'option3') {
        rm1 = false;
        rm2 = false;
        rm4 = false;
    } else if (button_option == 'option4') {
        rm1 = false;
        rm2 = false;
        rm3 = false;
    } 

    graph_data = []
    if (rm1) {
        graph_data.unshift({
            data: temp_list,
            label: "Temperature",
            backgroundColor: window.chartColors.red,
            borderWidth: 2
        })
    }
    if (rm2) {
        graph_data.unshift({
            data: humid_list,
            label: "Humidity",
            backgroundColor: window.chartColors.green,
            borderWidth: 2
        })
    }
    if (rm3) {
        graph_data.unshift({
            data: shock_list,
            label: "Shock",
            backgroundColor: window.chartColors.purple,
            borderWidth: 2
        })
    }
    if (rm4) {
        graph_data.unshift({
            data: light_list,
            label: "Light",
            backgroundColor: window.chartColors.yellow,
            borderWidth: 2
        })
    }

    var val_list = []
    var max = 0
    var min = 300
    var max_index = 0
    var min_index = 0
    for (var i=0; i<24; i++) {
        val = 0
        if (rm1) {val += temp_list[i]}
        if (rm2) {val += humid_list[i]}
        if (rm3) {val += shock_list[i]}
        if (rm4) {val += light_list[i]}
        val_list.push(val)
        if (val > max) {
            max = val
            max_index = i
        }
        if (val < min) {
            min = val
            min_index = i
        }
    }
    max_min_points = [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
    max_min_points[max_index] = 10
    max_min_points[min_index] = 10

    graph_data.unshift({
        label:"",
        data: val_list,
        borderColor: window.chartColors.blue,
        borderWidth: 2,
        fill: false,
        type: 'line',
        pointRadius: max_min_points
    })

    // Assuming you have a function to update the chart data
    updateChartData(graph_data);

    return [max, max_index, min, min_index]
}

function updateChartData(graph_data) {
    if (myChart) {
        // Update existing chart with new data
        myChart.data.datasets = graph_data;
        myChart.update();
    } else {
        // Create a new chart
        myChart = new Chart(document.getElementById("myCanvas2"), {
            type: 'line',
            data: {
                labels: time_labels,
                datasets: graph_data
            },
            borderColor: window.chartColors.blue,
        borderWidth: 2,
        fill: false,
        type: 'line',
        pointRadius: max_min_points,
            options: {
                title: {
                    display: true,
                    text: 'Perishervation'
                },
                hover: {
                    mode: 'index',
                    //intersect: true
                },
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true
                        }
                    },
                    y: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Value'
                        },
                        suggestedMax: 10
                    }
                }
            }
        });
    }
}


function create_data(data) {

    for (var i = 0; i<data['feeds'].length; i++) {
     
            time = data['feeds'][i]['created_at']
            const dateObj = new Date(time);
            const utc8Time = new Date(dateObj.getTime() + 8 * 60 * 60 * 1000);
            const formattedTime = utc8Time.toISOString().substr(11, 8);
            create_time(formattedTime)

        correct = false
        if (!isNaN(data['feeds'][i]['field1'])){
            if (data['feeds'][i]['field1'] != null){correct = true}
        }

        if (correct) {temp = parseFloat(data['feeds'][i]['field1'])}
        else {temp = 0}
        temp_list.push(temp)

        correct = false
        if (!isNaN(data['feeds'][i]['field2'])){
            if (data['feeds'][i]['field2'] != null){correct = true}
        }

        if (correct) {humid = parseFloat(data['feeds'][i]['field2'])}
        else {humid = 0}
        humid_list.push(humid)

        correct = false
        if (!isNaN(data['feeds'][i]['field3'])){
            if (data['feeds'][i]['field3'] != null){correct = true}
        }

        if (correct) {val = parseFloat(data['feeds'][i]['field3'])}
        else {val = 0}
        shock_list.push(val)

        correct = false
        if (!isNaN(data['feeds'][i]['field4'])){
            if (data['feeds'][i]['field4'] != null){correct = true}
        }

        if (correct) {val = parseFloat(data['feeds'][i]['field4'])}
        else {val = 0}
        light_list.push(val)
    }



    [max, max_index, min, min_index] = filter_actions('option1')

    var avg_temp = 0
    var avg_light = 0
    var avg_shock = 0
    var avg_humid = 0
    var temp_total=0
    var humid_total=0
    var shock_total=0
    var light_total=0
    var total_val = 0

    for (var i = 0; i< temp_list.length; i++) {
        if (humid_list[i] != 0){
            avg_humid += humid_list[i];
            humid_total += 1
        }
        if (temp_list[i] != 0) {
            avg_temp += temp_list[i];
            temp_total += 1
        }
        if (shock_list[i] != 0) {
            avg_shock += shock_list[i];
            shock_total += 1
        }
        if (light_list[i] != 0) {
            avg_light += light_list[i];
            light_total += 1
        }
        total_val += light_list[i]; 
        total_val += humid_list[i]; 
        total_val += shock_list[i]; 
    }
    console.log("TEST")
    console.log(avg_humid, avg_temp)
    console.log(temp_list)
    console.log(humid_list)
    
    if (avg_humid == 0) {
        avg_humid = '-'
    } else {
        avg_humid = (avg_humid/humid_total).toFixed(2)
    }

    if (avg_temp == 0) {
        avg_temp = '-'
    } else {
        avg_temp = (avg_temp/temp_total).toFixed(2)
    }

    if (avg_shock == 0) {
        avg_shock = '-'
    } else {
        avg_shock = (avg_shock/shock_total).toFixed(2)
    }

    if (avg_light == 0) {
        avg_light = '-'
    } else {
        avg_light = (avg_light/light_total).toFixed(2)
    }

    return [avg_temp, avg_humid, avg_shock,avg_light, (max/1000).toFixed(2), max_index, (min/1000).toFixed(2), min_index]

}