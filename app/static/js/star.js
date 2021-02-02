"use strict";

function get_star(){
    let star = JSON.parse(localStorage.getItem("star"));

    if(star == null){
        star = {};
        localStorage.setItem("star", JSON.stringify(star));
    }

    console.log("[chick_0] 즐겨찾기 불러옴 : "+Object.keys(star));
    return star;
}

function add_star(school, url){
    let star = get_star();

    star[school] = url;
    localStorage.setItem("star", JSON.stringify(star));

    console.log("[chick_0] 즐겨찾기 추가 함 : "+school);
}

function del_star(school){
    let star = get_star();

    delete star[school];
    localStorage.setItem("star", JSON.stringify(star));

    console.log("[chick_0] 즐겨찾기 삭제 함 : "+school);
}

function render_star(){
    const star = get_star();
    const keys = Object.keys(star);

    let html = "";
    for(var key in keys){
        html += `<li><a class="high l select" href="${star[keys[key]]}">${keys[key]}</a></li>`;
        console.log("[chick_0] 목록에 추가함 : "+keys[key]);
    }

    document.querySelector("#render_target").innerHTML = html;
}