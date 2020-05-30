var button = document.getElementById("collect");
button.addEventListener("click", function() {
	// event.preventDefault();
	var httpRequest;

	httpRequest = new XMLHttpRequest();
	var pid = getQueryString("pid");
	//从cookies中获取csrftoken
	var csrftoken = getCookie('csrftoken');

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
	httpRequest.send(JSON.stringify({data:pid, action:"add"}));

	function makeResponse() {
		if (httpRequest.readyState == 4 && httpRequest.status == 200){
			alert(httpRequest.responseText);
		}
	}

	//匹配url中的关键词
	function getQueryString(name) {
	    let reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
	    let r = window.location.search.substr(1).match(reg);
	    if (r != null) {
	        return r[2];
	    };
	    return null;
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
});