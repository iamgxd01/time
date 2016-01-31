/**
 * Created by Administrator on 1/30/2016.
 */

(function ($,windows,i) {


    function get_notification(){

        $.ajax({
            url:''+'/get_notification',
            type: 'POST',
            data: { value: 'notifications',
            },
            success: function(data){
                console.log(data.notifications.length)
                if(data.notifications.length>0){
                    showNotification(data.notifications[0].title,data.notifications[0].body)
                    console.log('title'+data.notifications[0].title)
                }

            },
            error: function(){

                console.log('task数据保存失败')
            }

        })

    }




    function myInterval()
         {
            alert('aaaaaaaaa');
         }
    function showNotification(title,body) {
        if(window.Notification){
            console.log(Notification.requestPermission)


            if (Notification.permission == 'granted') {
                // note the show()
                var options={
                body:body,
                icon:"Notification.jpg"
            };
                var notification = new Notification(title,options);
                     notification.onshow = function () {
                      setTimeout(function () {
                      notification.close();
                      }, 3000);
                 };
            }
            else{
                 Notification.requestPermission();
            }

        }else {
            alert('请下载最新的chrome浏览器体检该功能')
        }

    }

     //获得通知的权限

     Notification.requestPermission();

    // 定时通知
     setInterval(get_notification,2000);//1000为1秒钟
     //setInterval(myInterval,2000);//1000为1秒钟
})(jQuery, this, 0);