"use strict";

function get_star(){
    var star = JSON.parse(localStorage.getItem("star"));

    if(star == null){
        star = {};
        localStorage.setItem("star", JSON.stringify(star));
    }

    console.log("[chick_0] 즐겨찾기 불러옴 : "+Object.keys(star));
    return star;
}

function add_star(school, url){
    var star = get_star();

    star[school] = url;
    localStorage.setItem("star", JSON.stringify(star));

    console.log("[chick_0] 즐겨찾기 추가 함 : "+school);
}

function del_star(school){
    var star = get_star();

    delete star[school];
    localStorage.setItem("star", JSON.stringify(star));

    console.log("[chick_0] 즐겨찾기 삭제 함 : "+school);
}

function render_star(){
    var base = '<li><button class="high l select" data-select="#url#">#school#</button></li>';
    var star = get_star();
    var keys = Object.keys(star);
    var html = "";

    for(var key in keys){
        html += base.replace("#school#", keys[key]).replace("#url#", star[keys[key]]);
        console.log("[chick_0] 목록에 추가함 : "+keys[key]);
    }

    document.querySelector("#render_target").innerHTML = html;
}