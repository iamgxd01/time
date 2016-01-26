//相当于在页面中的body标签加上onload事件
$(function(){
    //找到所有的td节点
    var tds=$("td");
    //给所有的td添加点击事件
    tds.click(function(){
        //获得当前点击的对象
        var td=$(this);
        //取出当前td的文本内容保存起来
        var oldText=td.text();
        //建立一个文本框，设置文本框的值为保存的值   
        var input=$("<input type='text' value='"+oldText+"'/>"); 
        //将当前td对象内容设置为input
        td.html(input);
        //设置文本框的点击事件失效
        input.click(function(){
            return false;
        });
        //设置文本框的样式
        input.css("border-width","0");              
        input.css("font-size","16px");
        input.css("text-align","center");
        //设置文本框宽度等于td的宽度
        input.width(td.width());
        //当文本框得到焦点时触发全选事件  
        input.trigger("focus").trigger("select"); 
        //当文本框失去焦点时重新变为文本
        input.blur(function(){
            var input_blur=$(this);
            //保存当前文本框的内容
            var newText=input_blur.val(); 
            td.html(newText); 
        }); 
        //响应键盘事件
        input.keyup(function(event){
            // 获取键值
            var keyEvent=event || window.event;
            var key=keyEvent.keyCode;
            //获得当前对象
            var input_blur=$(this);
            switch(key)
            {
                case 13://按下回车键，保存当前文本框的内容
                    var newText=input_blur.val(); 
                    td.html(newText); 
                break;
                
                case 27://按下esc键，取消修改，把文本框变成文本
                    td.html(oldText); 
                break;
            }
        });
    });
});
