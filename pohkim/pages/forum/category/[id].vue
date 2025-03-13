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

    <template v-else>
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

        <div class="bg-gray-800 rounded-lg overflow-hidden">
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

        <div v-if="categoryTopics.length === 0" class="text-center py-12 bg-gray-800 rounded-lg">
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

// Mock categories data (in a real app, this would come from a store or API)
const categories = {
  '1': {
    id: 1,
    name: 'Action & Adventure',
    description: 'Discuss high-octane action films and adventure epics',
    icon: '🔥',
    topics: 324,
    posts: 1892
  },
  '2': {
    id: 2,
    name: 'Drama & Romance',
    description: 'Share your thoughts on dramatic and romantic stories',
    icon: '💔',
    topics: 287,
    posts: 1456
  },
  '3': {
    id: 3,
    name: 'Sci-Fi & Fantasy',
    description: 'Explore worlds beyond our own and magical realms',
    icon: '🚀',
    topics: 412,
    posts: 2103
  },
  '4': {
    id: 4,
    name: 'Horror & Thriller',
    description: 'For fans of spine-tingling and suspenseful content',
    icon: '👻',
    topics: 198,
    posts: 876
  },
  '5': {
    id: 5,
    name: 'Comedy',
    description: 'Laugh and discuss your favorite comedies',
    icon: '😂',
    topics: 231,
    posts: 1204
  },
  '6': {
    id: 6,
    name: 'Documentary & Educational',
    description: 'Learn and discuss informative content',
    icon: '🧠',
    topics: 156,
    posts: 723
  }
};

// Mock topics data
const allTopics = [
  {
    id: 101,
    title: 'What did everyone think of the Cosmic Odyssey ending?',
    author: 'SpaceExplorer42',
    date: '2 hours ago',
    preview: 'I just finished watching and that twist at the end completely blew my mind! Did anyone else...',
    replies: 24,
    views: 142,
    category: 3
  },
  {
    id: 102,
    title: 'The Last Detective - Plot holes discussion [SPOILERS]',
    author: 'MysteryFan',
    date: '5 hours ago',
    preview: 'I noticed several inconsistencies in the storyline, especially when the detective visits the...',
    replies: 18,
    views: 97,
    category: 4
  },
  {
    id: 103,
    title: 'Whispers of the Heart made me cry - emotional impact thread',
    author: 'FilmBuff2023',
    date: '1 day ago',
    preview: 'I wasn\'t prepared for how emotional this film would be. The scene where the main characters...',
    replies: 32,
    views: 215,
    category: 2
  },
  {
    id: 104,
    title: 'Best Action Sequences of 2023',
    author: 'ActionFan',
    date: '3 days ago',
    preview: 'Let\'s compile the most impressive action sequences from this year\'s releases...',
    replies: 45,
    views: 280,
    category: 1
  },
  {
    id: 105,
    title: 'Hidden Gems: Indie Comedy Collection',
    author: 'ComedyBuff',
    date: '4 days ago',
    preview: 'I\'ve discovered some amazing independent comedies lately and wanted to share...',
    replies: 27,
    views: 165,
    category: 5
  },
  {
    id: 106,
    title: 'Most Educational Nature Documentaries',
    author: 'NatureExplorer',
    date: '5 days ago',
    preview: 'Looking for recommendations on the most informative nature documentaries...',
    replies: 19,
    views: 142,
    category: 6
  }
];

// Computed property to filter topics by category
const categoryTopics = computed(() => {
  const categoryId = parseInt(route.params.id);
  return allTopics.filter(topic => topic.category === categoryId);
});

async function loadCategory() {
  loading.value = true;
  error.value = null;
  
  try {
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 500));
    
    const categoryId = route.params.id;
    const categoryData = categories[categoryId];
    
    if (!categoryData) {
      throw new Error('Category not found');
    }
    
    category.value = categoryData;
    
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