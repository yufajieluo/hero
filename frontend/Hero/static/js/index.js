$(function(){
    $('.get_code').on(
        'click', function(){
            var register_account=$('#register_account').val();
            $.ajax({
                url:'/hero/user/captcha/',
                type:'get',
                data:{'register_account':register_account},
                dataType:'json',
                success:function(resp){
                    if(resp.rsp_head.rsp_code!=200){
                        alert(resp.rsp_head.rsp_info)
                    }else{
                        alert('验证码已发送至邮箱')
                    }
                }
            })
        }
    );

    $('#logout').on(
        'click', function(){
            $.ajax({
                url: '/hero/user/logout/',
                type: 'post',
                data: {},
                success: function(resp){
                    window.location.href="/hero/"
                }
            })
        }
    );

    $('#button_submit').on(
        'click', function(){
            var account = $('#current_account').html();
            var old_pass = $('#old_password').val();
            var new_pass = $('#new_password').val();
            $.ajax({
                url: '/hero/user/password/',
                type: 'post',
                data: {'original_password': old_pass, 'new_password': new_pass, 'account': account},
                success: function(resp){
                    alert(resp.rsp_head.rsp_info)
                }
            })
        }
    );

    $('.btnResetPass').on('click',function(){
        $(this).attr('data-value',1).parents('tr').siblings().find("[data-toggle='modal']").attr('data-value',2);
    });

    $('#button_reset_pass').on(
        'click', function(){
            var account = $('[data-value=1]').parents('tr').find('td:first-child').text();
            $.ajax({
                url: '/hero/user/password/',
                type: 'delete',
                data: {'account': account},
                success: function(resp){
                    alert(resp.rsp_head.rsp_info)
                    window.location.href = '/hero/user/'
                },
                error: function(){
                    $('.resetPass').on(
                        'hide.bs.modal', function(){
                            $(this).removeData()
                        }
                    )
                }
            })
        }
    );

    $('.button_allot_role').on(
        'click', function(){
            $(this).attr('data-value',1).parents('tr').siblings().find("[data-toggle='modal']").attr('data-value',2);
            var user_account = $('[data-value=1]').parents('tr').find('td:nth-child(1)').text();
            var user_name = $('[data-value=1]').parents('tr').find('td:nth-child(2)').text();
            $.ajax(
                {
                    url: '/hero/user/',
                    type: 'get',
                    data: {'account': user_account},
                    success: function(resp){
                        $('#user_role').empty()
                        $('#user_role').append('<option></option>')
                        if(resp.rsp_head.rsp_code == 200){
                            $('#user_account').val(user_account)
                            $('#user_name').val(user_name)
                            roles = resp.rsp_body.roles
                            user_role = resp.rsp_body.user.role
                            $.each(
                                roles,
                                function(i, d){
                                    if(user_role == roles[i].name){
                                        var option = '<option selected>' + roles[i].name + '</option>'
                                    }else{
                                        var option = '<option>' + roles[i].name + '</option>'
                                    }
                                    $('#user_role').append(option)
                                }
                            )
                        }
                    }
                }
            )
        }
    );

    $('#button_set_role').on(
        'click', function(){
            var user_account = $('#user_account').val()
            var user_role = $('#user_role').val()
            $.ajax({
                url: '/hero/user/',
                type: 'post',
                data: {'user_account': user_account, 'user_role': user_role},
                success: function(resp){
                    alert(resp.rsp_head.rsp_info)
                    window.location.href = '/hero/user/'
                },
                error: function(){
                    $('.resetPass').on(
                        'hide.bs.modal', function(){
                            $(this).removeData()
                        }
                    )
                }
            })
        }
    );


    $('.btnGetRole').on(
        'click', function(){
            $(this).attr('data-value',1).parents('tr').siblings().find("[data-toggle='modal']").attr('data-value',2);
            var role_name = $('[data-value=1]').parents('tr').find('td:nth-child(2)').text();
            $.ajax(
                {   
                    url: '/hero/role/',
                    type: 'get',
                    data: {'role_name': role_name},
                    success: function(resp){
                        if(resp.rsp_head.rsp_code == 200){
                            $('#show_role_name').val(resp.rsp_body.role.name)
                            $('#show_role_level').val(resp.rsp_body.role.level)
                            $('#show_role_desc').val(resp.rsp_body.role.description)
                            $('#show_role_users').val(resp.rsp_body.role.users)
                            $('#show_role_permissions').val(resp.rsp_body.role.permissions)
                        }
                    }
                }
            )
        }
    );

    $('.btnAllotPermission').on(
        'click', function(){
            $(this).attr('data-value',1).parents('tr').siblings().find("[data-toggle='modal']").attr('data-value',2);
            var role_name = $('[data-value=1]').parents('tr').find('td:nth-child(2)').text();
            $.ajax(
                {
                    url: '/hero/role/permission/',
                    type: 'get',
                    data: {'role_name': role_name},
                    success: function(resp){
                        fillTree(resp.rsp_body.permissions)
                    }
                }
            )
        }
    );

    $('#button_allot_permission').on(
        'click', function(){
            var role_name = $('[data-value=1]').parents('tr').find('td:nth-child(2)').text();
            var permission = tree_datas
            $.ajax(
                {
                    url: '/hero/role/permission/',
                    type: 'post',
                    traditional: true,
                    data: {'role_name': role_name, 'permission': permission},
                    success: function(resp){
                        alert(resp.rsp_head.rsp_info)
                        window.location.href = '/hero/role/'
                    },
                    error: function(){
                        $('.allotPermission').on(
                            'hide.bs.modal', function(){
                                $(this).removeData()
                            }
                        )
                    }
                }
            )
        }
    );



    $('#add_permission').on(
        'click', function(){
            $.ajax({
                url: '/hero/resource/',
                type: 'get',
                dataType: 'json',
                data: {},
                success:function(resp){
                    if(resp.rsp_head.rsp_code == 200){
                        var root_permissions = resp.rsp_body.permissions
                        $('#permission_superior').empty()
                        $('#permission_superior').append('<option>ROOT</option>')
                        $.each(
                            root_permissions,
                            function(i, d){
                                var option = '<option>' + root_permissions[i].name + '</option>'
                                $('#permission_superior').append(option)
                            }
                        )
                    }
                }
           })
        }
    );

    $('#button_add_permission').on(
        'click', function(){
            var data = {
                'name': $('#permission_name').val(),
                'desc': $('#permission_desc').val(),
                'url': $('#permission_url').val(),
                'superior': $('#permission_superior').val()
            }
            $.ajax({
                url: '/hero/permission/',
                type: 'put',
                dataType: 'json',
                data: data,
                success:function(resp){
                    alert(resp.rsp_head.rsp_info)
                    window.location.href = '/hero/permission/'
                }
           })
        }
    );

    $('.btnModifyPermission').on(
        'click', function(){
            $(this).attr('data-value',1).parents('tr').siblings().find("[data-toggle='modal']").attr('data-value',2);
            var permission_name = $('[data-value=1]').parents('tr').find('td:nth-child(1)').text();
            $.ajax(
                {
                    url: '/hero/permission/',
                    type: 'get',
                    data: {'permission_name': permission_name},
                    success: function(resp){
                        if(resp.rsp_head.rsp_code == 200){
                            $('#md_permission_name').val(resp.rsp_body.permission.name)
                            $('#md_permission_desc').val(resp.rsp_body.permission.description)
                            $('#md_permission_url').val(resp.rsp_body.permission.url)
                            $('#md_permission_superior').empty()
                            $('#md_permission_superior').append('<option>ROOT</option>')
                            var root_permissions = resp.rsp_body.permission.root_permissions
                            $.each(
                                root_permissions,
                                function(i, d){
                                    var option = '<option>' + root_permissions[i] + '</option>'
                                    $('#md_permission_superior').append(option)
                                }
                            )
                            $('#md_permission_superior').val(resp.rsp_body.permission.superior)
                        }
                    }
                }
            )
        }
    );

    $('#button_modify_permission').on(
        'click', function(){
            var data = {
                'name': $('#md_permission_name').val(),
                'desc': $('#md_permission_desc').val(),
                'url': $('#md_permission_url').val(),
                'superior': $('#md_permission_superior').val()
            }
            $.ajax({
                url: '/hero/permission/',
                type: 'post',
                dataType: 'json',
                data: data,
                success:function(resp){
                    alert(resp.rsp_head.rsp_info)
                    window.location.href = '/hero/permission/'
                }
           })
        }
    );

    $(".btnRemovePermission").on(
        'click',function(){
            $(this).attr('data-value',1).parents('tr').siblings().find("[data-toggle='modal']").attr('data-value',2);
        }
    );
    
            
    $('#button_remove_permission').on(
        'click', function(){
            var permission_name = $('[data-value=1]').parents('tr').find('td:nth-child(1)').text();
            $.ajax(
                {
                    url: '/hero/permission/',
                    type: 'delete',
                    data: {'permission_name': permission_name},
                    success: function(resp){
                        alert(resp.rsp_head.rsp_info)
                        window.location.href = '/hero/permission/'
                    }
                }
            )
        }
    );

});


