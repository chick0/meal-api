"use strict";

function get_star(){
    let star = JSON.parse(localStorage.getItem("star"));

    if(star == null){
        star = {};
        localStorage.setItem("star", JSON.stringify(star));
    }

    console.log(`[chick_0] 즐겨찾기 불러옴 : ${Object.keys(star)}`);
    return star;
}

function add_star(school, url){
    let star = get_star();

    star[school] = url;
    localStorage.setItem("star", JSON.stringify(star));

    console.log(`[chick_0] 즐겨찾기 추가 함 : ${school}`);
}

function del_star(school){
    let star = get_star();

    delete star[school];
    localStorage.setItem("star", JSON.stringify(star));

    console.log(`[chick_0] 즐겨찾기 삭제 함 : ${school}`);
}

function render_star(){
    const star = get_star();
    const keys = Object.keys(star);

    var render_target = document.getElementById("render_target");
    render_target.innerHTML = "";

    for(var key in keys){
        var li = document.createElement("li");
        var a = document.createElement("a");

        if(star[keys[key]].startsWith("/")){
            a.setAttribute("class", "high l");
            a.setAttribute("href", star[keys[key]]);
            a.appendChild(document.createTextNode(keys[key]));

            li.appendChild(a);
            render_target.appendChild(li);

            console.log(`[chick_0] 목록에 추가함 : ${keys[key]}`);
        }
        else{
            console.log(`[chick_0] 이상한 즐겨찾기 정보를 목록에 추가하지 않음 : ${keys[key]}`)
        }
    }
}