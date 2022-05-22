$(document).ready(function(){
    // update username and password
    $("#submit").click(function(){
        event.preventDefault();
        var username = $("#username").val().trim();
        var password = $("#password").val().trim();
        var password2 = $("#password2").val().trim();
        if(username.length > 20){
            alert("The length of the user name cannot over 20 characters");
            return;
        }
        if(username.length == 0){
            alert("Please input username");
            return;
        }
        if(password.length == 0){
            alert("Please input password");
            return;
        }
        if(password != password2){
            alert("The two passwords are inconsistent");
            return;
        }
        
        $.ajax({
            url: '/update',
            type: 'POST',
            dataType: 'json',
            data: {'username': username, 'password': password},
            success: function(data, textStatus, xhr) {
                if(data.status == "success"){
                    alert("Proflie update successful, please login again!");
                    window.location.href = "/login";
                }else{
                    alert('username already exists');
                }
            },
            error: function(xhr, textStatus, errorThrown) {
            //called when there is an error
            }
        });
    });
    // delete user account
    $("#delete").click(function(){
        event.preventDefault();
        $("#profile").modal('show');
    });
    $("#yes").click(function(){
        $.ajax({
            url: '/delete',
            type: 'POST',
            dataType: 'json',
            success: function(data, textStatus, xhr) {
                if(data.status == "success"){
                    alert("Your account has been deleted, thank you for using our service!");
                    window.location.href = "/login";
                }else{
                    alert('delete failed');
                }
            },
            error: function(xhr, textStatus, errorThrown) {
            //called when there is an error
            }
        });
    });
    $("#no").click(function(){
        $("#profile").modal('hide');
    }); // end of delete button
});