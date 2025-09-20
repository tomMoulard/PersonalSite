// Service Worker for tom.moulard.org
// Caches CV files, images, scripts, and stylesheets for offline access

const CACHE_NAME = 'tom-moulard-v1';
const CV_CACHE_NAME = 'tom-moulard-cv-v1';

// Files to cache immediately
const STATIC_ASSETS = [
  // CV Files (both locales)
  '/assets/tex/cv-en-tomMOULARD.pdf',
  '/assets/tex/cv-fr-tomMOULARD.pdf',

  // Core JavaScript files
  '/assets/js/jquery.js',
  '/assets/js/bootstrap.min.js',
  '/assets/js/scrollReveal.js',
  '/assets/js/custom.js',
  '/assets/js/chatbot.js',

  // Core CSS files
  '/assets/css/bootstrap.css',
  '/assets/css/font-awesome.min.css',
  '/assets/css/style.css',

  // Important images
  '/assets/img/team/moular_b_small.jpeg',
  '/assets/img/product/jaquette.png',
  '/assets/img/product/cat.jpg',
  '/assets/img/OCR.png',
  '/assets/img/team/china.jpg',

  // Main pages
  '/',
  '/fr/'
];

// Install event - cache static assets
self.addEventListener('install', event => {
  console.log('Service Worker: Installing...');

  event.waitUntil(
    Promise.all([
      // Cache static assets with error handling
      caches.open(CACHE_NAME).then(cache => {
        console.log('Service Worker: Caching static assets');
        return cache.addAll(STATIC_ASSETS).catch(error => {
          console.log('Service Worker: Some assets failed to cache:', error);
          // Cache individual files that succeed
          return Promise.allSettled(
            STATIC_ASSETS.map(url =>
              cache.add(url).catch(err =>
                console.log('Service Worker: Failed to cache:', url, err)
              )
            )
          );
        });
      }),

      // Pre-cache CV files specifically
      caches.open(CV_CACHE_NAME).then(cache => {
        console.log('Service Worker: Pre-caching CV files');
        return cache.addAll([
          '/assets/tex/cv-en-tomMOULARD.pdf',
          '/assets/tex/cv-fr-tomMOULARD.pdf'
        ]).catch(error => {
          console.log('Service Worker: CV files failed to cache:', error);
          return Promise.allSettled([
            cache.add('/assets/tex/cv-en-tomMOULARD.pdf'),
            cache.add('/assets/tex/cv-fr-tomMOULARD.pdf')
          ]);
        });
      })
    ]).then(() => {
      console.log('Service Worker: Installation complete');
      return self.skipWaiting();
    }).catch(error => {
      console.log('Service Worker: Installation failed:', error);
      return self.skipWaiting();
    })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  console.log('Service Worker: Activating...');

  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME && cacheName !== CV_CACHE_NAME) {
            console.log('Service Worker: Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      console.log('Service Worker: Activation complete');
      return self.clients.claim();
    })
  );
});

// Fetch event - serve from cache with network fallback
self.addEventListener('fetch', event => {
  const request = event.request;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }

  // Skip external requests
  if (url.origin !== location.origin) {
    return;
  }

  event.respondWith(
    caches.match(request).then(response => {
      // Return cached version if available
      if (response) {
        console.log('Service Worker: Serving from cache:', request.url);
        return response;
      }

      // Otherwise, fetch from network and cache
      return fetch(request).then(fetchResponse => {
        // Don't cache non-successful responses
        if (!fetchResponse || fetchResponse.status !== 200 || fetchResponse.type !== 'basic') {
          return fetchResponse;
        }

        // Clone the response
        const responseToCache = fetchResponse.clone();

        // Determine which cache to use
        let cacheToUse = CACHE_NAME;
        if (request.url.includes('/assets/tex/cv-') && request.url.endsWith('.pdf')) {
          cacheToUse = CV_CACHE_NAME;
        }

        // Cache the response
        caches.open(cacheToUse).then(cache => {
          console.log('Service Worker: Caching new resource:', request.url);
          cache.put(request, responseToCache);
        });

        return fetchResponse;
      }).catch(error => {
        console.log('Service Worker: Fetch failed:', request.url, error);

        // Return offline page for navigation requests
        if (request.mode === 'navigate') {
          return caches.match('/') || caches.match('/fr/');
        }

        // Return cached CV if available for CV requests
        if (request.url.includes('/assets/tex/cv-') && request.url.endsWith('.pdf')) {
          return caches.match(request.url);
        }

        throw error;
      });
    })
  );
});

// Message event - handle cache management commands
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }

  if (event.data && event.data.type === 'GET_CACHE_SIZE') {
    caches.keys().then(cacheNames => {
      Promise.all(
        cacheNames.map(cacheName =>
          caches.open(cacheName).then(cache =>
            cache.keys().then(keys => ({ name: cacheName, size: keys.length }))
          )
        )
      ).then(results => {
        event.ports[0].postMessage({ type: 'CACHE_SIZE', data: results });
      });
    });
  }
});

console.log('Service Worker: Script loaded');