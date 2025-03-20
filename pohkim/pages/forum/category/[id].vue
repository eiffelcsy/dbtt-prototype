<template>
  <div class="category min-h-screen bg-gray-900 text-white p-8">
    <div v-if="loading" class="flex justify-center items-center h-64">
      <div class="loader"></div>
    </div>

    <div v-else-if="error" class="text-center text-red-500 p-8">
      <p>{{ error }}</p>
      <div class="mt-6 flex flex-col items-center gap-4">
        <button @click="loadCategory" class="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
          Try Again
        </button>
        <NuxtLink to="/forum" class="text-gray-400 hover:text-white">
          Back to Community Home
        </NuxtLink>
      </div>
    </div>

    <template v-else-if="category">
      <!-- Breadcrumb -->
      <div class="flex items-center mb-6 text-sm">
        <NuxtLink to="/forum" class="text-gray-400 hover:text-white">Community</NuxtLink>
        <span class="mx-2 text-gray-600">→</span>
        <span class="text-gray-300">{{ category.name }}</span>
      </div>

      <!-- Category Header -->
      <div class="bg-gray-800 rounded-lg p-6 mb-8">
        <div class="flex items-start gap-4">
          <div class="bg-gray-700 rounded-lg p-3">
            <span class="text-3xl">{{ category.icon }}</span>
          </div>
          <div>
            <h1 class="text-2xl font-bold mb-2">{{ category.name }}</h1>
            <p class="text-gray-400">{{ category.description }}</p>
            <div class="flex gap-4 mt-4 text-sm text-gray-400">
              <div>
                <span class="font-semibold text-white">{{ category.topics }}</span> topics
              </div>
              <div>
                <span class="font-semibold text-white">{{ category.posts }}</span> posts
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Topics List -->
      <div class="mb-8">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-xl font-semibold">Topics</h2>
          <NuxtLink to="/forum/new-topic" class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md transition-colors duration-200">
            New Topic
          </NuxtLink>
        </div>

        <div v-if="categoryTopics.length > 0" class="bg-gray-800 rounded-lg overflow-hidden">
          <div v-for="(topic, index) in categoryTopics" :key="topic.id" 
               :class="['p-6 flex flex-col md:flex-row md:items-center', index < categoryTopics.length - 1 ? 'border-b border-gray-700' : '']">
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

        <div v-else class="text-center py-12 bg-gray-800 rounded-lg">
          <p class="text-gray-400">No topics yet in this category.</p>
          <NuxtLink to="/forum/new-topic" class="inline-block mt-4 bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded-md transition-colors duration-200">
            Start the First Topic
          </NuxtLink>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const loading = ref(true);
const error = ref(null);
const category = ref(null);
const categoryTopics = ref([]);

async function loadCategory() {
  loading.value = true;
  error.value = null;
  
  try {
    const categoryId = route.params.id;
    
    // Load categories
    const categoriesResponse = await fetch('/forum-categories.json');
    const categories = await categoriesResponse.json();
    const categoryData = categories.find(c => c.id === parseInt(categoryId));
    
    if (!categoryData) {
      throw new Error('Category not found');
    }
    
    category.value = categoryData;
    
    // Load topics
    const topicsResponse = await fetch('/forum-topics.json');
    const allTopics = await topicsResponse.json();
    categoryTopics.value = allTopics.filter(topic => topic.category === parseInt(categoryId));
    
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  loadCategory();
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