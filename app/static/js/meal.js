"use strict";

// 알러지 설명 추가
const button = document.querySelectorAll("span.allergy");
for(var i=0;i<button.length;i++){
    button[i].addEventListener("click",function(btn){
        window.alert(btn.srcElement.innerText+"와 관련된 알레르기를 가지고 있다면, 해당 식품을 배식받지 말아 주세요.");
    });
}

// 조식 중식 석식 이동 단축키 등록 파트
window.addEventListener("keydown", function(key){
    if(Number(key.key) > 0){
        try {
            window.scrollTo({
                top: window.pageYOffset + document.querySelector("#meal_"+key.key).getBoundingClientRect().top,
                behavior: 'smooth'
            });
        } catch(e) { console.log("-- Passed!\n" + e); }
    }
});

// 공유하기
function share(name){
    document.querySelector("#band").addEventListener("click",function(){
        window.open("https://band.us/plugin/share?body='"+name+"'의 급식 정보 "+document.URL+"&route="+document.domain)
    });
    document.querySelector("#twit").addEventListener("click",function(){
        window.open("https://twitter.com/intent/tweet?text='"+name+"'의 급식 정보&url="+document.URL);
    });
    document.querySelector("#fb").addEventListener("click",function(){
        window.open("http://www.facebook.com/sharer/sharer.php?u="+document.URL);
    });
}