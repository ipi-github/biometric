function submit_chat_history(){
	$.ajax({
            url: "/submit/chat/",
            data: {'message': document.getElementById('new_chat').value},
            type: "post",
            beforeSend : function() {
                $(".custom_preloader").css("display", "block");
            },
            complete : function() {
                $(".custom_preloader").css("display", "none");
            },
            success: function(response) {
            	var result = JSON.parse(response);
            	var prev_html = document.getElementById('show_chat_history').innerHTML;
            	document.getElementById('show_chat_history').innerHTML = "<tr><td>"+result['message']+"</td></tr>"+prev_html;
            	document.getElementById('new_chat').value = "";
            },
            error: function(response) {
                alert('Error : '+response)
            }
        });
}