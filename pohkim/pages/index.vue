<template>
  <div class="home-page min-h-screen bg-gray-900 text-white">
    <!-- Hero Section -->
    <div class="relative">
      <div class="absolute inset-0 z-0">
        <img src="/images/hero.jpg" alt="Hero Background" class="w-full h-full object-cover">
      </div>
      <div class="absolute inset-0 bg-gradient-to-r from-black to-transparent opacity-80 z-10"></div>
      <div class="h-[70vh] flex items-center">
        <div class="container mx-auto px-4 relative z-20">
          <div class="max-w-2xl">
            <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold mb-4">Welcome to Poh Kim</h1>
            <p class="text-xl md:text-2xl text-gray-300 mb-8">Your ultimate destination for premium DVD collections with exclusive trailers and a vibrant community.</p>
            <div class="flex flex-wrap gap-4">
              <NuxtLink to="/store" class="bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-6 rounded-lg transition-colors duration-300">
                Browse DVD Store
              </NuxtLink>
              <NuxtLink to="/forum" class="bg-gray-800 hover:bg-gray-700 text-white font-bold py-3 px-6 rounded-lg transition-colors duration-300">
                Join Community
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Featured Content Section -->
    <section class="py-12 bg-gray-900">
      <div class="container mx-auto px-4">
        <h2 class="text-3xl font-bold mb-8">Featured DVDs</h2>
        
        <div v-if="loading" class="flex justify-center items-center h-64">
          <div class="loader"></div>
        </div>
        
        <div v-else-if="error" class="text-center text-red-500 p-8">
          <p>{{ error }}</p>
        </div>
        
        <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <!-- Featured DVD -->
          <div v-if="featuredDVD" class="bg-gray-800 rounded-lg overflow-hidden">
            <div class="aspect-video bg-gradient-to-br from-red-900 to-gray-900 relative">
              <div v-if="!featuredDVD.thumbnail" class="absolute inset-0 flex items-center justify-center">
                <span class="text-6xl font-bold text-white opacity-30">{{ featuredDVD.title.substring(0, 2) }}</span>
              </div>
              <img v-else :src="featuredDVD.thumbnail" :alt="featuredDVD.title" class="absolute inset-0 w-full h-full object-cover">
              <div class="absolute top-4 left-4 bg-red-600 text-white text-xs font-bold px-2 py-1 rounded">
                FEATURED
              </div>
              <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black to-transparent p-6">
                <h3 class="text-2xl font-bold mb-2">{{ featuredDVD.title }}</h3>
                <div class="flex items-center text-sm text-gray-300 mb-2">
                  <span>{{ new Date(featuredDVD.releaseDate).getFullYear() }}</span>
                  <span class="mx-2">•</span>
                  <span>{{ featuredDVD.genre }}</span>
                  <span class="mx-2">•</span>
                  <span>{{ featuredDVD.duration }}</span>
                </div>
                <div class="flex">
                  <span class="text-yellow-400">★★★★★</span>
                  <span class="ml-1 text-sm">{{ featuredDVD.rating }}/5</span>
                </div>
              </div>
            </div>
            <div class="p-6">
              <p class="text-gray-300 mb-4">{{ featuredDVD.description.length > 250 ? featuredDVD.description.substring(0, 250) + '...' : featuredDVD.description }}</p>
              <div class="flex gap-3">
                <button @click="openProductOverlay(featuredDVD.id)" class="bg-gray-700 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded transition-colors duration-300">
                  Buy DVD
                </button>
              </div>
            </div>
          </div>
          
          <!-- Second Featured DVD (if available, otherwise show a placeholder) -->
          <div v-if="newReleases.length > 0" class="bg-gray-800 rounded-lg overflow-hidden">
            <div class="aspect-video bg-gradient-to-br from-blue-900 to-gray-900 relative">
              <div v-if="!newReleases[0].thumbnail" class="absolute inset-0 flex items-center justify-center">
                <span class="text-6xl font-bold text-white opacity-30">{{ newReleases[0].title.substring(0, 2) }}</span>
              </div>
              <img v-else :src="newReleases[0].thumbnail" :alt="newReleases[0].title" class="absolute inset-0 w-full h-full object-cover">
              <div class="absolute top-4 left-4 bg-blue-600 text-white text-xs font-bold px-2 py-1 rounded">
                NEW RELEASE
              </div>
              <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black to-transparent p-6">
                <h3 class="text-2xl font-bold mb-2">{{ newReleases[0].title }}</h3>
                <div class="flex items-center text-sm text-gray-300 mb-2">
                  <span>{{ new Date(newReleases[0].releaseDate).getFullYear() }}</span>
                  <span class="mx-2">•</span>
                  <span>{{ newReleases[0].genre }}</span>
                  <span class="mx-2">•</span>
                  <span>{{ newReleases[0].duration }}</span>
                </div>
                <div class="flex">
                  <span class="text-yellow-400">★★★★★</span>
                  <span class="ml-1 text-sm">{{ newReleases[0].rating }}/5</span>
                </div>
              </div>
            </div>
            <div class="p-6">
              <p class="text-gray-300 mb-4">{{ newReleases[0].description.length > 250 ? newReleases[0].description.substring(0, 250) + '...' : newReleases[0].description }}</p>
              <div class="flex gap-3">
                <button @click="openProductOverlay(newReleases[0].id)" class="bg-gray-700 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded transition-colors duration-300">
                  Buy DVD
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- DVD Store Section -->
    <section class="py-12 bg-gray-900">
      <div class="container mx-auto px-4">
        <div class="flex justify-between items-center mb-8">
          <h2 class="text-3xl font-bold">New DVD Releases</h2>
          <NuxtLink to="/store" class="text-red-500 hover:text-red-400 font-semibold">
            Shop All DVDs
          </NuxtLink>
        </div>
        
        <div v-if="loading" class="flex justify-center items-center h-64">
          <div class="loader"></div>
        </div>
        
        <div v-else-if="error" class="text-center text-red-500 p-8">
          <p>{{ error }}</p>
        </div>
        
        <div v-else-if="newReleases.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          <div v-for="video in newReleases" :key="video.id" class="bg-gray-800 rounded-lg overflow-hidden hover:shadow-lg transition-shadow duration-300 cursor-pointer" @click="openProductOverlay(video.id)">
            <div class="aspect-[3/4] relative bg-gradient-to-br from-gray-700 to-gray-900 flex items-center justify-center">
              <img v-if="video.thumbnail" :src="video.thumbnail" :alt="video.title" class="w-full h-full object-cover">
              <span v-else class="text-4xl font-bold text-white opacity-30">{{ video.title.substring(0, 2) }}</span>
              
              <!-- Format Badge -->
              <div class="absolute top-2 right-2 bg-red-600 text-white text-xs font-bold px-2 py-1 rounded">
                {{ video.format }}
              </div>
            </div>
            
            <div class="p-4">
              <h3 class="font-bold text-lg mb-1 hover:text-red-500 transition-colors truncate">{{ video.title }}</h3>
              <p class="text-gray-400 text-sm mb-2 truncate">{{ video.genre }}</p>
              <div class="flex justify-between items-center">
                <span class="font-bold">${{ video.price }}</span>
                <div class="flex">
                  <span class="text-yellow-400">★★★★</span>
                  <span class="text-sm ml-1">{{ video.rating }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Community Section -->
    <section class="py-12 bg-gray-800">
      <div class="container mx-auto px-4">
        <div class="flex justify-between items-center mb-8">
          <h2 class="text-3xl font-bold">Community Discussions</h2>
          <NuxtLink to="/forum" class="text-red-500 hover:text-red-400 font-semibold">
            Join the Community
          </NuxtLink>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="i in 3" :key="i" class="bg-gray-900 rounded-lg overflow-hidden border border-gray-700 hover:border-gray-600 transition-colors duration-300">
            <div class="p-6">
              <div class="flex items-start mb-4">
                <div class="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center mr-3">
                  <span class="text-sm font-bold">{{ ['S', 'F', 'B'][i-1] }}</span>
                </div>
                <div>
                  <h3 class="font-semibold text-lg hover:text-red-500 transition-colors">
                    <NuxtLink :to="`/forum/topic/${100+i}`">
                      {{ [
                        'What did everyone think of the Cosmic Odyssey ending?',
                        'Top 5 sci-fi movies of the last decade - what are yours?',
                        'Fantasy series with the best world-building?'
                      ][i-1] }}
                    </NuxtLink>
                  </h3>
                  <div class="flex items-center text-sm text-gray-400 mt-1">
                    <span>{{ ['SpaceExplorer42', 'FilmBuff2023', 'BookWorm'][i-1] }}</span>
                    <span class="mx-2">•</span>
                    <span>{{ ['2 hours ago', '1 day ago', '5 days ago'][i-1] }}</span>
                    <span class="mx-2">•</span>
                    <span>{{ ['24 replies', '37 replies', '42 replies'][i-1] }}</span>
                  </div>
                </div>
              </div>
              <p class="text-gray-400 text-sm line-clamp-2">
                {{ [
                  'I just finished watching Cosmic Odyssey and that twist at the end completely blew my mind! The way they revealed that the entire journey was actually happening in a parallel universe was so unexpected.',
                  'I\'ve been thinking about my favorite sci-fi films from the past decade and wanted to share my top 5. What are yours? I\'m always looking for great recommendations!',
                  'I\'m a huge fan of fantasy worlds with deep lore and history. Which series do you think has the most immersive and well-developed world-building?'
                ][i-1] }}
              </p>
            </div>
            <div class="px-6 py-3 bg-gray-800 flex justify-between items-center">
              <div class="flex items-center text-sm text-gray-400">
                <span>Category: </span>
                <NuxtLink to="/forum/category/3" class="ml-1 text-red-500 hover:text-red-400">
                  Sci-Fi & Fantasy
                </NuxtLink>
              </div>
              <NuxtLink :to="`/forum/topic/${100+i}`" class="text-sm text-white hover:text-red-500">
                Join Discussion →
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Trailer Modal -->
    <div v-if="showTrailerModal" class="fixed inset-0 bg-black bg-opacity-90 flex items-center justify-center z-50">
      <div class="relative w-full max-w-4xl">
        <button @click="closeTrailer" class="absolute -top-10 right-0 text-white hover:text-gray-300">
          Close ✕
        </button>
        <div class="bg-black aspect-video flex items-center justify-center">
          <p class="text-center text-gray-400">
            This is a prototype. Trailer playback for product #{{ currentTrailerId }} would be implemented here in the production version.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useProductStore } from '~/composables/useProductStore';

const videos = ref([]);
const featuredDVD = ref(null);
const newReleases = ref([]);
const loading = ref(true);
const error = ref(null);
const showTrailerModal = ref(false);
const currentTrailerId = ref(null);
const productStore = useProductStore();

// Function to show trailer
function showTrailer(id) {
  currentTrailerId.value = id;
  showTrailerModal.value = true;
}

// Function to close trailer
function closeTrailer() {
  showTrailerModal.value = false;
}

// Function to open product overlay
function openProductOverlay(productId) {
  const product = videos.value.find(v => v.id === productId);
  if (product) {
    productStore.openProductOverlay(product);
  }
}

// Function to load videos from videos.json
async function loadVideos() {
  try {
    const response = await fetch('/videos.json');
    if (!response.ok) {
      throw new Error('Failed to fetch videos');
    }
    
    const data = await response.json();
    videos.value = data;
    
    // Find featured DVD (ID 67)
    featuredDVD.value = videos.value.find(video => video.id === 67);
    
    // If featured DVD not found, use first video as fallback
    if (!featuredDVD.value && videos.value.length > 0) {
      featuredDVD.value = videos.value[0];
    }
    
    // Get 4 random videos for new releases
    const randomVideos = [...videos.value]; // Create a copy
    randomVideos.sort(() => Math.random() - 0.5); // Shuffle array
    newReleases.value = randomVideos.slice(0, 4); // Take first 4
    
    loading.value = false;
  } catch (err) {
    console.error('Error loading videos:', err);
    error.value = err.message;
    loading.value = false;
  }
}

onMounted(() => {
  loadVideos();
});
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

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
</style>