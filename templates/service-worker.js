self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open('tea-nav-cache').then((cache) => {
            return cache.addAll([
                '/',
                '/success.html',
                '/img/favicon.ico',
                '/css/styles.css',
                '/js/app.js'
            ]);
        })
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});
    