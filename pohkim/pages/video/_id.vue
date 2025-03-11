<template>
  <div class="video-detail min-h-screen bg-gray-900 text-white">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center min-h-screen">
      <div class="loader"></div>
    </div>
    
    <!-- Error State -->
    <div v-else-if="error" class="text-center p-8">
      <p class="text-red-500 mb-4">{{ error }}</p>
      <button @click="loadVideo" class="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
        Try Again
      </button>
    </div>
    
    <!-- Video Not Found -->
    <div v-else-if="!video" class="text-center p-16">
      <h1 class="text-3xl font-bold mb-4">Video Not Found</h1>
      <p class="mb-8">The video you're looking for doesn't exist or has been removed.</p>
      <NuxtLink to="/movies" class="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
        Browse Movies
      </NuxtLink>
    </div>
    
    <!-- Video Content -->
    <div v-else>
      <!-- Hero Banner -->
      <div class="relative h-96">
        <div class="absolute inset-0 bg-gradient-to-r from-gray-900 via-transparent to-transparent z-10"></div>
        <img :src="video.thumbnail || '/images/default-banner.jpg'" alt="Video Banner" class="w-full h-full object-cover">
        
        <div class="absolute bottom-0 left-0 p-8 z-20 w-full md:w-2/3">
          <h1 class="text-4xl font-bold mb-2">{{ video.title }}</h1>
          <div class="flex items-center text-sm text-gray-400 mb-4">
            <span>{{ video.releaseDate }}</span>
            <span class="mx-2">•</span>
            <span>{{ video.genre }}</span>
            <span class="mx-2">•</span>
            <span>HD</span>
          </div>
          <p class="text-gray-300 mb-6">{{ video.description }}</p>
          <div class="flex space-x-4">
            <button @click="showPlayer = true" class="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-6 rounded flex items-center">
              <span class="mr-2">▶</span> Play
            </button>
            <button class="bg-gray-700 hover:bg-gray-600 text-white font-bold py-2 px-6 rounded">
              + My List
            </button>
          </div>
        </div>
      </div>
      
      <!-- Video Player Modal -->
      <div v-if="showPlayer" class="fixed inset-0 bg-black bg-opacity-90 flex items-center justify-center z-50">
        <div class="relative w-full max-w-4xl">
          <button @click="showPlayer = false" class="absolute -top-10 right-0 text-white hover:text-gray-300">
            Close ✕
          </button>
          <div class="bg-black aspect-video flex items-center justify-center">
            <p class="text-center text-gray-400">
              This is a prototype. Video playback would be implemented here in the production version.
            </p>
          </div>
        </div>
      </div>
      
      <!-- Additional Information -->
      <div class="container mx-auto p-8">
        <h2 class="text-2xl font-semibold mb-4">More Like This</h2>
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          <div 
            v-for="i in 5" 
            :key="i" 
            class="similar-video bg-gray-800 rounded overflow-hidden h-64 animate-pulse"
          ></div>
        </div>
        
        <div class="mt-12 bg-gray-800 p-6 rounded-lg">
          <h2 class="text-2xl font-semibold mb-4">About "{{ video.title }}"</h2>
          <p class="mb-4">{{ video.description }}</p>
          <p class="text-gray-400">
            This is a prototype demonstration of how a DVD retailer could transition to digital streaming.
            In a production version, this section would contain more detailed information about the video,
            including cast, director, and additional metadata.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const video = ref(null);
const loading = ref(true);
const error = ref(null);
const showPlayer = ref(false);

async function loadVideo() {
  loading.value = true;
  error.value = null;
  
  try {
    const response = await fetch('/videos.json');
    if (!response.ok) {
      throw new Error('Failed to fetch video data');
    }
    
    const videos = await response.json();
    video.value = videos.find(v => v.id === parseInt(route.params.id));
    
    // If video not found, could redirect or handle as needed
    if (!video.value) {
      console.warn('Video not found');
    }
  } catch (err) {
    console.error('Error loading video:', err);
    error.value = 'There was a problem loading the video. Please try again.';
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  loadVideo();
});
</script>

<style scoped>
.loader {
  border: 4px solid rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  border-top: 4px solid #fff;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: .5; }
}
</style> 