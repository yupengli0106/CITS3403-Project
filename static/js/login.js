$(document).ready(function(){
	$("#submit").click(function(){
		event.preventDefault();
		var username = $("#username").val().trim();
		var password = $("#password").val().trim();
		var remember = false;
		if(username.length == 0 ){
			alert("Please input username");
			return;
		}
		if(password.length == 0 ){
			alert("Please input password");
			return;
		}
		if($("#remember_me").is(':checked')){
			remember = true;
		}
		$.ajax({
			url: '/login',
			type: 'POST',
			dataType: 'json',
			data: {'username': username, 'password': password, 'remember': remember},
			success: function(data, textStatus, xhr) {
				if(data.status == 'success'){
					window.location.href = '/game.html';
				}else{
					alert("The user name does not match the password");
				}
			},
			error: function(xhr, textStatus, errorThrown) {
			//called when there is an error
			}
				
		});
	});
});
