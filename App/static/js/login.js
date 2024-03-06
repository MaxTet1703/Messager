$(function($){

    const messages = ["login", "sign-up"];

    const buttons = Array.from($("#NavBar button"));
    const forms = Array.from($(".forms form"));
    $(forms[0]).addClass("active");
    $(buttons[0]).addClass("active");
    buttons.forEach((button, index) => {
        $(button).click(function(e){
            $(buttons).removeClass("active");
            $(button).addClass("active");
            $(forms).removeClass("active");
            $(forms[index]).addClass("active");
        });
    });


    function success_for_login(response){
        window.location = 'main/';
    }
     function success_for_sign_up(response){
        $("#sign-up .m-ok").removeClass("opacity-0");
        $("#sign-up i.ok").removeClass("d-none");
    }


    function fail_for_login(response){
         $("#login .m-error").removeClass("opacity-0");
         $("#login .input-wrapper i.error").removeClass("d-none");

    }
    function fail_for_sign_up(response){
        Array.from($("#sign-up div")).forEach(block =>{
            const key = $(block).find("input").attr("name");
            if(key in response.errors){
                $(block).find("span").text(response.errors[key][0].message);
                $(block).find("i.error").removeClass("d-none");
            }else{
                $(block).find("i.ok").removeClass("d-none");
            }
        });
        $("#sign-up div").find("span").removeClass("d-none");
    }


    forms.forEach((form, index) => {

        $(form).submit(function(e){
            const id_form = $(form).attr('id');
            const csrfmiddlewaretoken = $(`${id_form} input[name="csrfmiddlewaretoken"]`);

            const data = $(this).serialize() + `&message=${messages[index]}`;
            $(this).find("span").text("").addClass("d-none");
            $(this).find("i").addClass("d-none");


            e.preventDefault();

            $.ajax({
                type: this.method,
                url: this.action,
                data: data,
                dataType: "json",
                success: function(response){
                    if (response.type_form == messages[0]){
                        success_for_login(response);
                    } else{
                        success_for_sign_up(response);
                    }
                },
                error: function(xhr, status, error){
                     console.log(xhr.responseJSON);
                     if (xhr.responseJSON.type_form == messages[0]){
                        fail_for_login(xhr.responseJSON);
                    } else{
                        fail_for_sign_up(xhr.responseJSON);
                    }
                }
            });
        });
    });
});