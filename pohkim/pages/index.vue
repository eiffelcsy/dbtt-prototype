<template>
  <div class="home min-h-screen bg-gray-900 text-white">
    <section class="hero bg-cover bg-center h-96 flex items-center justify-center text-white">
      <div class="hero-bg absolute inset-0 bg-[url('/images/hero-bg.jpg')] filter brightness-50"></div>
      <div class="text-center relative z-10">
        <h1 class="text-4xl font-bold mb-2">Welcome to Pohkim Streaming</h1>
        <p class="text-lg mb-6">Transition from DVD to Digital Streaming</p>
        <button class="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-6 rounded-md transition-colors duration-300">
          Start Watching
        </button>
      </div>
    </section>
    <section class="trending p-8">
      <h2 class="text-2xl font-semibold mb-4">Trending Videos</h2>
      <div class="trending-videos flex space-x-4 overflow-x-auto pb-4">
        <VideoCard 
          v-for="video in trendingVideos" 
          :key="video.id" 
          :video="video" 
          class="flex-shrink-0 w-64"
        />
      </div>
    </section>
    <section class="categories p-8">
      <h2 class="text-2xl font-semibold mb-4">Categories</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div v-for="category in categories" :key="category.id" 
             class="category bg-gray-800 rounded-lg p-4 hover:bg-gray-700 transition-colors duration-300 cursor-pointer">
          <h3 class="text-xl font-semibold mb-2">{{ category.name }}</h3>
          <p class="text-gray-400 text-sm">{{ category.videoCount }} videos</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import VideoCard from '~/components/VideoCard.vue';

const trendingVideos = ref([]);
const categories = ref([
  { id: 1, name: 'Action', videoCount: 42 },
  { id: 2, name: 'Drama', videoCount: 38 },
  { id: 3, name: 'Comedy', videoCount: 31 },
  { id: 4, name: 'Sci-Fi', videoCount: 27 },
  { id: 5, name: 'Horror', videoCount: 18 },
  { id: 6, name: 'Documentary', videoCount: 23 },
  { id: 7, name: 'Animation', videoCount: 19 },
  { id: 8, name: 'Thriller', videoCount: 25 }
]);

onMounted(async () => {
  try {
    const response = await fetch('/videos.json');
    const allVideos = await response.json();
    trendingVideos.value = allVideos.slice(0, 6); // Display first 6 videos as trending
  } catch (error) {
    console.error('Error loading trending videos:', error);
  }
});
</script>

<style scoped>
.hero {
  position: relative;
}
.hero-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  background-size: cover;
  background-repeat: no-repeat;
}
.trending-videos::-webkit-scrollbar {
  height: 8px;
}
.trending-videos::-webkit-scrollbar-track {
  background: #1f2937;
  border-radius: 4px;
}
.trending-videos::-webkit-scrollbar-thumb {
  background: #4b5563;
  border-radius: 4px;
}
.trending-videos::-webkit-scrollbar-thumb:hover {
  background: #6b7280;
}
</style>