$(function($){

    const path_to_page = 'ws://' + window.location.host + '/ws/main';
    var search_ws = new WebSocket(path_to_page);
    search_ws.onmessage = create_user_list;

    $("#search input.line").keydown(function(event){
        $('.user-list').addClass('d-none');
        $('.loader-wrapper').removeClass("d-none");
        $('.user-list .user').remove();

        const message = $("#search input.line").val();
        search_ws.send(message);

        $('.user-list').removeClass('d-none');
        $('.loader-wrapper').addClass("d-none");
    });
    function create_user_list(event){
        var data = JSON.parse(event.data);
         if (!data.length){
            $('.loader-wrapper').addClass("d-none");
            $('.user-list p').removeClass('d-none');
            return;
        }
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
        add_friend();
        $('.user-list p').addClass('d-none');
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