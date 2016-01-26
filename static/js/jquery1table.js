/*! editTable v0.2.0 by Alessandro Benoit */
(function ($, window, i) {

    'use strict';

    $.fn.editTable = function (options) {

        // Settings
        var s = $.extend({
                data: [['']],
                tableClass: 'inputtable',
                jsonData: false,
                headerCols: false,
                maxRows: 999,
                first_row: true,
                row_template: false,
                field_templates: false,
                nav_templates:false,
                list_id:false,
                date:false,
                validate_field: function (col_id, value, col_type, $element) {
                    return true;
                }
            }, options),
            $el = $(this),
            defaultTableContent = '<thead><tr></tr></thead><tbody></tbody>',
            $table = $('<table/>', {
                class: s.tableClass + ((s.first_row) ? ' wh' : ''),
                html: defaultTableContent
            }),
            defaultth = '<th><a class="addcol icon-button" href="#">+</a> <a class="delcol icon-button" href="#">-</a></th>',
            colnumber,
            rownumber,
            reset,
            is_validated = true;

        // Increment for IDs
        i = i + 1;

        // Build cell
        function buildCell(content,name, type) {
            content = (content === 0) ? "0" : (content || '');
            // Custom type
            //if (type && 'text' !== type){
            //    var field = s.field_templates[type];
            //    return '<td>' + field.setValue(field.html, content)[0].outerHTML + '</td>';
            //}
            // Default
            if(type == 'textarea' ){
                 var  textarea =  '<td><textarea name = "'+name+'" type="text"> '+ content.toString().replace(/"/g, "&quot;") + '</textarea></td>'
                 //$(textarea).innerText="nihao"
                return textarea
            }



            //return '<td><textarea name = "'+name+'" type="text" value="" />nihao</td>';
            return '<td><input name = "'+name+'" type="text" value="' + content.toString().replace(/"/g, "&quot;") + '" /></td>';
        }

        // Build row
        function buildRow(data, len,id) {

            var rowcontent = '', b;

            data = data || '';

            if (!s.row_template) {
                // Without row template


                for (b = 0; b < (len || data.length); b += 1) {

                    if(b==0){
                        rowcontent += buildCell(id,'id');
                    }
                     else if(b==1){
                        rowcontent += buildCell(data.start_time,'start_time');
                    }else if(b==2){
                        rowcontent += buildCell(data.taskname,'taskname','textarea');
                    }
                    //else if (b==3){
                    //    if (data.lists != null){
                    //         rowcontent += buildCell(data.lists.listname,'listname')
                    //    }
                    //    else{
                    //         rowcontent += buildCell('','listname')
                    //    }
                    //
                    //}
                    else if(b==3){
                        rowcontent+= buildCell(data.thought,'thought','textarea');
                    }
                    else if(b==4){
                        rowcontent+= buildCell(data.scheduled_time,'scheduled_time');
                    } else if(b==5){
                        rowcontent += buildCell(data.efficiency,'efficiency');
                    } else if(b==6){
                        rowcontent +=buildCell(data.summary,'summary','textarea');
                    } else if(b==7) {
                        rowcontent += buildCell(data.end_time,'end_time');
                    } else if(b==8){
                        rowcontent+= buildCell(data.actual_time,'actual_time');
                    }
                }


            } else {
                // With row template
                for (b = 0; b < s.row_template.length; b += 1) {
                    // For each field in the row
                    rowcontent += buildCell(data[b], s.row_template[b]);
                }
            }

            //return $('<tr />', {
            //    html: rowcontent + '<td><a class="addrow icon-button" href="#">+</a> <a class="delrow icon-button" href="#">-</a></td>'
            //});
            var before_tr = '<tr id=" ">'
            var behind_tr ='</tr>'
            var  button  =  '<td><a class="addrow icon-button" href="#">+</a> <a class="delrow icon-button" href="#">-</a></td>'


             return $(before_tr + rowcontent + button + behind_tr)


        }

        function  getdate(){
            s.date = $('#datetimepicker input').val()
        }


         // build templatemo-left-nav
        function buildNav(data){

              var nav =''
              if(s.list_id==data.id){
                  //  选中当前的清单
                  nav =  '<li><a href="/tasks/'+data.listname+'?date='+ s.date+'" id="'+data.id+'",onclick="getdate()",class = "actived" style="background:  #18191b;border-left: 8px solid #13895F"}}"><i class="fa fa-home fa-fw"></i>'+data.listname+'</a></li>'
              }else {
                  nav =  '<li><a href="/tasks/'+data.listname+'?date='+ s.date+'" id="'+data.id+'" }}"><i class="fa fa-home fa-fw"></i>'+data.listname+'</a></li>'
              }




              return  nav
        }




        // Check button status (enable/disabled)
        function checkButtons() {
            if (colnumber < 2) {
                $table.find('.delcol').addClass('disabled');
            }
            if (rownumber < 2) {
                $table.find('.delrow').addClass('disabled');
            }
            if (s.maxRows && rownumber === s.maxRows) {
                $table.find('.addrow').addClass('disabled');
            }
        }

        // Fill table with data
        function fillTableData(data) {

            var a, crow = Math.min(s.maxRows, data.length);

            // Clear table
            $table.html(defaultTableContent);

            // If headers or row_template are set
            if (s.headerCols || s.row_template) {

                // Fixed columns
                var col = s.headerCols || s.row_template;

                // Table headers
                for (a = 0; a < col.length; a += 1) {
                    var col_title = s.headerCols[a] || '';
                    $table.find('thead tr').append('<th>' + col_title + '</th>');
                }

                // Table content
                for (a = 0; a < crow; a += 1) {
                    // For each row in data
                     buildRow(data[a], col.length,a+1).appendTo($table.find('tbody'));

                }

                // nav content
                // 创建全部类型
                 $('.templatemo-left-nav ul ').append( '<li><a href="/tasks/全部?date='+ s.date+'" id="" }}"><i class="fa fa-home fa-fw"></i>全部</a></li>')
                for (i =0;i<list_data.length;i++){
                    $('.templatemo-left-nav ul ').append(buildNav(list_data[i]))
                }
                // 添加创建清单
                  $('.templatemo-left-nav ul ').append( '<li><a href="#"><i class="fa fa-home fa-fw"></i>创建清单</a></li>')



                // 为 tbody tr  中的id 赋值
                // id 用来存储task_id 的值

                for(i=0;i<crow;i++){
                        //$table.find('tbody').find('tr:eq('+i+')').attr('id',data[i].id)
                        $table.find('tbody').find('tr:eq('+i+')').attr('id',data[i].id)
                  }

                // 生成最小行数
                var default_row_count =10
                if(crow < default_row_count ){
                    data =[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
                    for (a = 0; a < default_row_count-crow; a += 1) {
                        buildRow(data).appendTo($table.find('tbody'));
                    }
                }

            } else if ( data[0] ) {

                // Variable columns
                for (a = 0; a < data[0].length; a += 1) {
                    $table.find('thead tr').append(defaultth);
                }

                for (a = 0; a < crow; a += 1) {

                    buildRow(data[a]).appendTo($table.find('tbody'));

                }

            }

            // Append missing th
            $table.find('thead tr').append('<th></th>');

            // Count rows and columns
            colnumber = $table.find('thead th').length - 1;
            rownumber = $table.find('tbody tr').length;

            checkButtons();
        }

        // Export data
        function exportData() {
            var row = 0, data = [], value;

            is_validated = true;

            $table.find('tbody tr').each(function () {

                row += 1;
                data[row] = [];

                $(this).find('td:not(:last-child)').each(function (i, v) {
                    if ( s.row_template && 'text' !== s.row_template[i] ){
                        var field = s.field_templates[s.row_template[i]],
                            el = $(this).find($(field.html).prop('tagName'));
                        
                        value = field.getValue(el);
                        if ( !s.validate_field(i, value, s.row_template[i], el) ){
                            is_validated = false;
                        }
                        data[row].push(value);
                    } else {
                        value = $(this).find('input[type="text"]').val();
                        if ( !s.validate_field(i, value, 'text', v) ){
                            is_validated = false;
                        }
                        data[row].push(value);
                    }
                });
                
            });

            // Remove undefined
            data.splice(0, 1);

            return data;
        }

        // Fill the table with data from textarea or given properties
        if ($el.is('textarea')) {

            try {
                reset = JSON.parse($el.val());
            } catch (e) {
                reset = s.data;
            }

            $el.after($table);

            // If inside a form set the textarea content on submit
            if ($table.parents('form').length > 0) {
                $table.parents('form').submit(function () {
                    $el.val(JSON.stringify(exportData()));
                });
            }

        } else {


            reset = (JSON.parse(s.jsonData) || s.data);
            //reset = (s.jsonData || s.data);

            $el.append($table);
        }

        fillTableData(reset);

            // 保存 input 数据
        $table.on('change','tbody tr input',function(){
            var tr_task_id = $(this).closest('tr')

            $.ajax({
                url:''+'/addtask',
                type: 'POST',
                data: { value: $(this).val(),
                        name: $(this).attr('name'),
                        task_id:tr_task_id.attr('id'),
                        list_id: s.list_id,
                        task_date:  $('#datetimepicker input').val()
                },
                success: function(data){
                    tr_task_id.attr('id',data.task_id)
                    console.log('taskid'+data.task_id)
                    if(data.status=='false')
                     alert('此清单不存在')
                },
                error: function(){

                    console.log('task数据保存失败')
                }

            })

        })

        // 保存textarea 数据
           $table.on('change','tbody tr textarea',function(){
                 var tr_task_id = $(this).closest('tr')
            $.ajax({
                url:''+'/addtask',
                type: 'POST',
                data: { value: $(this).val(),
                        name: $(this).attr('name'),
                        task_id:tr_task_id.attr('id'),
                        list_id: s.list_id,
                        task_date: $('#datetimepicker input').val()
                },
                success: function(data){
                    tr_task_id.attr('id',data.task_id)
                    console.log('taskid'+data.task_id)
                    if(data.status=='false')
                     alert('此清单不存在')
                },
                error: function(){

                    console.log('task数据保存失败')
                }

            })

        })

        // Add column

        $table.on('click','.addcol',function(){

       //$table.find(".addcol").bind('click',function(){
           // 获取列的值
           // 用closest获得行，children 获得行的所有子元素
            var colid = parseInt($(this).closest('tr').children().index($(this).parent('th')), 10);
            alert("列值"+colid);

            colnumber += 1;

            $table.find('thead tr').find('th:eq(' + colid + ')').after(defaultth);

            $table.find('tbody tr').each(function () {
                $(this).find('td:eq(' + colid + ')').after(buildCell());
            });

            $table.find('.delcol').removeClass('disabled');

            return false;
        })

        // 点击清单时传递日期给后台
        var length = $('.templatemo-left-nav  ul a').length
        $('.templatemo-left-nav  ul ').on('click','a:lt('+length+')',function(){

            var  list_id = $(this).attr('id')
            var  calender_date = $('#datetimepicker input').val()
            console.log('list_id'+calender_date)

             $.ajax({
                url:''+'/tasks/'+list_id+'',
                type: 'POST',
                data: {
                        calender_date: $('#datetimepicker input').val()
                },
                success: function(data){

                     //alert('成功')
                },
                error: function(){

                    console.log('task数据保存失败')
                }

            })



        })

        //  格式校验

        //$table.find('tbody tr td input[name="start_time"] ').bind('click',function(){
        //    console.log('id'+ $(this).attr('name'))
        //
        //})
        var start_time =  $table.find('tbody tr td input[name="start_time"] ')
            $("#form").validate({
           rules:{
                    //username:{ minlength:6 },
                    start_time:{ rangelength:[2,3] },

                },
            messages:{
                    //username: "budui",
                    start_time:"shijiangeshibudui",
            },
            onsubmit:false,
            focusCleanup:true,
            onkeyup:false,
            success:function(lable) {
                //lable.parents(".tip").remove()
                $("#error").remove()
            },

                /*错误提示位置*/
                errorPlacement:function(error,element){
                    console.log('错误')
                    if($("#error").length>0){
                          $("#error").remove()
                    }
                    $('#form').before('<p id = "error"></p>')
                    error.appendTo($("#error"));

                    //error.append(element)

                }

         })



        //$table.on('change',,function(){
        //
        //
        //})






        // Remove column
         $table.on('click','.delcol',function(){
        //$table.find(".delcol").bind('click',function(){
            if ($(this).hasClass('disabled')) {
                return false;
            }

            var colid = parseInt($(this).closest('tr').children().index($(this).parent('th')), 10);

            colnumber -= 1;

            checkButtons();

            $(this).parent('th').remove();

            $table.find('tbody tr').each(function () {
                $(this).find('td:eq(' + colid + ')').remove();
            });

            return false;
        });
        // 自定义添加

        // Add row
        $table.on('click','.addrow',function(){
        //$table.find(".addrow").bind('click',function(){
            if ($(this).hasClass('disabled')) {
                return false;
            }


            rownumber += 1;

            $(this).closest('tr').after(buildRow(0, colnumber));

            $table.find('.delrow').removeClass('disabled');

            checkButtons();

            return false;
        });


        // Delete row
         $table.on('click','.delrow',function(){
        //$table.find(".delrow").bind('click',function(){


             $.ajax({
                url:''+'/deletetask',
                type: 'POST',
                data: {
                        task_id:$(this).closest('tr').attr('id')
                },
                success: function(){
                     //alert('删除成功')
                },
                error: function(){
                    console.log('task数据删除失败')
                }

            })

            if ($(this).hasClass('disabled')) {
                return false;
            }

            rownumber -= 1;

            checkButtons();

            $(this).closest('tr').remove();

            $table.find('.addrow').removeClass('disabled');

            return false;
        });

        // Select all content on click
         $table.find("input").bind('click',function(){
            $(this).select();
        });




        // Return functions
        return {
            // Get an array of data
            getData: function () {
                return exportData();
            },
            // Get the JSON rappresentation of data
            getJsonData: function () {
                return JSON.stringify(exportData());
            },
            // Load an array of data
            loadData: function (data) {
                fillTableData(data);
            },
            // Load a JSON rappresentation of data
            loadJsonData: function (data) {
                fillTableData(JSON.parse(data));
            },
            // Reset data to the first instance
            reset: function () {
                fillTableData(reset);
            },
            isValidated: function () {
                return is_validated;
            }
        };
    };


})(jQuery, this, 0);