$(function($){
    var data;
    const path_to_page = 'ws://127.0.0.1:8000/ws/main';
    $("#search input.line").keyup(function(event){
        $('.user-list .user, .user-list p').remove();
        $('.user-list').addClass('d-none');
        $('.loader-wrapper .loader').removeClass("d-none")
        var message = $("#search input.line").val();;
        var wb = new WebSocket(path_to_page);
        wb.message = message;
        wb.onopen = send_message;
        wb.onmessage = function(event){
            data = JSON.parse(event.data);
        };
        if (data != null){
            user_list();
        }else{
            $('.user-list').append('<p>Пользователя не нашлось</p>');
        }

        $('.loader-wrapper .loader').addClass("d-none")
        $('.user-list').removeClass('d-none');
    });
    function user_list(){
        Array.from(data).forEach(user => {
//            if (user.photo_image == null){
//                user.photo_image = "/static/images/default.jpg";
//            }
            $('.user-list').append(`
                <div class="user">
                    <img class="profile" src="${user.photo_image}">
                    <span class="full-name">${user.first_name} ${user.last_name}</span>
                </div>
            `);
        });
    }
    function send_message(){
        this.send(this.message);
    }


});