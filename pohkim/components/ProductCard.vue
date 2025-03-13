<template>
  <div 
    class="product-card bg-gray-800 rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition-all duration-300"
    @mouseenter="isHovered = true" 
    @mouseleave="isHovered = false"
    @click="openOverlay"
  >
    <div class="relative">
      <div 
        class="w-full h-40 bg-gradient-to-r from-gray-700 to-gray-600 flex items-center justify-center"
        v-if="!thumbnailExists"
      >
        <span class="text-gray-400">{{ product.title }}</span>
      </div>
      <img 
        v-else
        :src="product.thumbnail" 
        :alt="product.title" 
        class="w-full h-40 object-cover" 
      />
      <div 
        v-if="isHovered" 
        class="absolute inset-0 bg-black bg-opacity-70 flex items-center justify-center transition-opacity duration-300"
      >
        <div class="text-center space-y-2">
          <button class="inline-block bg-red-600 hover:bg-red-700 text-white font-bold py-1 px-4 rounded-full">
            View Details
          </button>
        </div>
      </div>
      <div class="absolute top-0 right-0 bg-red-600 px-2 py-1 text-xs font-bold">
        {{ product.format }}
      </div>
    </div>
    <div class="p-4">
      <div class="flex justify-between items-start mb-1">
        <h3 class="text-lg font-semibold text-white truncate">{{ product.title }}</h3>
        <span class="text-yellow-400 text-sm">★ {{ product.rating }}</span>
      </div>
      <p class="text-gray-400 text-sm mb-2 line-clamp-2">{{ product.description }}</p>
      <div class="flex justify-between items-center mt-4">
        <div>
          <span class="text-white font-bold">${{ product.price }}</span>
          <span v-if="!product.inStock" class="ml-2 text-red-500 text-xs">Out of Stock</span>
        </div>
        <button 
          @click.stop="addToCart"
          :disabled="!product.inStock"
          :class="[
            'bg-red-600 hover:bg-red-700 text-white font-bold py-1 px-3 rounded-full text-sm',
            !product.inStock ? 'opacity-50 cursor-not-allowed' : ''
          ]"
        >
          Add to Cart
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['add-to-cart', 'open-overlay']);

const isHovered = ref(false);

// In a real app, we'd verify if the image exists
// For this prototype, we'll assume images don't exist and use placeholders
const thumbnailExists = computed(() => {
  return false; // Force using placeholders since we don't have real images
});

function addToCart() {
  if (props.product.inStock) {
    emit('add-to-cart', props.product);
  }
}

function openOverlay() {
  emit('open-overlay', props.product);
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