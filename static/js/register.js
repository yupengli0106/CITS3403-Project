$(document).ready(function(){
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
			url: '/register',
			type: 'POST',
			dataType: 'json',
			data: {'username': username, 'password': password},
			success: function(data, textStatus, xhr) {
				if(data.status == "success"){
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
});
