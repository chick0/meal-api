"use strict";

// 선택 메뉴에서 이동 버튼 등록 하는 함수
const button = document.querySelectorAll("button.select");

for(var i=0; i<button.length; i++){
    button[i].addEventListener("click",function(btn){
        location.replace(btn.srcElement.dataset.select);
    });
}

window.addEventListener("keydown", function(key){
    const map = {
        "1": 0,  "!": 0,
        "2": 1,  "@": 1,
        "3": 2,  "#": 2,
        "4": 3,  "$": 3,
        "5": 4,  "%": 4,
        "6": 5,  "^": 5,
        "7": 6,  "&": 6,
        "8": 7,  "*": 7,
        "9": 8,  "(": 8,
        "0": 9,  ")": 9,
        "-": 10, "_": 10,
        "=": 11, "+": 11,
    };

    try{
        if(confirm("'"+button[map[key.key]].textContent+"'로 이동할까요?")){
            location.replace(button[map[key.key]].dataset.select);
        }
    } catch(e) { console.log("-- Passed!\n" + e); }
});