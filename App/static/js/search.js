$(function($){
    const path_to_page = 'ws://0.0.0.0/ws/main';
    $("#search input.line").keyup(function(event){
        var message = $("#search input.line").val();;
        var wb = new WebSocket(path_to_page);
        wb.message = message;
        wb.onopen = send_message;
    });

    function send_message(){
        this.send(this.message)
    }

});