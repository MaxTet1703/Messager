$(function($){
    $('.user-menu').click(function(e){
        $('.user-menu').toggleClass('active');
    });

    Array.from($('.user-menu ul li.item')).forEach(item => {
        if ($(item).find('a').attr("href") == window.location.pathname){
            $(item).addClass('active');
        }
    });
    $("div.chat-container i").click((event) => {
        $(event.target.parentElement).addClass("d-none");
        $(".msg-button").removeClass("d-none");
    });
    $(".msg-button").click((event) => {
        $(event.target).addClass("d-none");
        $("div.chat-container").removeClass("d-none");
    })
});