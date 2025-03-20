<template>
  <div class="forum-topic min-h-screen bg-gray-900 text-white p-8">
    <div v-if="loading" class="flex justify-center items-center h-64">
      <div class="loader"></div>
    </div>

    <div v-else-if="error" class="text-center text-red-500 p-8">
      <p>{{ error }}</p>
      <div class="mt-6 flex flex-col items-center gap-4">
        <button @click="loadTopic" class="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
          Try Again
        </button>
        <NuxtLink to="/forum" class="text-gray-400 hover:text-white">
          Back to Community Home
        </NuxtLink>
      </div>
    </div>

    <template v-else-if="topic">
      <!-- Breadcrumb -->
      <div class="flex items-center mb-6 text-sm">
        <NuxtLink to="/forum" class="text-gray-400 hover:text-white">Community</NuxtLink>
        <span class="mx-2 text-gray-600">→</span>
        <NuxtLink :to="`/forum/category/${topic.category}`" class="text-gray-400 hover:text-white">
          {{ getCategoryName(topic.category) }}
        </NuxtLink>
        <span class="mx-2 text-gray-600">→</span>
        <span class="text-gray-300">{{ topic.title }}</span>
      </div>

      <!-- Topic Header -->
      <div class="bg-gray-800 rounded-lg p-6 mb-6">
        <h1 class="text-2xl font-bold mb-4">{{ topic.title }}</h1>
        <div class="flex items-center text-sm text-gray-400">
          <div class="flex items-center">
            <div class="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center mr-2">
              <span class="font-bold">{{ topic.author[0] }}</span>
            </div>
            <span>{{ topic.author }}</span>
          </div>
          <span class="mx-2">•</span>
          <span>{{ topic.date }}</span>
          <span class="mx-2">•</span>
          <span>{{ topic.views }} views</span>
        </div>
      </div>

      <!-- Original Post -->
      <div class="bg-gray-800 rounded-lg p-6 mb-6">
        <div class="prose prose-invert max-w-none">
          {{ topic.content }}
        </div>
      </div>

      <!-- Replies -->
      <div class="mb-6">
        <h2 class="text-xl font-bold mb-4">Replies ({{ topic.replies }})</h2>
        <div v-if="replies.length > 0" class="space-y-4">
          <div v-for="reply in replies" :key="reply.id" class="bg-gray-800 rounded-lg p-6">
            <div class="flex items-center mb-4">
              <div class="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center mr-2">
                <span class="font-bold">{{ reply.author[0] }}</span>
              </div>
              <div>
                <div class="font-semibold">{{ reply.author }}</div>
                <div class="text-sm text-gray-400">{{ reply.date }}</div>
              </div>
            </div>
            <div class="prose prose-invert max-w-none">
              {{ reply.content }}
            </div>
          </div>
        </div>
        <div v-else class="bg-gray-800 rounded-lg p-6 text-center">
          <p class="text-gray-400">No replies yet. Be the first to reply!</p>
        </div>
      </div>

      <!-- Reply Form -->
      <div class="bg-gray-800 rounded-lg p-6">
        <h3 class="text-lg font-bold mb-4">Leave a Reply</h3>
        <div class="mb-4">
          <textarea
            v-model="newReply"
            rows="4"
            class="w-full bg-gray-700 text-white rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-red-500"
            placeholder="Write your reply..."
          ></textarea>
        </div>
        <div class="flex justify-end">
          <button
            @click="submitReply"
            class="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-6 rounded transition-colors duration-200"
          >
            Post Reply
          </button>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const loading = ref(true);
const error = ref(null);
const topic = ref(null);
const replies = ref([]);
const newReply = ref('');
const categories = ref({});

async function loadTopic() {
  loading.value = true;
  error.value = null;
  
  try {
    const topicId = route.params.id;
    
    // Load categories
    const categoriesResponse = await fetch('/forum-categories.json');
    const categoriesData = await categoriesResponse.json();
    // Convert categories array to an object for easier lookup
    categoriesData.forEach(cat => {
      categories.value[cat.id] = cat.name;
    });
    
    // Load topics
    const topicsResponse = await fetch('/forum-topics.json');
    const allTopics = await topicsResponse.json();
    const topicData = allTopics.find(t => t.id === parseInt(topicId));
    
    if (!topicData) {
      throw new Error('Topic not found');
    }
    
    topic.value = topicData;
    
    // Load replies
    const repliesResponse = await fetch('/forum-replies.json');
    const allReplies = await repliesResponse.json();
    replies.value = allReplies[topicId] || [];
    
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
}

function submitReply() {
  if (!newReply.value.trim()) return;
  
  // In a real app, this would be an API call
  const reply = {
    id: replies.value.length + 1,
    author: 'CurrentUser', // In a real app, this would come from auth
    date: 'Just now',
    content: newReply.value
  };
  
  replies.value.push(reply);
  newReply.value = '';
}

function getCategoryName(categoryId) {
  return categories.value[categoryId] || 'Unknown Category';
}

onMounted(() => {
  loadTopic();
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

.prose {
  color: #e5e7eb;
  line-height: 1.6;
}

.prose p {
  margin-bottom: 1rem;
}
</style> 