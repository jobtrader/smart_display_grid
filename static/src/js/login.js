$("#loginForm").submit(function(e) {
    e.preventDefault();
    login();
    return false;
});

function login() {
    request_data = $("#loginForm").serialize()
    $.ajax({
        type: "POST",
        data: request_data,
        url: "/admin/login",
        dataType: "JSON",
        withCredentials: true,
        success: function(data, textStatus, xhr) {
            console.log(data)
            window.location.href = '/admin/home';
        },
        error: function(err) {
            data = err.responseJSON;
            console.log(data);
            $(".login-window").addClass("animated shake");
            setTimeout(function() {$(".login-window").removeClass("shake");}, 1000);
            var invalid = document.getElementById("invalid-feedback");
            invalid.innerHTML = data.message;
            $("#login-error .alert-content").text(data.message);
            $("#login-error").css("display", "block");
        }
    });
}
