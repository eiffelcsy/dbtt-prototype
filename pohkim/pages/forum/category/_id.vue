<template>
  <div class="forum-category min-h-screen bg-gray-900 text-white p-8">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center h-64">
      <div class="loader">Loading...</div>
    </div>
    
    <!-- Error State -->
    <div v-else-if="error" class="text-center text-red-500 p-8">
      <p>{{ error }}</p>
      <NuxtLink to="/forum" class="mt-4 bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded inline-block">
        Return to Forum
      </NuxtLink>
    </div>
    
    <!-- Category Content -->
    <div v-else>
      <!-- Breadcrumbs -->
      <div class="mb-6">
        <div class="flex items-center text-sm text-gray-400">
          <NuxtLink to="/forum" class="hover:text-white">Forum</NuxtLink>
          <span class="mx-2">›</span>
          <span class="text-white">{{ category.name }}</span>
        </div>
      </div>
      
      <!-- Category Header -->
      <div class="mb-8">
        <div class="flex items-center mb-4">
          <div class="w-12 h-12 rounded-full bg-red-600 flex items-center justify-center mr-4">
            <span class="text-xl font-bold">{{ category.icon }}</span>
          </div>
          <div>
            <h1 class="text-3xl font-bold">{{ category.name }}</h1>
            <p class="text-gray-400">{{ category.description }}</p>
          </div>
        </div>
        
        <div class="flex flex-wrap gap-4 text-sm">
          <div class="bg-gray-800 px-4 py-2 rounded-md">
            <span class="text-gray-400">Topics:</span>
            <span class="ml-1 font-semibold">{{ category.topicCount }}</span>
          </div>
          <div class="bg-gray-800 px-4 py-2 rounded-md">
            <span class="text-gray-400">Posts:</span>
            <span class="ml-1 font-semibold">{{ category.postCount }}</span>
          </div>
          <div class="bg-gray-800 px-4 py-2 rounded-md">
            <span class="text-gray-400">Last Post:</span>
            <span class="ml-1 font-semibold">{{ category.lastPost }}</span>
          </div>
        </div>
      </div>
      
      <!-- Category Actions -->
      <div class="flex justify-between items-center mb-6">
        <div class="flex space-x-2">
          <div class="relative">
            <button @click="showSortOptions = !showSortOptions" class="bg-gray-800 hover:bg-gray-700 text-white px-4 py-2 rounded-md flex items-center">
              <span>Sort by: {{ sortBy }}</span>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            <div v-if="showSortOptions" class="absolute top-full left-0 mt-1 bg-gray-800 rounded-md shadow-lg z-10 w-48">
              <div class="py-1">
                <button @click="setSortBy('newest')" class="block w-full text-left px-4 py-2 hover:bg-gray-700">Newest</button>
                <button @click="setSortBy('oldest')" class="block w-full text-left px-4 py-2 hover:bg-gray-700">Oldest</button>
                <button @click="setSortBy('most_replies')" class="block w-full text-left px-4 py-2 hover:bg-gray-700">Most Replies</button>
                <button @click="setSortBy('most_views')" class="block w-full text-left px-4 py-2 hover:bg-gray-700">Most Views</button>
              </div>
            </div>
          </div>
          <div class="relative">
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="Search topics..." 
              class="bg-gray-800 text-white px-4 py-2 rounded-md border border-gray-700 focus:outline-none focus:border-red-500"
            />
          </div>
        </div>
        <button class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md">
          <span class="hidden md:inline">New Topic</span>
          <span class="md:hidden">+ Topic</span>
        </button>
      </div>
      
      <!-- Topics List -->
      <div class="mb-8">
        <div v-if="filteredTopics.length === 0" class="text-center py-12 bg-gray-800 rounded-lg">
          <p class="text-gray-400">No topics found in this category.</p>
          <button class="mt-4 bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md">
            Start a New Discussion
          </button>
        </div>
        
        <div v-else class="bg-gray-800 rounded-lg overflow-hidden">
          <!-- Topics Table Header -->
          <div class="hidden md:flex bg-gray-700 text-gray-300 text-sm font-semibold">
            <div class="py-3 px-6 w-8/12">Topic</div>
            <div class="py-3 px-4 w-1/12 text-center">Replies</div>
            <div class="py-3 px-4 w-1/12 text-center">Views</div>
            <div class="py-3 px-6 w-2/12">Last Post</div>
          </div>
          
          <!-- Topics List -->
          <div>
            <div 
              v-for="topic in filteredTopics" 
              :key="topic.id" 
              class="border-t border-gray-700 hover:bg-gray-750 transition-colors duration-150"
            >
              <div class="flex flex-col md:flex-row">
                <!-- Topic Info (Mobile & Desktop) -->
                <div class="py-4 px-6 md:w-8/12">
                  <div class="flex items-start">
                    <!-- Topic Icon -->
                    <div class="hidden md:block w-10 h-10 rounded-full bg-gray-700 flex-shrink-0 mr-3 overflow-hidden">
                      <div class="w-full h-full flex items-center justify-center">
                        <span class="text-lg font-bold">{{ topic.author.substring(0, 1) }}</span>
                      </div>
                    </div>
                    
                    <!-- Topic Details -->
                    <div class="flex-grow">
                      <NuxtLink :to="`/forum/topic/${topic.id}`" class="text-lg font-semibold hover:text-red-500 transition-colors duration-150">
                        {{ topic.title }}
                      </NuxtLink>
                      
                      <div class="mt-1 text-sm text-gray-400">
                        Started by <span class="text-gray-300">{{ topic.author }}</span> • {{ topic.date }}
                      </div>
                      
                      <!-- Mobile Only Stats -->
                      <div class="md:hidden mt-2 flex text-xs text-gray-400">
                        <div class="mr-4">
                          <span class="font-semibold">{{ topic.replies }}</span> replies
                        </div>
                        <div>
                          <span class="font-semibold">{{ topic.views }}</span> views
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- Stats (Desktop Only) -->
                <div class="hidden md:flex md:w-4/12">
                  <div class="py-4 px-4 w-3/12 text-center flex items-center justify-center">
                    <span class="font-semibold">{{ topic.replies }}</span>
                  </div>
                  <div class="py-4 px-4 w-3/12 text-center flex items-center justify-center">
                    <span class="font-semibold">{{ topic.views }}</span>
                  </div>
                  <div class="py-4 px-6 w-6/12 text-sm">
                    <div>{{ topic.lastReplyDate }}</div>
                    <div class="text-gray-400">by {{ topic.lastReplyAuthor }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Pagination -->
      <div class="flex justify-center">
        <div class="inline-flex rounded-md shadow">
          <button class="py-2 px-4 bg-gray-800 text-gray-400 rounded-l-md hover:bg-gray-700 disabled:opacity-50" :disabled="currentPage === 1">
            Previous
          </button>
          <button 
            v-for="page in totalPages" 
            :key="page" 
            class="py-2 px-4 bg-gray-800 hover:bg-gray-700"
            :class="{ 'bg-red-600 hover:bg-red-700': currentPage === page }"
          >
            {{ page }}
          </button>
          <button class="py-2 px-4 bg-gray-800 text-gray-400 rounded-r-md hover:bg-gray-700 disabled:opacity-50" :disabled="currentPage === totalPages">
            Next
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const loading = ref(true);
const error = ref(null);
const category = ref(null);
const topics = ref([]);
const searchQuery = ref('');
const showSortOptions = ref(false);
const sortBy = ref('newest');
const currentPage = ref(1);
const totalPages = ref(1);

// Categories data (in a real app, this would come from an API)
const categories = [
  { 
    id: 1, 
    name: 'Action & Adventure', 
    icon: '🎬',
    description: 'Discuss high-octane action films and thrilling adventure movies.',
    topicCount: 124,
    postCount: 1842,
    lastPost: '2 hours ago'
  },
  { 
    id: 2, 
    name: 'Drama & Romance', 
    icon: '💔',
    description: 'Share your thoughts on emotional dramas and heartwarming romance films.',
    topicCount: 98,
    postCount: 1253,
    lastPost: '4 hours ago'
  },
  { 
    id: 3, 
    name: 'Sci-Fi & Fantasy', 
    icon: '🚀',
    description: 'Explore futuristic worlds and magical realms in sci-fi and fantasy discussions.',
    topicCount: 156,
    postCount: 2341,
    lastPost: '1 hour ago'
  },
  { 
    id: 4, 
    name: 'Horror & Thriller', 
    icon: '👻',
    description: 'For fans of spine-chilling horror and suspenseful thrillers.',
    topicCount: 87,
    postCount: 1120,
    lastPost: '5 hours ago'
  },
  { 
    id: 5, 
    name: 'Comedy', 
    icon: '😂',
    description: 'Laugh and discuss your favorite comedy films and shows.',
    topicCount: 112,
    postCount: 1756,
    lastPost: '3 hours ago'
  },
  { 
    id: 6, 
    name: 'Documentary & Educational', 
    icon: '📚',
    description: 'Learn and discuss informative documentaries and educational content.',
    topicCount: 65,
    postCount: 892,
    lastPost: '8 hours ago'
  }
];

// Sample topics data
const sampleTopics = [
  {
    id: 101,
    categoryId: 3,
    title: 'What did everyone think of the Cosmic Odyssey ending?',
    author: 'SpaceExplorer42',
    date: '2 hours ago',
    replies: 24,
    views: 142,
    lastReplyDate: '15 minutes ago',
    lastReplyAuthor: 'GalacticDreamer'
  },
  {
    id: 102,
    categoryId: 3,
    title: 'Top 5 sci-fi movies of the last decade - what are yours?',
    author: 'FilmBuff2023',
    date: '1 day ago',
    replies: 37,
    views: 215,
    lastReplyDate: '1 hour ago',
    lastReplyAuthor: 'MovieCritic'
  },
  {
    id: 103,
    categoryId: 3,
    title: 'The physics in "Quantum Leap" - how accurate is it?',
    author: 'ScienceNerd',
    date: '3 days ago',
    replies: 18,
    views: 98,
    lastReplyDate: '6 hours ago',
    lastReplyAuthor: 'PhysicsProf'
  },
  {
    id: 104,
    categoryId: 3,
    title: 'Fantasy series with the best world-building?',
    author: 'BookWorm',
    date: '5 days ago',
    replies: 42,
    views: 187,
    lastReplyDate: '2 hours ago',
    lastReplyAuthor: 'FantasyFan'
  },
  {
    id: 105,
    categoryId: 3,
    title: "Upcoming sci-fi releases I'm excited about",
    author: 'FutureFan',
    date: '1 week ago',
    replies: 15,
    views: 124,
    lastReplyDate: '1 day ago',
    lastReplyAuthor: 'MovieBuff'
  }
];

// Computed property for filtered topics
const filteredTopics = computed(() => {
  let result = [...topics.value];
  
  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(topic => 
      topic.title.toLowerCase().includes(query) || 
      topic.author.toLowerCase().includes(query)
    );
  }
  
  // Apply sorting
  switch (sortBy.value) {
    case 'newest':
      // For this prototype, we'll assume the order is already newest first
      break;
    case 'oldest':
      result = [...result].reverse();
      break;
    case 'most_replies':
      result = [...result].sort((a, b) => b.replies - a.replies);
      break;
    case 'most_views':
      result = [...result].sort((a, b) => b.views - a.views);
      break;
  }
  
  return result;
});

