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

// 급식 날짜 이동 버튼 등록 함수
function meal(edu, school, yesterday, tomorrow){
    const base = "/meal/"+[edu,school].join("/");
    document.querySelector('#yesterday').addEventListener('click',function(){
        location.replace(base + "/" + yesterday);
        console.log("[chick_0] 어제 급식으로 이동합니다");
    });
    document.querySelector('#tomorrow').addEventListener('click',function(){
        location.replace(base + "/" +  tomorrow);
        console.log("[chick_0] 내일 급식으로 이동합니다");
    });

    window.addEventListener("keydown", function(key){
        if(key.key == "[" || key.key == "a" || key.key == "ArrowLeft"){
            location.replace(base + "/" + yesterday);
            console.log("[chick_0] 어제 급식으로 이동합니다");
        }
        else if(key.key == "]" || key.key == "d" || key.key == "ArrowRight"){
            location.replace(base + "/" +  tomorrow);
            console.log("[chick_0] 내일 급식으로 이동합니다");
        }
    });

    try {
        document.querySelector("#today").addEventListener("click",function(){
            location.replace(base); console.log("[chick_0] 오늘 급식으로 이동합니다");
        });
    } catch(e) { console.log("-- Passed!\n" + e); }
}