"use strict";

function poem(idx){
    const url = "/api/get/" + idx;
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        console.log("[ajax]readyState: " + xhr.readyState);
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                console.log("[ajax]Request Success");
                const response = JSON.parse(xhr.responseText);
                document.querySelector("#poem").innerHTML = response.preview;
                document.querySelector("#poem").href = response.url;
            }
        }
    };

    xhr.open("GET", url, true);
    xhr.send(null);
}