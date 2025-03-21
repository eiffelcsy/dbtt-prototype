<template>
  <div 
    class="product-card bg-gray-800 rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition-all duration-300 flex flex-col"
    :class="{'featured-product': isFeaturedProduct}"
    @mouseenter="isHovered = true" 
    @mouseleave="isHovered = false"
    @click="openOverlay"
  >
    <div class="relative">
      <div 
        class="w-full h-40 bg-gradient-to-r from-gray-700 to-gray-600 flex items-center justify-center"
        :class="{'h-56': isFeaturedProduct}"
        v-if="!thumbnailExists"
      >
        <span class="text-gray-400" :class="{'text-xl': isFeaturedProduct}">{{ product.title }}</span>
      </div>
      <img 
        v-else
        :src="product.thumbnail" 
        :alt="product.title" 
        class="w-full h-40 object-cover"
        :class="{'h-56': isFeaturedProduct}"
        loading="lazy" 
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
      <div v-if="isFeaturedProduct" class="absolute top-0 left-0 bg-yellow-500 px-2 py-1 text-xs font-bold text-black">
        FEATURED
      </div>
    </div>
    
    <div class="p-4 flex flex-col flex-grow" :class="{'p-5': isFeaturedProduct}">
      <div class="flex-grow mb-4">
        <div class="flex justify-between items-start mb-1">
          <h3 class="text-lg font-semibold text-white" :class="{'text-xl': isFeaturedProduct, 'truncate': !isFeaturedProduct}">{{ product.title }}</h3>
          <span class="text-yellow-400 text-sm" :class="{'text-base': isFeaturedProduct}">★ {{ product.rating }}</span>
        </div>
        <p class="text-gray-400 text-sm mb-2" :class="{'line-clamp-2': !isFeaturedProduct, 'line-clamp-5': isFeaturedProduct, 'mt-2': isFeaturedProduct}">{{ product.description }}</p>
        
        <!-- Additional info for featured product -->
        <div v-if="isFeaturedProduct && product.additionalInfo" class="mt-3 border-t border-gray-700 pt-3">
          <h4 class="text-sm font-semibold text-white mb-2">Product Information</h4>
          <ul class="text-gray-400 text-xs space-y-1">
            <li><span class="text-gray-500">Audio:</span> {{ product.additionalInfo.audio }}</li>
            <li><span class="text-gray-500">Subtitle:</span> {{ product.additionalInfo.subtitle }}</li>
            <li><span class="text-gray-500">Episodes:</span> {{ product.additionalInfo.episodes }}</li>
            <li><span class="text-gray-500">Discs:</span> {{ product.additionalInfo.discs }}</li>
          </ul>
        </div>
      </div>
      
      <!-- This div is always at the bottom of the card -->
      <div class="flex justify-between items-center mt-auto">
        <div>
          <span class="text-white font-bold" :class="{'text-xl text-yellow-400': isFeaturedProduct}">${{ product.price }}</span>
          <span v-if="!product.inStock" class="ml-2 text-red-500 text-xs">Out of Stock</span>
        </div>
        <button 
          @click.stop="addToCart"
          :disabled="!product.inStock"
          :class="[
            'bg-red-600 hover:bg-red-700 text-white font-bold py-1 px-3 rounded-full text-sm',
            !product.inStock ? 'opacity-50 cursor-not-allowed' : '',
            isFeaturedProduct ? 'py-2 px-4' : ''
          ]"
        >
          Add to Cart
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['add-to-cart', 'open-overlay']);

const isHovered = ref(false);
const isVisible = ref(false);

// Check if this is our featured product (Condor Heroes)
const isFeaturedProduct = computed(() => {
  return props.product.id === 67;
});

// In a real app, we'd verify if the image exists
// For this prototype, we'll assume images don't exist and use placeholders
const thumbnailExists = computed(() => {
  // Check if thumbnail path is defined and not empty
  return props.product.thumbnail && props.product.thumbnail.length > 0;
});

function addToCart() {
  if (props.product.inStock) {
    emit('add-to-cart', props.product);
  }
}

function openOverlay() {
  emit('open-overlay', props.product);
}

onMounted(() => {
  // Set up intersection observer for lazy loading
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting) {
        isVisible.value = true;
        observer.disconnect();
      }
    }, { threshold: 0.1 });
    
    observer.observe(document.querySelector('.product-card'));
  } else {
    // Fallback for browsers without intersection observer
    isVisible.value = true;
  }
});
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-4 {
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2), 0 4px 6px -2px rgba(0, 0, 0, 0.1);
}

.featured-product {
  grid-column: span 2;
  grid-row: span 2;
  border: 2px solid #F59E0B;
  box-shadow: 0 0 15px rgba(245, 158, 11, 0.2);
}

@media (max-width: 640px) {
  .featured-product {
    grid-column: span 1;
    grid-row: span 1;
  }
}
</style> 