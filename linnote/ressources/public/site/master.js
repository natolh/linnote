function xhr(METHOD, URL) {

    var req = new XMLHttpRequest();

    req.onreadystatechange = function() {
        if (this.status == 200) {
            window.location.reload();
        }
    };

    req.open(METHOD, URL, true);
    req.send();
}
