function xhr(METHOD, ENDPOINT) {
    let req = new XMLHttpRequest();
    req.responseType = "json";
    req.onreadystatechange = function() {
        if(req.readyState === 4 && req.status === 200) {
            window.location.replace(req.response.redirect);
        };
    };
    req.open(METHOD, ENDPOINT, true);
    req.send();
}

var xhrButtons = document.querySelectorAll(".xhr");
for (var index = 0; index < xhrButtons.length; index++) {
    let button = xhrButtons[index];
    let endpoint = button.getAttribute("data-action");
    let method = button.getAttribute("data-method");
    button.addEventListener("click", function() {xhr(method, endpoint)});
};
