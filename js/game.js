$(document).ready(function(){
	$('#game_shows').modal('show');
	var question_id = 0;
	var arr = [1,4,5,6];
	var theme_turn = false;
	var day = new Date();
	var start_time= Date.parse(new Date());
	var streak = 0;
	var time = 0;
	var username = "";
	var rank = 0;
	var score = 0;
   
	var clipboard = new ClipboardJS('.glyphicon-share-alt',{
		text: function(trigger){
			return 'username:'+username+' rank:'+rank+' score:'+score+' '+window.location.href;
		}
	});

	clipboard.on('success', function(e){
		console.info('Action:', e.action);
		console.info('Text:', e.text);
		console.info('Trigger:', e.trigger);
		e.clearSelection();
		alert("copy success");
	});
	clipboard.on('error', function(e){
		console.error('Action:', e.action);
		console.error('Trigger:', e.trigger);
	});

	function sendStatic(streak){
		$.ajax({
			url: '/statistic',
			type: 'post',
			dataType: 'json',
			data:{"question_id": question_id,"streak" : streak},
			success: function(problem, textStatus, xhr) {
			},
			error: function(xhr, textStatus, errorThrown) {
			}
		});	
	} 
	$.ajax({
		url: '/share',
		type: 'post',
		dataType: 'json',
		data:{},
		success: function(data, textStatus, xhr) {
			username = data.username;
			rank = data.rank;
			score = data.score;
		},
		error: function(xhr, textStatus, errorThrown) {
		}
	});	

	$.ajax({
		url: '/questions',
		type: 'GET',
		dataType: 'json',
		success: function(data, textStatus, xhr) {
			$("#question").text(data.question);
			question_id = data.question_id;
			arr = data.answer.split("");
		},
		error: function(xhr, textStatus, errorThrown) {
		}
	});
	var char_num = 4;
	var try_times = 6;
	var row_check = [];
	var answer = false;
	for(var i = 0; i < try_times; i++){
		row_check.push(0);
		var trs = $("<tr class='content_tr'></tr>");  
		for(var j = 0; j < char_num; j++){
			var tds = $("<td id='box_"+(i*char_num+j)+"'class='content_td'></td>").text("");
			trs.append(tds);
		}
		$("#content_table").append(trs);
	}
	var input_count = 0;
	$(".char").mouseover(function(){
		$(this).css({"cursor":"pointer"});
	});
	$(".char").click(function(){
		if(answer == true){
			return;
		}
		if(row_check[try_times-1] == 1){
			$("#game_failed").modal("show");
			return;
		}
		var key = $(this).text();
		if(key.length == 1){
			if(input_count == char_num * try_times){
			  	return;
			}
			if(input_count == 0){
		        $("#box_"+input_count).text(key);
		        input_count++;
		        return;
			}
			if(input_count % char_num == 0){
			    if(row_check[Math.floor((input_count -1)/char_num)] == 0){
			    	return;
			    }
		    }
			$("#box_"+input_count).text(key);
			input_count++;
		}else{
			if(key == "DELETE"){
				if(input_count == 0){
					return;
				}
				var row = Math.floor((input_count-1)/char_num);
				if(row_check[row] == 1){
					return;
				}else{
					if(input_count == row * char_num){
						return;
					}
					input_count--;
					$("#box_"+input_count).text("");
				}
			}else{
				if(input_count % char_num ==0){
					var row = Math.floor((input_count -1)/char_num);
					row_check[row] = 1;
					var right_answer = 0;
					for( var i = input_count - char_num, j=0; i<input_count; i++, j++){
						if($("#box_"+i).text() == arr[j]){
							$("#box_"+i).css({"background-color": "gold"});
							right_answer++;
						}else{
							if(arr.includes(parseInt($("#box_"+i).text()))){
								$("#box_"+i).css({"background-color": "green"});
							}else{
								$("#box_"+i).css({"background-color": "red"});
							}
						}
					}
					var end_time = Date.parse(new Date());
					time = Math.floor((end_time - start_time)/1000);
					var showTime = time + "s";
					if(right_answer >= char_num){
						answer = true;
						for(var j = input_count; j< try_times*char_num; j++){
							$("#box_"+j).css({"background-color":"grey"});
						}
						streak = row + 1;
						$("#success_static_time").html(showTime);
						$("#success_static_streak").html(streak);
						$("#game_success").modal("show");
						sendStatic(streak);
					}
					if(row_check[try_times-1] == 1){
						$("#game_failed").modal("show");
						return;
					}
				}
			}
		}

	});
	$("#theme_turn").click(function(){
		if(theme_turn == false ){
			theme_turn = true;
			$("#content_table").css({"background-color": "blue"});
			$("body").css({"background-color": "#121213"});
			$(".head_title").css({"color": "blue"});
			$(".question").css({"color": "blue"});
			$(".char").css({"color": "blue"});
			$(".glyphicon").css({"color": "blue"});
		}else{
			theme_turn = false;
			for(var j = input_count; j< try_times*char_num; j++){
				$("#box_"+j).css({"color":"white"});
			}
			$("body").css({"background-color": "white"});
			$(".head_title").css({"color": "black"});
			$(".question").css({"color": "black"});
			$(".char").css({"color": "black"});
			$(".glyphicon").css({"color": "black"});
			$("#content_table").css({"background-color": "white"});
		}
	});
	$("#static_turn").click(function(){
		$("#static_streak").text(streak);
		$("#static_time").text(time + "s");
		$('#statistics').modal('show');
	});
});