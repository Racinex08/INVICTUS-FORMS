/*
 * Firebase Messaging Service Worker - Compatible con GitHub Pages
 * Mantener en la RAÍZ del repositorio
 */

// Importa Firebase (versión compat)
importScripts('https://www.gstatic.com/firebasejs/10.7.1/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.7.1/firebase-messaging-compat.js');

firebase.initializeApp({
  apiKey: "AIzaSyCGOi3sF7tDHr8MiMFSMK4VTFz1KnKCBqo",
  authDomain: "invictus-pwa-cc9e0.firebaseapp.com",
  projectId: "invictus-pwa-cc9e0",
  storageBucket: "invictus-pwa-cc9e0.appspot.com",
  messagingSenderId: "103953800507",
  appId: "1:103953800507:web:some-app-id"
});

const messaging = firebase.messaging();

// Manejar mensajes en background
messaging.onBackgroundMessage(function(payload) {
  console.log('[SW] Mensaje en background recibido:', payload);
  const { title, body, icon } = payload.notification || {};
  self.registration.showNotification(title || 'INVICTUS JUVENIL', {
    body: body || '',
    icon: icon || 'https://cdn-icons-png.flaticon.com/512/3119/3119338.png',
    badge: 'https://cdn-icons-png.flaticon.com/512/3119/3119338.png',
    data: payload.data
  });
});

// Cache básico para funcionamiento offline
const CACHE_NAME = 'invictus-v3';
const URLS_TO_CACHE = ['./'];

self.addEventListener('install', event => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(URLS_TO_CACHE))
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  // Solo cachear GET, y solo recursos del mismo origen
  if (event.request.method !== 'GET') return;
  const url = new URL(event.request.url);
  if (url.origin !== self.location.origin) return;
  
  event.respondWith(
    caches.match(event.request).then(cached => cached || fetch(event.request))
  );
});
