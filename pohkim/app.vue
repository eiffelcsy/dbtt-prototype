<template>
  <div class="app bg-gray-900 min-h-screen text-white">
    <Header />
    <div class="main-content">
      <NuxtPage />
    </div>
    <Footer />
  </div>
</template>

<script setup>
import Header from '~/components/Header.vue';
import Footer from '~/components/Footer.vue';
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

:root {
  --primary: #EF4444;
  --dark-bg: #111827;
  --dark-surface: #1F2937;
  --text: #F9FAFB;
  --text-secondary: #D1D5DB;
}

body {
  background-color: var(--dark-bg);
  color: var(--text);
}

.main-content {
  min-height: calc(100vh - 300px); /* Adjust based on header/footer height */
}

/* For smoother scrolling */
html {
  scroll-behavior: smooth;
}

/* Hide scrollbar but still allow scrolling */
::-webkit-scrollbar {
  width: 5px;
  height: 5px;
}

::-webkit-scrollbar-track {
  background: #1F2937;
}

::-webkit-scrollbar-thumb {
  background: #4B5563;
  border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
  background: #6B7280;
}
</style>
