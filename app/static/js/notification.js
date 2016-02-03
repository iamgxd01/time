/**
 * Created by Administrator on 1/30/2016.
 */

(function ($, windows, i) {


    function get_notification() {


        $.ajax({
            url: '' + '/get_notification',
            type: 'POST',
            data: {
                value: 'notifications',
            },
            success: function (data) {
                console.log(data.notifications.length)
                if (data.notifications.length > 0) {
                    for (i = 0; i < data.notifications.length; i++) {
                        showNotification(data.notifications[i].title, data.notifications[i].body)
                        console.log('title' + data.notifications[i].title)
                    }
                }
            },
            error: function () {
                console.log('获取task通知数据失败')
            }
        })

    }


    function showNotification(title, body) {
        if (window.Notification) {
            console.log(Notification.requestPermission)
            if (Notification.permission == 'granted') {
                // note the show()
                var options = {
                    body: body,
                    icon: "Notification.jpg"
                };
                var notification = new Notification(title, options);
                // 控制通知显示多长时间消失
                //notification.onshow = function () {
                //    setTimeout(function () {
                //        notification.close();
                //    }, 2000);
                //};
            }
            else {
                Notification.requestPermission();
            }

        } else {
            alert('请下载最新的chrome浏览器体检该功能')
        }

    }

    //获得通知的权限
    Notification.requestPermission();

    // 定时通知
    setInterval(get_notification, 60000);//1000为1秒钟
})(jQuery, this, 0);