<template>
  <div 
    class="video-card bg-gray-800 rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
    @mouseenter="isHovered = true" 
    @mouseleave="isHovered = false"
    @click="openProductDetails"
  >
    <div class="relative">
      <div 
        class="w-full h-40 bg-gradient-to-r from-gray-700 to-gray-600 flex items-center justify-center"
        v-if="!thumbnailExists"
      >
        <span class="text-gray-400">{{ video.title }}</span>
      </div>
      <img 
        v-else
        :src="video.thumbnail" 
        :alt="video.title" 
        class="w-full h-40 object-cover" 
      />
      <div 
        v-if="isHovered" 
        class="absolute inset-0 bg-black bg-opacity-70 flex items-center justify-center transition-opacity duration-300"
      >
        <div class="text-center">
          <button class="bg-red-600 hover:bg-red-700 text-white font-bold py-1 px-4 rounded-full mb-2">
            View Details
          </button>
        </div>
      </div>
      <div class="absolute bottom-0 right-0 bg-red-600 px-2 py-1 text-xs font-bold">
        {{ video.duration }}
      </div>
    </div>
    <div class="p-4">
      <div class="flex justify-between items-start mb-1">
        <h3 class="text-lg font-semibold text-white truncate">{{ video.title }}</h3>
        <span class="text-yellow-400 text-sm">★ {{ video.rating }}</span>
      </div>
      <p class="text-gray-400 text-sm mb-2 line-clamp-2">{{ video.description }}</p>
      <p class="text-gray-500 text-xs">{{ video.genre }} • {{ video.releaseDate }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useProductStore } from '~/composables/useProductStore';

const props = defineProps({
  video: {
    type: Object,
    required: true
  }
});

const isHovered = ref(false);
const productStore = useProductStore();

// In a real app, we'd verify if the image exists
// For this prototype, we'll assume images don't exist and use placeholders
const thumbnailExists = computed(() => {
  return false; // Force using placeholders since we don't have real images
});

// Function to open the product details overlay
function openProductDetails() {
  // Convert video to product format if needed
  const product = {
    ...props.video,
    id: props.video.productId || props.video.id,
    price: (Math.random() * 20 + 9.99).toFixed(2), // Random price between $9.99 and $29.99
    inStock: Math.random() > 0.2, // 80% chance of being in stock
    format: Math.random() > 0.5 ? 'DVD' : 'Blu-ray',
  };
  
  productStore.openProductOverlay(product);
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style> 