const C="eftmap-v1";
const ASSETS=["./","./index.html","./manifest.json","./icon-192.png","./icon-512.png",
"./map_Customs.jpg","./map_Woods.jpg","./map_Shoreline.jpg","./map_Factory.jpg",
"./map_StreetsOfTarkov.jpg","./map_GroundZero.jpg","./map_Interchange.jpg","./map_Lighthouse.jpg"];
self.addEventListener("install",e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(ASSETS)));self.skipWaiting()});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==C).map(k=>caches.delete(k)))));self.clients.claim()});
self.addEventListener("fetch",e=>{
 if(e.request.method!=="GET"||!e.request.url.startsWith(self.location.origin))return;
 e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request).then(res=>{
  const cp=res.clone();caches.open(C).then(c=>c.put(e.request,cp));return res}).catch(()=>caches.match("./index.html"))));
});