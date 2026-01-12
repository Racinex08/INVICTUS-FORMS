importScripts('https://www.gstatic.com/firebasejs/10.7.1/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.7.1/firebase-messaging-compat.js');

const firebaseConfig = {
  apiKey: "AIzaSyAQxRxoH8UdnC5t5nxAbPUemwT-V3peKfM",
  authDomain: "invictus-forms.firebaseapp.com",
  projectId: "invictus-forms",
  storageBucket: "invictus-forms.firebasestorage.app",
  messagingSenderId: "175025854516",
  appId: "1:175025854516:web:d0256e3d40de07172b5261",
  measurementId: "G-HDTKK6J61G"
};

firebase.initializeApp(firebaseConfig);
const messaging = firebase.messaging();

// Manejar notificaciones en segundo plano
messaging.onBackgroundMessage((payload) => {
  console.log('[sw.js] Notificación recibida en segundo plano:', payload);
  const notificationTitle = payload.notification.title || "INVICTUS JUVENIL";
  const notificationOptions = {
    body: payload.notification.body,
    icon: 'https://cdn-icons-png.flaticon.com/512/3119/3119338.png',
    badge: 'https://cdn-icons-png.flaticon.com/512/3119/3119338.png'
  };

  self.registration.showNotification(notificationTitle, notificationOptions);
});

// Lógica de Cache original
const CACHE_NAME = 'invictus-v1';
const ASSETS = [
  './index.html',
  './manifest.json',
  'https://cdn-icons-png.flaticon.com/512/3119/3119338.png'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
});

self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((res) => res || fetch(e.request))
  );
});
