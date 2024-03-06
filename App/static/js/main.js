$(function($){
    $('.user-menu').click(function(e){
        $('.user-menu').toggleClass('active');
    });

    Array.from($('.user-menu ul li.item')).forEach(item => {
        if ($(item).find('a').attr("href") == window.location.pathname){
            $(item).addClass('active');
        }
    });
});