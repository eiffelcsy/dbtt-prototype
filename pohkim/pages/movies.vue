<template>
  <div class="movies min-h-screen bg-gray-900 text-white p-8">
    <div class="mb-8">
      <h1 class="text-3xl font-bold mb-6">Movies & Shows</h1>
      
      <!-- Filters -->
      <div class="filters flex flex-wrap gap-4 mb-6">
        <div class="filter-group">
          <label class="block text-gray-400 text-sm mb-2">Genre</label>
          <select v-model="selectedGenre" class="bg-gray-800 text-white rounded p-2 border border-gray-700 w-full md:w-48">
            <option value="">All Genres</option>
            <option v-for="genre in genres" :key="genre" :value="genre">{{ genre }}</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label class="block text-gray-400 text-sm mb-2">Sort By</label>
          <select v-model="sortBy" class="bg-gray-800 text-white rounded p-2 border border-gray-700 w-full md:w-48">
            <option value="title">Title</option>
            <option value="releaseDate">Release Date</option>
          </select>
        </div>
        
        <div class="filter-group ml-auto">
          <label class="block text-gray-400 text-sm mb-2">Search</label>
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Search videos..." 
            class="bg-gray-800 text-white rounded p-2 border border-gray-700 w-full md:w-64"
          >
        </div>
      </div>
    </div>
    
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center h-64">
      <div class="loader">Loading...</div>
    </div>
    
    <!-- Error State -->
    <div v-else-if="error" class="text-center text-red-500 p-8">
      <p>{{ error }}</p>
      <button @click="loadVideos" class="mt-4 bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
        Try Again
      </button>
    </div>
    
    <!-- Video Grid -->
    <div v-else>
      <div v-if="filteredVideos.length === 0" class="text-center text-gray-400 p-16">
        <p>No videos found matching your criteria.</p>
      </div>
      
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
        <VideoCard v-for="video in filteredVideos" :key="video.id" :video="video" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import VideoCard from '~/components/VideoCard.vue';

const videos = ref([]);
const loading = ref(true);
const error = ref(null);
const searchQuery = ref('');
const selectedGenre = ref('');
const sortBy = ref('title');

const genres = computed(() => {
  const genreSet = new Set(videos.value.map(video => video.genre));
  return [...genreSet];
});

const filteredVideos = computed(() => {
  let result = [...videos.value];
  
  // Filter by genre
  if (selectedGenre.value) {
    result = result.filter(video => video.genre === selectedGenre.value);
  }
  
  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(video => 
      video.title.toLowerCase().includes(query) || 
      video.description.toLowerCase().includes(query)
    );
  }
  
  // Sort videos
  result.sort((a, b) => {
    if (sortBy.value === 'title') {
      return a.title.localeCompare(b.title);
    } else if (sortBy.value === 'releaseDate') {
      return new Date(b.releaseDate) - new Date(a.releaseDate);
    }
    return 0;
  });
  
  return result;
});

async function loadVideos() {
  loading.value = true;
  error.value = null;
  
  try {
    const response = await fetch('/videos.json');
    if (!response.ok) {
      throw new Error('Failed to fetch videos');
    }
    videos.value = await response.json();
  } catch (err) {
    console.error('Error loading videos:', err);
    error.value = 'There was a problem loading videos. Please try again.';
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  loadVideos();
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
</style> 