const C = "eftmap-v5";
const ASSETS = ["./","./index.html","./manifest.json","./icon-192.png","./icon-512.png",
"./map_Customs.svg","./map_Woods.svg","./map_Shoreline.svg","./map_Factory.svg",
"./map_StreetsOfTarkov.svg","./map_GroundZero.svg","./map_Interchange.svg",
"./map_Interchange_Basement.svg","./map_Interchange_1F.svg","./map_Interchange_2F.svg","./map_Lighthouse.svg",
"./map_Reserve.svg"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(C).then(c => c.addAll(ASSETS)));
  self.skipWaiting();
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== C).map(k => caches.delete(k)))));
  self.clients.claim();
});
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET" || !e.request.url.startsWith(self.location.origin)) return;
  const isHTML = e.request.mode === "navigate" || e.request.url.endsWith("index.html") || e.request.url.endsWith("/");
  if (isHTML) {
    // network-first: always try fresh HTML, fall back to cache when offline
    e.respondWith(
      fetch(e.request).then(res => {
        const cp = res.clone();
        caches.open(C).then(c => c.put(e.request, cp));
        return res;
      }).catch(() => caches.match(e.request).then(r => r || caches.match("./index.html")))
    );
  } else {
    // images etc: cache-first (heavy, rarely change)
    e.respondWith(
      caches.match(e.request).then(r => r || fetch(e.request).then(res => {
        const cp = res.clone();
        caches.open(C).then(c => c.put(e.request, cp));
        return res;
      }))
    );
  }
});