function repass_verify(){
   var pwd1 = $("#register_password").val();
   var pwd2 = $("#repeat_password").val();
   var info = "";
   if (pwd1 == pwd2) {
       $("#submit_register").prop('disabled', false);
   }
   else {
       info = "<font color='red'>两次密码不相同</font>";
       $("#submit_register").prop('disabled', true);
   }
   $("#verify").html(info);
}

function modify_pass_verify(){
   var pwd1 = $("#new_password").val();
   var pwd2 = $("#repeat_password").val();
   var info = "";
   if (pwd1 == pwd2) {
       $("#button_submit").prop('disabled', false);
   }
   else {
       info = "<font color='red'>两次密码不相同</font>";
       $("#button_submit").prop('disabled', true);
   }
   $("#verify").html(info);
}

function S4() {
   return (((1+Math.random())*0x10000)|0).toString(16).substring(1);
}

function guid() {
   return (S4()+S4()+"-"+S4()+"-"+S4()+"-"+S4()+"-"+S4()+S4()+S4());
}

function fill_page(fooler, current_page, ceiling) {
    for (index = fooler; index < current_page; index++) {
        $('.pagination').append(
            '<li><a href="?page=' + index + '">' + index + '</a></li>'
        )
    }
    $('.pagination').append(
        '<li class="active"><a href="?page=' + current_page + '">' + current_page + '</a></li>'
    )
    for (index = current_page + 1; index < ceiling + 1; index++) {
        $('.pagination').append(
            '<li><a href="?page=' + index + '">' + index + '</a></li>'
        )
    }
}

function jump_page() {
    var e = window.event;
    if(e.keyCode == 13){
        target_page = $('#jump_target_page').val()
        console.log(target_page)
        window.location.href = "?page=" + target_page
    }
}

$('tbody tr td').on(
    'mouseover',function () {
        var indexTd=$(this).index();
        $(this).parent().css('background','#d1e1ed').siblings().css('background','none');
        /*$('tbody tr').each(function () {
            $(this).find('td:eq('+indexTd+')').css('background','#d1e1ed').siblings().css('background','none');
        });*/
    }
);
