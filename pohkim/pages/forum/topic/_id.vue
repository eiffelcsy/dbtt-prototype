<template>
  <div class="forum-topic min-h-screen bg-gray-900 text-white p-8">
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
    
    <!-- Topic Content -->
    <div v-else>
      <!-- Breadcrumbs -->
      <div class="mb-6">
        <div class="flex items-center text-sm text-gray-400">
          <NuxtLink to="/forum" class="hover:text-white">Forum</NuxtLink>
          <span class="mx-2">›</span>
          <NuxtLink :to="`/forum/category/${topic.categoryId}`" class="hover:text-white">{{ getCategoryName(topic.categoryId) }}</NuxtLink>
          <span class="mx-2">›</span>
          <span class="text-white">{{ topic.title }}</span>
        </div>
      </div>
      
      <!-- Topic Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold mb-2">{{ topic.title }}</h1>
        <div class="flex items-center text-sm text-gray-400">
          <span>Started by {{ topic.author }}</span>
          <span class="mx-2">•</span>
          <span>{{ topic.date }}</span>
          <span class="mx-2">•</span>
          <span>{{ topic.replies }} replies</span>
          <span class="mx-2">•</span>
          <span>{{ topic.views }} views</span>
        </div>
      </div>
      
      <!-- Topic Actions -->
      <div class="flex justify-between items-center mb-6">
        <div class="flex space-x-2">
          <button class="bg-gray-800 hover:bg-gray-700 text-white px-4 py-2 rounded-md">
            <span class="hidden md:inline">Follow Topic</span>
            <span class="md:hidden">Follow</span>
          </button>
          <button class="bg-gray-800 hover:bg-gray-700 text-white px-4 py-2 rounded-md">
            <span class="hidden md:inline">Share Topic</span>
            <span class="md:hidden">Share</span>
          </button>
        </div>
        <button class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md">
          <span class="hidden md:inline">Reply to Topic</span>
          <span class="md:hidden">Reply</span>
        </button>
      </div>
      
      <!-- Original Post -->
      <div class="bg-gray-800 rounded-lg overflow-hidden mb-6">
        <div class="p-6">
          <div class="flex items-start">
            <!-- Author Info -->
            <div class="hidden md:block w-48 pr-6">
              <div class="flex flex-col items-center">
                <div class="w-20 h-20 rounded-full bg-gray-700 flex items-center justify-center mb-2">
                  <span class="text-2xl font-bold">{{ topic.author.substring(0, 1) }}</span>
                </div>
                <h3 class="font-semibold mb-1">{{ topic.author }}</h3>
                <p class="text-gray-400 text-sm">Member since 2022</p>
                <div class="mt-2 flex">
                  <span class="text-yellow-400">★★★★</span><span class="text-gray-600">★</span>
                </div>
                <p class="text-gray-400 text-xs mt-1">Posts: 142</p>
              </div>
            </div>
            
            <!-- Post Content -->
            <div class="flex-grow">
              <div class="md:hidden flex items-center mb-4">
                <div class="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center mr-3">
                  <span class="text-sm font-bold">{{ topic.author.substring(0, 1) }}</span>
                </div>
                <div>
                  <h3 class="font-semibold">{{ topic.author }}</h3>
                  <p class="text-gray-400 text-xs">{{ topic.date }}</p>
                </div>
              </div>
              
              <div class="post-content">
                <p class="mb-4">{{ topic.content }}</p>
                <p class="mb-4">I'd love to hear everyone's thoughts on this. What did you think about the character development? Did the ending make sense to you?</p>
              </div>
              
              <!-- Post Footer -->
              <div class="mt-6 pt-4 border-t border-gray-700 flex justify-between items-center">
                <div class="flex space-x-4">
                  <button class="text-gray-400 hover:text-white flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
                    </svg>
                    <span>Like (24)</span>
                  </button>
                  <button class="text-gray-400 hover:text-white flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                    </svg>
                    <span>Reply</span>
                  </button>
                </div>
                <div>
                  <button class="text-gray-400 hover:text-white">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h.01M12 12h.01M19 12h.01M6 12a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0z" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Replies -->
      <div class="mb-8">
        <h2 class="text-xl font-semibold mb-4">Replies ({{ replies.length }})</h2>
        
        <div v-for="(reply, index) in replies" :key="reply.id" class="bg-gray-800 rounded-lg overflow-hidden mb-4">
          <div class="p-6">
            <div class="flex items-start">
              <!-- Author Info -->
              <div class="hidden md:block w-48 pr-6">
                <div class="flex flex-col items-center">
                  <div class="w-16 h-16 rounded-full bg-gray-700 flex items-center justify-center mb-2">
                    <span class="text-xl font-bold">{{ reply.author.substring(0, 1) }}</span>
                  </div>
                  <h3 class="font-semibold mb-1">{{ reply.author }}</h3>
                  <p class="text-gray-400 text-sm">Member since {{ reply.memberSince }}</p>
                  <p class="text-gray-400 text-xs mt-1">Posts: {{ reply.postCount }}</p>
                </div>
              </div>
              
              <!-- Reply Content -->
              <div class="flex-grow">
                <div class="md:hidden flex items-center mb-4">
                  <div class="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center mr-3">
                    <span class="text-sm font-bold">{{ reply.author.substring(0, 1) }}</span>
                  </div>
                  <div>
                    <h3 class="font-semibold">{{ reply.author }}</h3>
                    <p class="text-gray-400 text-xs">{{ reply.date }}</p>
                  </div>
                </div>
                
                <div class="post-content">
                  <p class="mb-4">{{ reply.content }}</p>
                </div>
                
                <!-- Reply Footer -->
                <div class="mt-6 pt-4 border-t border-gray-700 flex justify-between items-center">
                  <div class="flex space-x-4">
                    <button class="text-gray-400 hover:text-white flex items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
                      </svg>
                      <span>Like ({{ reply.likes }})</span>
                    </button>
                    <button class="text-gray-400 hover:text-white flex items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                      </svg>
                      <span>Reply</span>
                    </button>
                  </div>
                  <div>
                    <button class="text-gray-400 hover:text-white">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h.01M12 12h.01M19 12h.01M6 12a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0z" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Reply Form -->
      <div class="bg-gray-800 rounded-lg overflow-hidden p-6">
        <h2 class="text-xl font-semibold mb-4">Post a Reply</h2>
        <div class="mb-4">
          <textarea 
            v-model="newReply" 
            rows="5" 
            class="w-full bg-gray-700 text-white rounded p-3 border border-gray-600"
            placeholder="Write your reply here..."
          ></textarea>
        </div>
        <div class="flex justify-end">
          <button 
            @click="submitReply" 
            class="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded-md transition-colors duration-200"
          >
            Post Reply
          </button>
        </div>
      </div>
    </div>
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

