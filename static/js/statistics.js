/**
 * Created by Administrator on 1/28/2016.
 */
(function ($,windows,i) {

    $.fn.statistics = function (datajsons) {

        function time_to_hour_and_minute(time_int){
            var hour = parseInt(time_int/60)
            var minute = parseInt(time_int%60)
            if(hour==0){
                return minute+'分钟'
            }
            else {
                return hour +'小时'+minute+'分钟'
            }
        }


        function bulid_rows(data){
            console.log(data)
            var before_tr = '<tr id=" " value ="11">'
            var td1 = '<td  <p>   '+data.listname+'</p> </td> '
            var td2 = '<td <p>  '+time_to_hour_and_minute(data.time_sum)+'</p> </td> '
            var behind_tr ='</tr>'
            return $(before_tr+td1+td2+behind_tr)

        }
        var color_list =['#89A54E','#F38630','#AA4643','#80699B','#3D96AE','#DB843D','#92A8CD','#A47D7C','#B5CA92',
            '#4572A7','#AA4643','#89A54E','#80699B','#3D96AE','#DB843D','#92A8CD','#A47D7C','#B5CA92',
            '#4572A7','#AA4643','#89A54E','#80699B','#3D96AE','#DB843D','#92A8CD','#A47D7C','#B5CA92',
            '#4572A7','#AA4643','#89A54E','#80699B','#3D96AE','#DB843D','#92A8CD','#A47D7C','#B5CA92',
        ]
        var data = []
        var time_sum =0
        for(i=0; i< datajsons.length;i++ ){
            bulid_rows(datajsons[i]).appendTo($('#list_time_sum tbody'))
            data_dict = {
                value:datajsons[i].time_sum ,
                color:color_list[i]

            }
            time_sum = time_sum+parseInt(datajsons[i].time_sum)
            data.push(data_dict)

        }
    // 显示总时长
        console.log(time_sum)
        $('.p_right').text(time_to_hour_and_minute(time_sum))

    //  制作图表
        var ctx = $("#myChart").get(0).getContext("2d");

        //var data = [
        //    {
        //        value: 30,
        //        color:"#F38630"
        //    },
        //    {
        //        value : 50,
        //        color : "#E0E4CC"
        //    },
        //    {
        //        value : 100,
        //        color : "#69D2E7"
        //    }
        //]
        var options = {
            //Boolean - Whether we should show a stroke on each segment
            segmentShowStroke : true,

            //String - The colour of each segment stroke
            segmentStrokeColor : "#fff",

            //Number - The width of each segment stroke
            segmentStrokeWidth : 2,

            //Boolean - Whether we should animate the chart
            animation : true,

            //Number - Amount of animation steps
            animationSteps : 100,

            //String - Animation easing effect
            animationEasing : "easeOutBounce",

            //Boolean - Whether we animate the rotation of the Pie
            animateRotate : true,

            //Boolean - Whether we animate scaling the Pie from the centre
            animateScale : false,

            //Function - Will fire on animation completion.
            onAnimationComplete : null
        }
        //new Chart(ctx).PolarArea(data,options);
           new Chart(ctx).Pie(data,options);

         function myInterval()
         {
            alert('aaaaaaaaa');
         }
        //setInterval(myInterval,2000);//1000为1秒钟




    }

})(jQuery, this, 0);
