function user_submit_edit_form() {
    var form_ready = true;

    var form = new FormData();
    var file = document.getElementById('user-image-upload-edit').files[0];
    form.append('image', file);

    form.append('lineid', document.getElementById('user-edit-lineid').value);
    form.append('email', document.getElementById('user-edit-email').value);
    form.append('username', document.getElementById('user-edit-username').value);


    // Level regex check : not empty
    if (/^$/.test(document.getElementById('user-edit-level').value)) {
        document.getElementById('user-edit-level').setAttribute('class', 'form-control is-invalid');
        document.getElementById('user-edit-level').focus();
        form_ready = false;
    } else {
        document.getElementById('user-edit-level').setAttribute('class', 'form-control');
        form.append('level', document.getElementById('user-edit-level').value);
    }

    //submit form
    if (form_ready) {
        $.ajax({
            type: "PUT",
            data: form,
            url: "/admin/account",
            cache: false,
            contentType: false,
            processData: false,
            success: function(result) {
                toastr.options = {
                    positionClass: "toast-bottom-center"
                };
                toastr.success(result['message']);
                setTimeout(() => {
                    window.location.href = window.location.href;
                }, 1500);
            },
            error: err => {
                toastr.options = {
                    positionClass: "toast-bottom-center"
                };
                toastr.error(JSON.parse(err['responseText']).message);
            }
        });
    }

    // Stop Display loader
    document.getElementById('loader').style.display = "none";
}


function user_select_profile_image_edit() {
    document.getElementById('user-image-upload-edit').click();
}


var user_loadFile_edit = function(event) {
	var image = document.getElementById('user-image-edit');
	if (event.target.files[0] != undefined) {
        image.src = URL.createObjectURL(event.target.files[0]);
    }
};

function user_clear_image_edit() {
    var image = document.getElementById('user-image-edit');
    var input_image = document.getElementById('user-image-upload-edit');
    input_image.value = null
    image.src = "/static/src/img/nobody.jpg";
}


function displayUserInfo() {
    user_name = document.getElementById("username").innerHTML;
    fetch("/admin/userinfo?username=" + user_name)
    .then(res => {
        return res.json();
    })
    .then(data => {
        if (!(data.image ==null)) {
        document.getElementById("user-image-edit").src = window.location.origin + '/' + data.image;
        } else {
            document.getElementById("user-image-edit").src = "/static/src/img/nobody.jpg";
        }
        document.getElementById("user-edit-id_no").value = data.id;
        document.getElementById("user-edit-first_name").value = data.firstname;
        document.getElementById("user-edit-last_name").value = data.lastname;
        document.getElementById("user-edit-username").value = data.username;
        document.getElementById("user-edit-level").value = data.level;
        document.getElementById("user-edit-email").value = data.email;
        document.getElementById("user-edit-lineid").value = data.lineid;
        document.getElementById("user-edit-created_date").value = data.created_datetime;
    });
}
