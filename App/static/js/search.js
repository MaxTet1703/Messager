$(function($){
    var data = null;
    const path_to_page = 'ws://127.0.0.1:8000/ws/main';
    $("#search input.line").keydown(function(event){
        $('.user-list').addClass('d-none');
        $('.loader-wrapper').removeClass("d-none");
        $('.user-list .user').remove();

        var message = $("#search input.line").val();;
        var wb = new WebSocket(path_to_page);
        wb.message = message;
        wb.onopen = send_message;
        wb.onmessage = get_users;
        if (data.length != 0){
            create_user_list();
            add_friend();
        }else{
            $('.user-list p').removeClass('d-none');
        }
        $('.user-list').removeClass('d-none');
        $('.loader-wrapper').addClass("d-none");
    });
    function create_user_list(){
        Array.from(data).forEach(user => {
            let status = null;
            if (user.is_yourself){
                status = '<span class="yourself">Это Вы</span>';
            }
            else if(user.is_friend){
                status = '<span class="status">Друг</span> <i class="fa fa-user add-friend" aria-hidden="true"></i>';
            }
            else{
                status = '<span class="status">Не друг</span> <i class="fa fa-user-plus add-friend" aria-hidden="true"></i>';
            }
            $('.user-list').append(`
                <div class="user" name="${user.id}">
                    <img class="profile" src="${user.photo_image}">
                    <span class="full-name">${user.first_name} ${user.last_name}</span>
                    ${status}
                </div>
            `);
        });
        $('.user-list p').addClass('d-none');
    }
    function send_message(){
        this.send(this.message);
    }
    function get_users(event){
        data = JSON.parse(event.data);
    }
    function add_friend(){
        Array.from($('.fa-user-plus')).forEach(button => {
            $(button).click(function(event){
                $(button).removeClass('fa-user-plus');
                $(button).addClass('fa-user');
                $(button).parent().find('.status').text('Друг');
                console.log('Жёстко нажали');
                console.log($(button).parent().attr('name'));
                $.ajax({
                     type: "POST",
                    url: $(location).attr("href"),
                    dataType: 'json',
                    data: {
                        pk: $(button).parent().attr('name'),
                        csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
                    }
                })
            });
        });
    }

});