"use strict";

// GET 요청 보내기 용도
function request(url){
    var httpRequest = new XMLHttpRequest();
    httpRequest.open('GET', url, true);
    httpRequest.send();
}

// 이동 버튼 함수
function btn(target, where){
    document.querySelector(target).addEventListener('click',function(){
        location.replace(where);
    });
}

// 초기화 함수
function init(root){
    try{
        document.querySelector('#root').addEventListener('click',function(){
            location.replace(root);
        });
    } catch(e) { console.log("-- Passed!\n" + e); }

    if(window.location.pathname != "/"){
        window.addEventListener("keydown", function(key){
            if(key.key == "Backspace"){
                location.replace(root);
            }
        });
    }

    if("serviceWorker" in navigator) {
        window.addEventListener("load",function(){
            navigator.serviceWorker.register("/service-worker.js");
        });
    }
}