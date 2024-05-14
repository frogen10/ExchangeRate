export const chartData = {
        labels:['2024-10-18  23:39:30', '2024-10-19 23:39:30'],
        datasets:[
            {
                label:'Polish Zloty',
                borderColor:["RED"],
                backgroundColor:"RED",
                data:[34, 8, 14, 60, 27, 48, 16, 55, 19, 73, 67, 52, 91, 36, 47, 13, 21, 6, 43, 78, 50, 28, 84, 76],
                fill: false
            }    
        ],
    };
export const options = {
        legend:{
            display:true,
        },
        scales:{
            x:{
                type:'time',
                time:{
                    unit:'hour',
                },
            distribution: 'linear'
            },
            y:{
                beginAtZero:true,
            }
        },
        title:{
            display:true,
            text:"Kursy Walut",
            fontColor:"#111",
            fontSize:50,
            padding:10,
        }
    }
