$(document).ready(function(){
    var tds=$("td");
    tds.click(tdclick);
});
function tdclick(){
         var td=$(this);
         //1,取出当前td中的文本内容保存起来
        var text=td.text();
        //2,清空td里面的内容
        td.html(""); //也可以用td.empty();
        //3，建立一个文本框，也就是input的元素节点
        var input=$("<input>");
        //4，设置文本框的值是保存起来的文本内容
        input.attr("value",text);
        input.keyup(function(event){
             var myEvent =event||window.event;
             var kcode=myEvent.keyCode;
            if(kcode==13){
                var inputnode=$(this);
                var inputtext=inputnode.val();
                var tdNode=inputnode.parent();
                tdNode.html(inputtext);
                tdNode.click(tdclick);
            }
        });
        //5，将文本框加入到td中
        td.append(input);       //也可以用input.appendTo(td);
       //6,清楚点击事件
        td.unbind("click");
}






























