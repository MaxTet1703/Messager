$(function($){
    
    $(".messages").scrollTop($(".messages").height());

    const chatSocket = new WebSocket("ws://" + window.location.host + "/ws" + window.location.pathname);
    
    chatSocket.onmessage = function(event){
        var class_for_message = "";
        var animation_class = "";
        message_info = JSON.parse(event.data)
        fetch("http://" + window.location.host + "/get_user/")
        .then(response => response.json())
        .then(data => {

            if (data.id == message_info.user_id){
                class_for_message = "my-mes";
                animation_class = "right";
            }else{
                class_for_message = "com-mes";
                animation_class = "left";
            }
            $(".messages").append(`
                <div class="mes-wrapp ${animation_class}">
                    <p class="${class_for_message}">${message_info.message}</p>
                </div>
            `);
            $(".messages").scrollTop($(".messages").height());
        })
        .catch(error => console.error('Error:', error));
    }
    $("#mes-sending").submit(function(event){
        event.preventDefault();
        const message = $(this).find("input").val();
        chatSocket.send(message);
        $(this).find("input").val("");
    });
});
