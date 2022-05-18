$(document).ready(function(){
	$.ajax({
		url: '/admin_question_list',
		type: 'GET',
		dataType: 'json',
		data: {},
		success: function(data, textStatus, xhr) {
			if(data.status == 'success'){
				var question_list ="";
				for(var i =0; i<data.list.length; i++){
					question_list += '<li class="li_question">' +
						'<div>' +data.list[i].question+'</div>' +
						'<span class="li_left">'+ data.list[i].answer+'</span>' +
						'<span class="li_right">'+
						'<button class="btn btn-default" onclick="getQuestion('+data.list[i].question_id+')">Edit</button>'+
						'<button class="btn btn-default" onclick="deleteQuestion('+data.list[i].question_id+')">Delete</button>'+
						'</span>'+
					'</li>';
				}
				$("#ul_question").html(question_list);
			}
		},
		error: function(xhr, textStatus, errorThrown) {
		//called when there is an error
		}	
	});
	function getQuestion(id){
		$.ajax({
			url: '/admin_get_question/id',
			type: 'GET',
			dataType: 'json',
			data: {'id': id},
			success: function(data, textStatus, xhr) {
				if(data.status == 'success'){
					$("#question_id").val(id);
					$("#edit_question").val(data.content);
					$("#edit_answer").val(data.answer);
					$("#modal_edit_question").modal("show");
				}
			},
			error: function(xhr, textStatus, errorThrown) {
			//called when there is an error
			}	
		});
	}
	function deleteQuestion(id){
		if(confirm("do you want to delete?") == false){
			return;
		}
		$.ajax({
			url: '/question_delete',
			type: 'GET',
			dataType: 'json',
			data: {'id': id},
			success: function(data, textStatus, xhr) {
				if(data.status == 'success'){
					window.location.href = window.location.href;
					alert("delete success");
				}
			},
			error: function(xhr, textStatus, errorThrown) {
			//called when there is an error
			}	
		});
	}
	$("#submit_add_question").click(function(){
		event.preventDefault();
		var question = $("#add_question").val().trim();
		var answer = $("#add_answer").val().trim();
		if(question.length == 0 ){
			alert("Please input question");
			return;
		}
		if(answer.length == 0 ){
			alert("Please input answer");
			return;
		}
		$.ajax({
			url: '/question_add',
			type: 'POST',
			dataType: 'json',
			data: {'question': question, 'answer': answer},
			success: function(data, textStatus, xhr) {
				if(data.status == 'success'){
					window.location.href = window.location.href;
					alert("add success");
				}else{
					alert("try again");
				}
			},
			error: function(xhr, textStatus, errorThrown) {
			//called when there is an error
			}	
		});
	});
	$("#submit_edit_question").click(function(){
		event.preventDefault();
		var id = $("#question_id").val();
		var question = $("#edit_question").val().trim();
		var answer = $("#edit_answer").val().trim();
		if(question.length == 0 ){
			alert("Please input question");
			return;
		}
		if(answer.length == 0 ){
			alert("Please input answer");
			return;
		}
		$.ajax({
			url: '/question_edit',
			type: 'POST',
			dataType: 'json',
			data: {'id':id,'question': question, 'answer': answer},
			success: function(data, textStatus, xhr) {
				if(data.status == 'success'){
					window.location.href = window.location.href;
					alert("edit success");
				}else{
					alert("try again");
				}
			},
			error: function(xhr, textStatus, errorThrown) {
			//called when there is an error
			}	
		});
	});
	$("#submit_search").click(function(){
		event.preventDefault();
		var content = $("#search_content").val().trim();
		if(content.length == 0 ){
			return;
		}
		$.ajax({
			url: '/admin_search_keyword',
			type: 'GET',
			dataType: 'json',
			data: {'content': content},
			success: function(data, textStatus, xhr) {
				if(data.status == 'success'){
					var question_list ="";
					for(var i =0; i<data.list.length; i++){
						question_list += '<li class="li_question">' +
							'<div>' +data.list[i].question+'</div>' +
							'<span class="li_left">'+ data.list[i].answer+'</span>' +
							'<span class="li_right">'+
							'<button class="btn btn-default" onclick="getQuestion('+data.list[i].question_id+')">Edit</button>'+
							'<button class="btn btn-default" onclick="deleteQuestion('+data.list[i].question_id+')">Delete</button>'+
							'</span>'+
						'</li>';
					}
					$("#ul_question").html(question_list);
				}
			},
			error: function(xhr, textStatus, errorThrown) {
			//called when there is an error
			}	
		});
	});
});