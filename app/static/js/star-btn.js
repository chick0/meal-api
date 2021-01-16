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
            // Firefox를 제외한 모든 브라우저
            e.code === 22 ||
            // Firefox
            e.code === 1014 ||
            // 코드가 존재하지 않을 수도 있기 떄문에 이름 필드도 확인합니다.
            // Firefox를 제외한 모든 브라우저
            e.name === 'QuotaExceededError' ||
            // Firefox
            e.name === 'NS_ERROR_DOM_QUOTA_REACHED') &&
            // 이미 저장된 것이있는 경우에만 QuotaExceededError를 확인하십시오.
            (storage && storage.length !== 0);
    }
}

function check_star(school){
    var star = get_star();

    if(typeof star[school] === "undefined"){
        return false
    }
    return true;
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
            window.alert("이런! 즐겨찾기 기능을 사용할 수 없습니다!");
            return
        }

        if(check_star(school)){
            del_star(school);
            window.alert("삭제되었습니다!");
        }
        else{
            add_star(school, url);
            window.alert("추가되었습니다!");
        }
        render_btn(school);
    });
}