"use strict";

function get_star(){
    let star = JSON.parse(localStorage.getItem("star"));
    if(star == null){star = {};localStorage.setItem("star", JSON.stringify(star));}
    console.log(`즐겨찾기 불러옴 : ${Object.keys(star)}`);return star;
}
function add_star(school, url){
    let star = get_star();star[school] = url;localStorage.setItem("star", JSON.stringify(star));
    console.log(`즐겨찾기 추가 함 : ${school}`);
}
function del_star(school){
    let star = get_star();delete star[school];localStorage.setItem("star", JSON.stringify(star));
    console.log(`즐겨찾기 삭제 함 : ${school}`);
}
function render_star(){
    const star = get_star();
    const keys = Object.keys(star);
    let render_target = document.getElementById("render_target");render_target.innerHTML="";
    keys.forEach(function(key){
        let li=document.createElement("li");let a=document.createElement("a");
        if(star[key].startsWith("/")){
            a.setAttribute("class","high l");a.setAttribute("href",star[key]);
            a.appendChild(document.createTextNode(key));li.appendChild(a);render_target.appendChild(li);
            console.log(`목록에 추가함 : ${key}`);
        }
    });
}