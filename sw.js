const CACHE_NAME = 'agrisense-v1';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './assets/hero_poultry.jpg',
  './assets/danjuma_poultry.jpg',
  './assets/solar_farm.jpg',
  './assets/nigerian_farmer.jpg',
  './assets/hardware_lab.jpg',
  './assets/abduljabbar.jpg',
  './assets/jungudo.jpg'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[ServiceWorker] Caching static assets');
      return cache.addAll(ASSETS);
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('[ServiceWorker] Removing old cache', key);
            return caches.delete(key);
          }
        })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      return cachedResponse || fetch(event.request);
    })
  );
});
