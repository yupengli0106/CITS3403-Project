$(document).ready(function(){
	$('#game_shows').modal('show');
	var question_id = 0;
	var arr = [1,4,5,6];
	var theme_turn = false;
	var day = new Date();
	var start_time=day.getTime();
	var played = 0;
	var wined_count = 0;
	var streak = 0;
	var time = 0;

	function shareGrades(){
		let dom = document.createElement('input');
		dom.value = 'played:'+played+' wined_count:'+wined_count+' streak:'+streak+' time:'+time+' '+window.location.href;
		document.body.appendChild(dom);
		dom.select();
		document.execCommand("Copy"); 
		document.body.removeChild(dom);
		alert('cpoy success');
	}
	$("#success_share").click(function(){
		shareGrades();
	});

	$("#failed_share").click(function(){
		shareGrades();
	});

	function sendStatic(wined_count,streak){
		var end_time = day.getTime();
		$.ajax({
			url: '/static',
			type: 'post',
			dataType: 'json',
			data:{"question_id": question_id,  "question_time": (end_time - start_time)/60, "played": played +1,  "wined_count" : wined_count, "streak" : streak},
			success: function(problem, textStatus, xhr) {
			},
			error: function(xhr, textStatus, errorThrown) {
			}
		});	
	} 
	$.ajax({
		url: '/questions',
		type: 'GET',
		dataType: 'json',
		success: function(data, textStatus, xhr) {
			$("#question").text(data.question);
			question_id = data.question_id;
			arr = data.answer.split("");
			played = data.played;
			wined_count = data.wined_count;
			streak = data.streak;
			time = data.time;
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
					if(row == try_times-1 && right_answer < char_num ){
						sendStatic(0,0);
					}
					if(right_answer >= char_num){
						answer = true;
						for(var j = input_count; j< try_times*char_num; j++){
							$("#box_"+j).css({"background-color":"grey"});
						}
						$("#game_success").modal("show");
						sendStatic(1,row);
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
		$("#static_played").text(played);
		$("#static_win").text((wined_count/played * 100) + "%");
		$("#static_streak").text(streak);
		$("#static_time").text(time);
		$('#statistics').modal('show');
	});
});