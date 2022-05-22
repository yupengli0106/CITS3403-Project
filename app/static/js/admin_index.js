$(document).ready(function(){
	$.ajax({
		url: '/admin_question_list',
		type: 'GET',
		dataType: 'json',
		data: {},
		success: function(data, textStatus, xhr) {	
			questionListHtml(data.question_list);
		},
		error: function(xhr, textStatus, errorThrown) {
		//called when there is an error
		}	
	});

	$(document).on("click",".click-edit",function(){
		getQuestion($(this).attr('value'));
	});

	$(document).on("click",".click-delete",function(){
		deleteQuestion($(this).attr('value'));
	});

	function getQuestion(id){
		id = parseInt(id);
		$.ajax({
			url: '/admin_get_question/'+id,
			type: 'GET',
			dataType: 'json',
			data: {'id': id},
			success: function(data, textStatus, xhr) {
				$("#question_id").val(id);
				$("#edit_question").val(data.content);
				$("#edit_answer").val(data.answer);
				$("#modal_edit_question").modal("show");
			},
			error: function(xhr, textStatus, errorThrown){
			//called when there is an error
			}	
		});
	}

	function deleteQuestion(id){
		if(confirm("do you want to delete?") == false){
			return;
		}
		$.ajax({
			url: '/admin_delete_question/'+id,
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
			url: '/admin_add_question',
			type: 'POST',
			dataType: 'json',
			data: {'content': question, 'answer': answer},
			success: function(data, textStatus, xhr) {
				if(data.status == 'success'){
					alert("add success");
					window.location.href = window.location.href;
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
			url: '/admin_edit_question/'+parseInt(id),
			type: 'POST',
			dataType: 'json',
			data: {'content': question, 'answer': answer},
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
		$.ajax({
			url: '/admin_search_keyword',
			type: 'POST',
			dataType: 'json',
			data: {'keyword': content},
			success: function(data, textStatus, xhr) {
				questionListHtml(data.question_list);
			},
			error: function(xhr, textStatus, errorThrown) {
			//called when there is an error
			}	
		});
	});
	function questionListHtml(question_list){
		var question_list_html = "";
		for(var i =0; i<question_list.length; i++){
			question_list_html += '<li class="li_question">' +
				'<div>' +question_list[i].content+'</div>' +
				'<span class="li_left">'+ question_list[i].answer+'</span>' +
				'<span class="li_right">'+
				'<button class="click-edit btn btn-default" value='+question_list[i].id+'>Edit</button>'+
				'<button class="click-delete btn btn-default" value='+question_list[i].id+'>Delete</button>'+
				'</span>'+
			'</li>';
		}
		$("#ul_question").html(question_list_html);	
	}
});