function setSortBy(value) {
  sortBy.value = value;
  showSortOptions.value = false;
}

async function loadCategory() {
  loading.value = true;
  error.value = null;
  
  try {
    // In a real app, this would be an API call
    // For this prototype, we'll simulate loading data
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // Find category based on route param
    const categoryId = parseInt(route.params.id);
    const foundCategory = categories.find(c => c.id === categoryId);
    
    if (foundCategory) {
      category.value = foundCategory;
      
      // Filter topics for this category
      topics.value = sampleTopics.filter(t => t.categoryId === categoryId);
      
      // Set pagination
      totalPages.value = Math.ceil(topics.value.length / 10) || 1;
    } else {
      error.value = 'Category not found';
    }
  } catch (err) {
    console.error('Error loading category:', err);
    error.value = 'There was a problem loading this category. Please try again.';
  } finally {
    loading.value = false;
  }
}

// Close sort options dropdown when clicking outside
function handleClickOutside(event) {
  if (showSortOptions.value) {
    showSortOptions.value = false;
  }
}

onMounted(() => {
  loadCategory();
  document.addEventListener('click', handleClickOutside);
});

// Clean up event listener
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});

// Reset to page 1 when search query changes
watch(searchQuery, () => {
  currentPage.value = 1;
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

/* Custom hover color for table rows */
.bg-gray-750 {
  background-color: #2d3748;
}
</style> 