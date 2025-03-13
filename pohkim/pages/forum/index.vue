<template>
  <div class="forum min-h-screen bg-gray-900 text-white p-8">
    <div class="mb-8">
      <h1 class="text-3xl font-bold mb-2">Pohkim Community</h1>
      <p class="text-gray-400">Join discussions about your favorite films with fellow enthusiasts.</p>
    </div>
    
    <!-- Community Stats -->
    <div class="bg-gray-800 rounded-lg p-6 mb-8">
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
    <div class="mb-12">
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
    <div>
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-semibold">Recent Discussions</h2>
        <NuxtLink to="/forum/new-topic" class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md transition-colors duration-200">
          <span class="hidden md:inline">Start New Topic</span>
          <span class="md:hidden">New</span>
        </NuxtLink>
      </div>
      
      <div class="bg-gray-800 rounded-lg overflow-hidden">
        <div v-for="(topic, index) in recentTopics" :key="topic.id" 
             :class="['p-6 flex flex-col md:flex-row md:items-center', index < recentTopics.length - 1 ? 'border-b border-gray-700' : '']">
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
        <button class="bg-gray-800 hover:bg-gray-700 text-white px-6 py-2 rounded-md transition-colors duration-200">
          Load More Discussions
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// Forum statistics
const forumStats = ref({
  topics: 1248,
  posts: 5729,
  members: 3421,
  online: 42
});

// Forum categories
const categories = ref([
  {
    id: 1,
    name: 'Action & Adventure',
    description: 'Discuss high-octane action films and adventure epics',
    icon: '🔥',
    topics: 324,
    posts: 1892
  },
  {
    id: 2,
    name: 'Drama & Romance',
    description: 'Share your thoughts on dramatic and romantic stories',
    icon: '💔',
    topics: 287,
    posts: 1456
  },
  {
    id: 3,
    name: 'Sci-Fi & Fantasy',
    description: 'Explore worlds beyond our own and magical realms',
    icon: '🚀',
    topics: 412,
    posts: 2103
  },
  {
    id: 4,
    name: 'Horror & Thriller',
    description: 'For fans of spine-tingling and suspenseful content',
    icon: '👻',
    topics: 198,
    posts: 876
  },
  {
    id: 5,
    name: 'Comedy',
    description: 'Laugh and discuss your favorite comedies',
    icon: '😂',
    topics: 231,
    posts: 1204
  },
  {
    id: 6,
    name: 'Documentary & Educational',
    description: 'Learn and discuss informative content',
    icon: '🧠',
    topics: 156,
    posts: 723
  }
]);

// Recent topics
const recentTopics = ref([
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
    title: 'Laugh Factory - Funniest moments compilation',
    author: 'ComedyLover',
    date: '2 days ago',
    preview: 'Let\'s compile a list of the absolute funniest moments from the show. My favorite has to be when...',
    replies: 27,
    views: 183,
    category: 5
  },
  {
    id: 105,
    title: 'Ocean Depths documentary - Fascinating facts I learned',
    author: 'OceanExplorer',
    date: '3 days ago',
    preview: 'This documentary was incredibly informative. I wanted to share some of the most interesting facts I learned...',
    replies: 15,
    views: 124,
    category: 6
  }
]);
</script>

<style scoped>
/* Additional styling can be added here if needed */
</style> 