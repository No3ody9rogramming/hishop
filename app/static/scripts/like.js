var url = "/like/";

function like(element, product_id) {
	
	var data = {
		csrf_token: $("#csrf_token").val(),
		like: true,
	};

	$.ajax({
		type:"POST",
		url: url + product_id,
		data: data,
		success: function(data) {
			if (data != "error")
				element.childNodes[0].className = data;
		}
	});
}