<template>
  <teleport to="body">
    <transition name="modal">
      <div v-if="isOpen" class="modal-wrapper">
        <!-- Semi-transparent backdrop that dims the background -->
        <div class="modal-backdrop" @click="close"></div>
        
        <!-- Modal container -->
        <div class="modal-container">
          <!-- Fixed header with close button -->
          <div class="modal-header">
            <button class="modal-close-btn" @click="close">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          <!-- Scrollable content -->
          <div class="modal-scrollable-content">
            <!-- Video player section -->
            <div class="modal-video">
              <p class="text-center text-gray-400">
                This is a prototype. Trailer playback would be implemented here in the production version.
              </p>
            </div>
            
            <!-- Product details section -->
            <div class="modal-content">
              <div class="modal-content-inner">
                <!-- Left column - Title and description -->
                <div class="modal-info">
                  <h3 class="text-2xl font-bold text-white mb-2">{{ product.title }}</h3>
                  
                  <div class="flex flex-wrap items-center mb-4">
                    <div class="flex mr-2">
                      <span v-for="i in 5" :key="i" class="text-lg">
                        <span v-if="i <= Math.floor(product.rating)" class="text-yellow-400">★</span>
                        <span v-else-if="i - 0.5 <= product.rating" class="text-yellow-400">★</span>
                        <span v-else class="text-gray-600">★</span>
                      </span>
                    </div>
                    <span class="text-gray-400">{{ product.rating }}/5</span>
                    <span class="mx-2 text-gray-600">|</span>
                    <span class="text-gray-400">{{ formatDate(product.releaseDate) }}</span>
                    <span class="mx-2 text-gray-600">|</span>
                    <span class="bg-red-600 text-white text-xs px-2 py-1 rounded">{{ product.format }}</span>
                  </div>
                  
                  <p class="text-gray-300 mb-4">{{ product.description }}</p>
                  
                  <div class="text-gray-400">
                    <p><span class="font-semibold text-gray-300">Director:</span> {{ product.director }}</p>
                    <p><span class="font-semibold text-gray-300">Genre:</span> {{ product.genre }}</p>
                  </div>
                </div>
                
                <!-- Right column - Price and add to cart -->
                <div class="modal-purchase">
                  <div class="mb-4">
                    <div class="flex items-baseline">
                      <span class="text-2xl font-bold text-white">${{ product.price }}</span>
                      <span v-if="onSale" class="ml-2 text-sm line-through text-gray-500">${{ (parseFloat(product.price) * 1.2).toFixed(2) }}</span>
                      <span v-if="onSale" class="ml-2 bg-red-600 text-white text-xs px-2 py-1 rounded">SALE</span>
                    </div>
                    <p v-if="!product.inStock" class="text-red-500 text-sm mt-1">Out of Stock</p>
                    <p v-else class="text-green-500 text-sm mt-1">In Stock</p>
                  </div>
                  
                  <button 
                    @click="addToCart"
                    :disabled="!product.inStock"
                    :class="[
                      'w-full bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-4 rounded flex items-center justify-center',
                      !product.inStock ? 'opacity-50 cursor-not-allowed' : ''
                    ]"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                    Add to Cart
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  product: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['close', 'add-to-cart']);

// Random chance of the product being on sale
const onSale = computed(() => {
  return Math.random() > 0.7; // 30% chance of being on sale
});

// Lock body scroll when modal is open
function lockScroll() {
  const scrollY = window.scrollY;
  document.body.style.position = 'fixed';
  document.body.style.top = `-${scrollY}px`;
  document.body.style.width = '100%';
}

// Unlock body scroll when modal is closed
function unlockScroll() {
  const scrollY = document.body.style.top;
  document.body.style.position = '';
  document.body.style.top = '';
  document.body.style.width = '';
  window.scrollTo(0, parseInt(scrollY || '0') * -1);
}

watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    lockScroll();
  } else {
    unlockScroll();
  }
}, { immediate: true });

onMounted(() => {
  if (props.isOpen) {
    lockScroll();
  }
});

onUnmounted(() => {
  unlockScroll();
});

function close() {
  emit('close');
}

function addToCart() {
  if (props.product.inStock) {
    emit('add-to-cart', props.product);
    close();
  }
}

function formatDate(dateString) {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('en-US', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  }).format(date);
}
</script>

<style scoped>
/* Modal wrapper - covers the entire viewport */
.modal-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
}

/* Semi-transparent backdrop */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(2px);
}

/* Modal container */
.modal-container {
  position: relative;
  width: 100%;
  max-width: 900px;
  max-height: 85vh;
  margin: 0 20px;
  background-color: #1f2937;
  border-radius: 8px;
  overflow: hidden; /* Changed from scroll to hidden */
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  z-index: 101;
  display: flex;
  flex-direction: column;
}

/* Fixed header */
.modal-header {
  position: absolute;
  top: 0;
  right: 0;
  z-index: 102;
  padding: 16px;
}

/* Close button */
.modal-close-btn {
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 50%;
  padding: 8px;
  transition: background-color 0.2s;
}

.modal-close-btn:hover {
  background-color: rgba(0, 0, 0, 0.7);
}

/* Scrollable content area */
.modal-scrollable-content {
  overflow-y: auto;
  max-height: 85vh;
}

/* Video section */
.modal-video {
  width: 100%;
  aspect-ratio: 16/9;
  background-color: black;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Content area */
.modal-content {
  overflow-y: auto;
}

.modal-content-inner {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

@media (min-width: 768px) {
  .modal-content-inner {
    flex-direction: row;
  }
}

/* Info column */
.modal-info {
  flex: 2;
}

/* Purchase column */
.modal-purchase {
  flex: 1;
  background-color: #111827;
  padding: 16px;
  border-radius: 8px;
}

/* Transition animations */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

.modal-enter-to,
.modal-leave-from {
  opacity: 1;
  transform: scale(1);
}
</style> 