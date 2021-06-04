"use strict";

function storageAvailable(type) {
    var storage;
    try {
        storage = window[type];
        var x = '__storage_test__';
        storage.setItem(x, x);
        storage.removeItem(x);
        return true;
    }
    catch(e) {
        return e instanceof DOMException && (
            e.code === 22 || e.code === 1014 ||
            e.name === 'QuotaExceededError' ||
            e.name === 'NS_ERROR_DOM_QUOTA_REACHED') &&
            (storage && storage.length !== 0);
    }
}

function check_star(school){
    var star = get_star();
    if(typeof star[school] === "undefined"){return false}return true;
}
function render_btn(school){
    if(check_star(school)){
        document.querySelector("#star").textContent = "즐겨찾기에서 삭제하기";
    }
    else{
        document.querySelector("#star").textContent = "즐겨찾기에 추가하기";
    }
}
function star_btn(school, url){
    document.querySelector("#star").addEventListener("click",function(){
        if (!storageAvailable('localStorage')) {
            window.alert("이런! 즐겨찾기 기능을 사용할 수 없습니다!");return
        }
        if(check_star(school)){
            del_star(school);window.alert("삭제되었습니다!");
        }
        else{
            add_star(school, url);window.alert("추가되었습니다!");
        }
        render_btn(school);
    });
}