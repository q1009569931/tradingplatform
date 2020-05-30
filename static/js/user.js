/*-------收藏页--------*/
var buttons = document.getElementsByClassName("remove");
var table = document.getElementsByClassName("table")[0];
var td = document.getElementsByClassName("rows");
for(var i=0; i < buttons.length; i++) {
	buttons[i].addEventListener("click", makeRequest(td[i]));
}

function makeRequest(td) {
	return function() {
		let httpRequest;

		httpRequest = new XMLHttpRequest();
		let pid = this.getAttribute("id")
		//从cookies中获取csrftoken
		let csrftoken = getCookie('csrftoken');

		if (!httpRequest) {
			alert('Giving up :( Cannot create an XMLHTTP instance');
			return false;
		}

		httpRequest.onreadystatechange = makeResponse;
		//设置延时时间
		httpRequest.timeout = 5000;
		httpRequest.open('POST', "/user/collection/", true);
		httpRequest.setRequestHeader("Content-type", "application/json");
		//跨域设置
		httpRequest.setRequestHeader("X-CSRFToken", csrftoken);
		httpRequest.send(JSON.stringify({data:pid, action:"remove"}));

		function makeResponse() {
			if (httpRequest.readyState == 4 && httpRequest.status == 200){
				if (httpRequest.responseText == "OK") {
					var index = td.parentNode.rowIndex;
					table.deleteRow(index);
				}
				if (httpRequest.responseText == "NO") {
					alert("error!")
				}
			}
		}

		//从cookie获取信息
		function getCookie(name) {
		    var cookieValue = null;
		    if (document.cookie && document.cookie !== '') {
		        var cookies = document.cookie.split(';');
		        for (var i = 0; i < cookies.length; i++) {
		            var cookie = cookies[i].trim();
		            // Does this cookie string begin with the name we want?
		            if (cookie.substring(0, name.length + 1) === (name + '=')) {
		                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
		                break;
		            }
		        }
		    }
		    return cookieValue;
		}
	}
};

/*---------地址页-----------*/
var a_table = document.getElementsByClassName("address_list")[0];
var b = document.getElementsByClassName("t-delete");
var tr = a_table.getElementsByTagName("tr");
for(var i=0; i < b.length; i++) {
	b[i].addEventListener("click", c(tr[i+1]));
}

function c(tr) {
	return function() {
		let httpRequest;

		httpRequest = new XMLHttpRequest();
		let aid = this.getAttribute("title");
		//从cookies中获取csrftoken
		let csrftoken = getCookie('csrftoken');

		if (!httpRequest) {
			alert('Giving up :( Cannot create an XMLHTTP instance');
			return false;
		}

		httpRequest.onreadystatechange = makeResponse;
		//设置延时时间
		httpRequest.timeout = 5000;
		httpRequest.open('POST', "/user/address/", true);
		httpRequest.setRequestHeader("Content-type", "application/json");
		//跨域设置
		httpRequest.setRequestHeader("X-CSRFToken", csrftoken);
		httpRequest.send(JSON.stringify({data:aid}));

		function makeResponse() {
			if (httpRequest.readyState == 4 && httpRequest.status == 200){
				if (httpRequest.responseText == "OK") {
					var index = tr.rowIndex;
					a_table.deleteRow(index);
				}
				if (httpRequest.responseText == "NO") {
					alert("error!")
				}
			}
		}

		//从cookie获取信息
		function getCookie(name) {
		    var cookieValue = null;
		    if (document.cookie && document.cookie !== '') {
		        var cookies = document.cookie.split(';');
		        for (var i = 0; i < cookies.length; i++) {
		            var cookie = cookies[i].trim();
		            // Does this cookie string begin with the name we want?
		            if (cookie.substring(0, name.length + 1) === (name + '=')) {
		                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
		                break;
		            }
		        }
		    }
		    return cookieValue;
		}
	}
}