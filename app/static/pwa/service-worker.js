"use strict";

const CACHE_VER = "2021-02-21_v24";

const FILES_TO_CACHE = [
    "/app",
    "/app/no-network.page",
    "/favicon.ico",
    "/static/js/star.js",
    "/static/css/main.css",
    "/static/fonts/noto-sans-kr-v12-latin_korean-regular.woff",
    "/static/fonts/noto-sans-kr-v12-latin_korean-regular.woff2"
];

self.addEventListener("install", function(e) {
    console.log("[Service Worker] 설치중...");
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
                    console.log("[Service Worker] 구버전 리소스를 제거함 : "+key);
                    return caches.delete(key);
                }
            }));
        })
    );
});

self.addEventListener("fetch", function(e) {
    e.respondWith(
        caches.match(e.request).then(function(r) {
            console.log("[Service Worker] 리소스를 가져옴: "+e.request.url);
            return r || fetch(e.request).then(function(response) {
                return caches.open(CACHE_VER).then(function(cache) {
                    if (e.request.url.endsWith(".css") || e.request.url.endsWith(".js") || e.request.url.endsWith(".png") ){
                        cache.put(e.request, response.clone());
                        console.log("[Service Worker] 새로운 리소스 캐싱됨 : "+e.request.url);
                        return response;
                    } else {
                        console.log("[Service Worker] 캐싱 취소됨 : "+e.request.url);
                        return response;
                    }
                });
            });
        }).catch(function() {
            if (e.request.url.endsWith(".css") || e.request.url.endsWith(".js")) {
                return "";
            }
            return caches.match("/app/no-network.page");
        })
    );
});