// Forum categories for reference
const categories = ref([
  { id: 1, name: 'Action & Adventure' },
  { id: 2, name: 'Drama & Romance' },
  { id: 3, name: 'Sci-Fi & Fantasy' },
  { id: 4, name: 'Horror & Thriller' },
  { id: 5, name: 'Comedy' },
  { id: 6, name: 'Documentary & Educational' }
]);

function getCategoryName(categoryId) {
  const category = categories.value.find(c => c.id === categoryId);
  return category ? category.name : 'Unknown Category';
}

async function loadTopic() {
  loading.value = true;
  error.value = null;
  
  try {
    // In a real app, this would be an API call
    // For this prototype, we'll simulate loading data
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // Find topic based on route param
    const topicId = parseInt(route.params.id);
    
    // Sample topic data
    if (topicId === 101) {
      topic.value = {
        id: 101,
        title: 'What did everyone think of the Cosmic Odyssey ending?',
        author: 'SpaceExplorer42',
        date: '2 hours ago',
        content: "I just finished watching Cosmic Odyssey and that twist at the end completely blew my mind! The way they revealed that the entire journey was actually happening in a parallel universe was so unexpected. The visual effects in the final scene where the dimensions merged were absolutely stunning. I've watched it three times now and keep noticing new details each time.",
        replies: 24,
        views: 142,
        categoryId: 3
      };
      
      replies.value = [
        {
          id: 1,
          author: 'GalacticDreamer',
          date: '1 hour ago',
          content: "I agree! That ending was incredible. I especially loved how they tied back to the subtle clues they planted in the first 30 minutes. The director really thought everything through. And that score during the final scene? Absolute perfection!",
          likes: 12,
          memberSince: '2021',
          postCount: 87
        },
        {
          id: 2,
          author: 'FilmCritic2023',
          date: '45 minutes ago',
          content: "I actually found it a bit predictable. If you've watched the director's previous work, you'll notice he uses the same twist formula. Don't get me wrong, the execution was great, but I saw it coming from a mile away.",
          likes: 5,
          memberSince: '2023',
          postCount: 134
        },
        {
          id: 3,
          author: 'StarGazer',
          date: '30 minutes ago',
          content: "The visuals were stunning, but I felt like the ending left too many unanswered questions. What happened to the secondary characters? And the whole subplot about the quantum device was completely abandoned. I'm hoping they address these in a sequel.",
          likes: 8,
          memberSince: '2020',
          postCount: 256
        }
      ];
    } else {
      // Default topic if ID doesn't match
      error.value = 'Topic not found';
    }
  } catch (err) {
    console.error('Error loading topic:', err);
    error.value = 'There was a problem loading this topic. Please try again.';
  } finally {
    loading.value = false;
  }
}

function submitReply() {
  if (!newReply.value.trim()) return;
  
  // In a real app, this would be an API call to save the reply
  // For this prototype, we'll just add it to the local array
  replies.value.push({
    id: replies.value.length + 1,
    author: 'CurrentUser',
    date: 'Just now',
    content: newReply.value,
    likes: 0,
    memberSince: '2023',
    postCount: 5
  });
  
  // Clear the reply input
  newReply.value = '';
  
  // Update the reply count
  topic.value.replies += 1;
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

.post-content {
  line-height: 1.6;
}
</style> 