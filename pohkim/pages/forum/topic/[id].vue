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

    <template v-else>
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
        <div class="space-y-4">
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

// Mock data for categories (in a real app, this would come from a store or API)
const categories = {
  1: 'Action & Adventure',
  2: 'Drama & Romance',
  3: 'Sci-Fi & Fantasy',
  4: 'Horror & Thriller',
  5: 'Comedy',
  6: 'Documentary & Educational'
};

// Mock topics data (in a real app, this would come from an API)
const mockTopics = {
  '101': {
    id: 101,
    title: 'What did everyone think of the Cosmic Odyssey ending?',
    author: 'SpaceExplorer42',
    date: '2 hours ago',
    content: 'I just finished watching Cosmic Odyssey and that twist at the end completely blew my mind! The way they revealed that the entire journey was actually happening in a parallel universe was so unexpected. The visual effects in the final scene where the dimensions merged were absolutely stunning. What did everyone else think about the ending? Did you see the twist coming?',
    replies: 24,
    views: 142,
    category: 3
  },
  '102': {
    id: 102,
    title: 'The Last Detective - Plot holes discussion [SPOILERS]',
    author: 'MysteryFan',
    date: '5 hours ago',
    content: 'I noticed several inconsistencies in the storyline of The Last Detective, especially in the final act. The biggest plot hole seems to be how the detective knew about the warehouse location without any prior clues leading there. Also, the missing evidence from the third episode was never explained. Has anyone else noticed these issues?',
    replies: 18,
    views: 97,
    category: 4
  },
  '103': {
    id: 103,
    title: 'Whispers of the Heart made me cry - emotional impact thread',
    author: 'FilmBuff2023',
    date: '1 day ago',
    content: 'I just finished watching Whispers of the Heart and I\'m still emotional. The way they portrayed the relationship between the main characters was so genuine and heartfelt. The scene where they finally reunite after years apart brought me to tears. The musical score during that moment was perfect. Would love to hear about moments that touched you the most.',
    replies: 32,
    views: 215,
    category: 2
  }
};

// Mock replies data
const mockReplies = {
  '101': [
    {
      id: 1,
      author: 'CinematicDreamer',
      date: '1 hour ago',
      content: 'The ending was incredible! I had to watch it twice to catch all the subtle hints they planted throughout the movie. The parallel universe theory actually explains so many of the "inconsistencies" we noticed earlier in the film.'
    },
    {
      id: 2,
      author: 'SciFiLover',
      date: '45 minutes ago',
      content: 'I actually predicted something similar around the halfway point, but the execution still blew me away. The visual effects team deserves an award for that final sequence!'
    }
  ],
  '102': [
    {
      id: 1,
      author: 'DetectiveNoir',
      date: '3 hours ago',
      content: 'The warehouse plot hole bothered me too! I think they might have cut a scene that explained it, because there was a brief mention of an informant in episode 5 that never went anywhere.'
    }
  ],
  '103': [
    {
      id: 1,
      author: 'MovieBuff',
      date: '12 hours ago',
      content: 'The reunion scene was perfectly executed. The way they used silence and then gradually brought in the music was masterful. I also loved how they showed the characters had grown but still retained their core personalities.'
    },
    {
      id: 2,
      author: 'EmotionalViewer',
      date: '6 hours ago',
      content: 'I couldn\'t stop crying during the letter reading scene. The voice acting was so genuine and heartfelt. This movie really knows how to portray deep emotions without being melodramatic.'
    }
  ]
};

function getCategoryName(categoryId) {
  return categories[categoryId] || 'Unknown Category';
}

async function loadTopic() {
  loading.value = true;
  error.value = null;
  
  try {
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 500));
    
    const topicId = route.params.id;
    const mockTopic = mockTopics[topicId];
    
    if (!mockTopic) {
      throw new Error('Topic not found');
    }
    
    topic.value = mockTopic;
    replies.value = mockReplies[topicId] || [];
    
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