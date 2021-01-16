"use strict";

// <학교 입력> placeholder 바꾸는 용
function school_update(){
    const holder = [
        "ㅁㅁ초",
        "ㅁㅁ초등학교",
        "ㅁㅁ중",
        "ㅁㅁ중학교",
        "ㅁㅁ고",
        "ㅁㅁ고등학교"
    ];

    try{
        document.querySelector("#school_name").placeholder = holder[Math.floor(Math.random()*holder.length)];
        setTimeout(school_update, 850);
    } catch(e) { console.log("-- Passed!\n" + e); }
} school_update();


// 즐겨찾기 버튼 관련 기능 정의 함수
function star(star_page){
    try{
        document.querySelector("#star").addEventListener("click",function(){
            location.replace(star_page);
        });
        document.querySelector("#school_name").addEventListener("focus",function(){
            document.querySelector("#starBox").setAttribute("style", "visibility: hidden;");
        });
        document.querySelector("#school_name").addEventListener("blur",function(){
            document.querySelector("#starBox").setAttribute("style", "visibility: visible;");
        });
    } catch(e) { console.log("-- Passed!\n" + e); }
}