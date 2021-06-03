"use strict";

// 2021-06-03
const CACHE_VER = "b68615c2e9d0a0465a394cedbbfa81ede9234cb6";
const FILES_TO_CACHE = [
    "/app",
    "/app/no-network",
    "/static/css/main.css",
    "/static/css/modal.css",
    "/static/fonts/noto-sans-kr-v12-latin_korean-regular.woff",
    "/static/fonts/noto-sans-kr-v12-latin_korean-regular.woff2",
    "/favicon.ico",
    "/static/img/icon192.png", "/static/img/icon512.png",
    "/static/js/clipboard.min.js",
    "/static/js/micromodal.min.js",
    "/static/js/star.js",
    "/static/js/star-btn.js",
];

self.addEventListener("install", function(e) {
    console.log("설치중...");
    e.waitUntil(
        caches.open(CACHE_VER).then(function(cache) {
            return cache.addAll(FILES_TO_CACHE);
        })
    );
});

self.addEventListener("activate", function(e) {
    e.waitUntil(
        caches.keys().then(function(keyList) {
            return Promise.all(keyList.map(function(key) {
                if(key !== CACHE_VER) {
                    console.log("구버전 리소스 제거 : "+key);
                    return caches.delete(key);
                }
            }));
        })
    );
});

self.addEventListener("fetch", function(e) {
    e.respondWith(
        caches.match(e.request).then(function(r) {
            console.log("리소스 가져옴 : "+e.request.url);
            return r || fetch(e.request).then(function(response) {
                return response;
            });
        }).catch(function() {
            return caches.match("/app/no-network");
        })
    );
});