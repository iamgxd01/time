$(document).ready(function(){
    var tds=$("td");
    tds.click(tdclick);
});
function tdclick(){
         var td=$(this);
         //1,ȡ����ǰtd�е��ı����ݱ�������
        var text=td.text();
        //2,���td���������
        td.html(""); //Ҳ������td.empty();
        //3������һ���ı���Ҳ����input��Ԫ�ؽڵ�
        var input=$("<input>");
        //4�������ı����ֵ�Ǳ����������ı�����
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
        //5�����ı�����뵽td��
        td.append(input);       //Ҳ������input.appendTo(td);
       //6,�������¼�
        td.unbind("click");
}






























