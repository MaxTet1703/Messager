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

    const methods = {
        "login": listen_for_login,
        "sign_up": listen_for_sign_up
    };

    function listen_for_login(response){
        if (response.status == 200){
            console.log("ok")
        }
        else{
            $("#login .m-error").removeClass("opacity-0");
            $("#login .input-wrapper i.error").removeClass("d-none");
        }

    }
    function listen_for_sign_up(response){
        if (response.status == 200){
            $("#sign-up .m-ok").removeClass("opacity-0");
            $("#sign-up i.ok").removeClass("d-none");
        } else{
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
    }
    forms.forEach((form, index) => {

        $(form).submit(function(e){

            const data = $(this).serialize() + `&message=${messages[index]}`;
            $(this).find("span").text("").addClass("d-none");
            $(this).find("i").addClass("d-none");
            console.log($(".forms span.error-message"));

            e.preventDefault();

            $.ajax({
                type: this.method,
                url: this.action,
                data: data,
                dataType: "json",
                success: function(response){
                    if (response.type_form == messages[0]){
                        listen_for_login(response);
                    } else{
                        listen_for_sign_up(response);
                    }
                },
                error: function(xhr, status, error){
                    console.log("Ошибка, сестра")
                    console.log(error);
                }
            });
        });
    });
});