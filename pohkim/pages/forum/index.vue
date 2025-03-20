<template>
  <div class="forum min-h-screen bg-gray-900 text-white p-8">
    <div class="mb-8">
      <h1 class="text-3xl font-bold mb-2">Pohkim Community</h1>
      <p class="text-gray-400">Join discussions about your favorite films with fellow enthusiasts.</p>
    </div>
    
    <!-- Community Stats -->
    <div v-if="!forumStats" class="bg-gray-800 rounded-lg p-6 mb-8 flex justify-center">
      <div class="loader"></div>
    </div>
    <div v-else class="bg-gray-800 rounded-lg p-6 mb-8">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
        <div>
          <p class="text-3xl font-bold text-red-500">{{ forumStats.topics }}</p>
          <p class="text-gray-400">Topics</p>
        </div>
        <div>
          <p class="text-3xl font-bold text-red-500">{{ forumStats.posts }}</p>
          <p class="text-gray-400">Posts</p>
        </div>
        <div>
          <p class="text-3xl font-bold text-red-500">{{ forumStats.members }}</p>
          <p class="text-gray-400">Members</p>
        </div>
        <div>
          <p class="text-3xl font-bold text-red-500">{{ forumStats.online }}</p>
          <p class="text-gray-400">Online Now</p>
        </div>
      </div>
    </div>
    
    <!-- Community Categories -->
    <div v-if="categories.length === 0" class="mb-12 bg-gray-800 rounded-lg p-6 flex justify-center">
      <div class="loader"></div>
    </div>
    <div v-else class="mb-12">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-semibold">Categories</h2>
        <div class="flex space-x-2">
          <button class="bg-gray-800 hover:bg-gray-700 text-white px-4 py-2 rounded-md">
            <span class="hidden md:inline">View All Categories</span>
            <span class="md:hidden">All</span>
          </button>
        </div>
      </div>
      
      <div class="grid md:grid-cols-2 gap-4">
        <div v-for="category in categories" :key="category.id" class="bg-gray-800 rounded-lg overflow-hidden hover:bg-gray-750 transition-colors duration-200">
          <NuxtLink :to="`/forum/category/${category.id}`" class="block p-6">
            <div class="flex items-start">
              <div class="bg-gray-700 rounded-lg p-3 mr-4">
                <span class="text-2xl">{{ category.icon }}</span>
              </div>
              <div class="flex-grow">
                <h3 class="text-xl font-semibold mb-1">{{ category.name }}</h3>
                <p class="text-gray-400 text-sm mb-2">{{ category.description }}</p>
                <div class="flex text-sm text-gray-500">
                  <span>{{ category.topics }} topics</span>
                  <span class="mx-2">•</span>
                  <span>{{ category.posts }} posts</span>
                </div>
              </div>
            </div>
          </NuxtLink>
        </div>
      </div>
    </div>
    
    <!-- Recent Discussions -->
    <div v-if="loadingTopics" class="bg-gray-800 rounded-lg p-6 flex justify-center">
      <div class="loader"></div>
    </div>
    <div v-else>
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-semibold">Recent Discussions</h2>
        <NuxtLink to="/forum/new-topic" class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md transition-colors duration-200">
          <span class="hidden md:inline">Start New Topic</span>
          <span class="md:hidden">New</span>
        </NuxtLink>
      </div>
      
      <div class="bg-gray-800 rounded-lg overflow-hidden">
        <div v-for="(topic, index) in displayedTopics" :key="topic.id" 
             :class="['p-6 flex flex-col md:flex-row md:items-center', index < displayedTopics.length - 1 ? 'border-b border-gray-700' : '']">
          <div class="flex-grow mb-4 md:mb-0">
            <div class="flex items-center mb-2">
              <div class="w-8 h-8 rounded-full bg-gray-600 flex items-center justify-center mr-2">
                <span class="text-xs font-bold">{{ topic.author.substring(0, 1) }}</span>
              </div>
              <span class="text-sm text-gray-400">{{ topic.author }}</span>
              <span class="mx-2 text-gray-600">•</span>
              <span class="text-sm text-gray-400">{{ topic.date }}</span>
            </div>
            <NuxtLink :to="`/forum/topic/${topic.id}`" class="text-lg font-semibold hover:text-red-500 transition-colors duration-200">
              {{ topic.title }}
            </NuxtLink>
            <p class="text-gray-400 text-sm mt-1">{{ topic.preview }}</p>
          </div>
          <div class="flex items-center">
            <div class="text-center mr-6">
              <div class="text-lg font-semibold">{{ topic.replies }}</div>
              <div class="text-xs text-gray-400">Replies</div>
            </div>
            <div class="text-center">
              <div class="text-lg font-semibold">{{ topic.views }}</div>
              <div class="text-xs text-gray-400">Views</div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="mt-6 text-center">
        <button 
          @click="loadMoreTopics" 
          class="bg-gray-800 hover:bg-gray-700 text-white px-6 py-2 rounded-md transition-colors duration-200"
          :disabled="loadingMore || noMoreTopics"
          :class="{ 'opacity-50 cursor-not-allowed': noMoreTopics }"
        >
          <span v-if="loadingMore" class="inline-block align-middle mr-2">
            <div class="w-4 h-4 border-2 border-t-transparent border-white rounded-full animate-spin"></div>
          </span>
          <span v-if="noMoreTopics">No More Discussions</span>
          <span v-else>Load More Discussions</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';

const forumStats = ref(null);
const categories = ref([]);
const allTopics = ref([]);
const displayedTopics = ref([]);
const currentPage = ref(1);
const topicsPerPage = ref(10);
const loadingTopics = ref(true);
const loadingMore = ref(false);
const noMoreTopics = computed(() => {
  return displayedTopics.value.length >= allTopics.value.length;
});

async function loadForumData() {
  try {
    loadingTopics.value = true;
    
    // Load forum stats
    const statsResponse = await fetch('/forum-stats.json');
    forumStats.value = await statsResponse.json();

    // Load categories
    const categoriesResponse = await fetch('/forum-categories.json');
    categories.value = await categoriesResponse.json();

    // Load topics
    const topicsResponse = await fetch('/forum-topics.json');
    allTopics.value = await topicsResponse.json();
    
    // Get initial set of topics
    displayedTopics.value = allTopics.value.slice(0, topicsPerPage.value);
    
    loadingTopics.value = false;
  } catch (error) {
    console.error('Error loading forum data:', error);
    loadingTopics.value = false;
  }
}

async function loadMoreTopics() {
  if (loadingMore.value || noMoreTopics.value) return;
  
  try {
    loadingMore.value = true;
    
    // Simulate network delay for loading animation
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // Calculate next page of topics
    currentPage.value++;
    const startIndex = (currentPage.value - 1) * topicsPerPage.value;
    const endIndex = startIndex + topicsPerPage.value;
    const nextPageTopics = allTopics.value.slice(startIndex, endIndex);
    
    // Add new topics to displayed topics
    displayedTopics.value = [...displayedTopics.value, ...nextPageTopics];
    
    loadingMore.value = false;
  } catch (error) {
    console.error('Error loading more topics:', error);
    loadingMore.value = false;
  }
}

onMounted(() => {
  loadForumData();
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