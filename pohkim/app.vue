<template>
  <div class="app">
    <Header />
    <NuxtPage />
    <Footer />
    <ProductOverlay 
      v-if="selectedProduct" 
      :is-open="!!selectedProduct" 
      :product="selectedProduct" 
      @close="closeProductOverlay" 
      @add-to-cart="addToCart" 
    />
  </div>
</template>

<script setup>
import Header from '~/components/Header.vue';
import Footer from '~/components/Footer.vue';
import ProductOverlay from '~/components/ProductOverlay.vue';
import { useProductStore } from '~/composables/useProductStore';
import { ref, computed, onMounted } from 'vue';

const productStore = useProductStore();
const selectedProduct = computed(() => productStore.selectedProduct.value);

// Cart functionality
const cart = ref([]);

function closeProductOverlay() {
  productStore.closeProductOverlay();
}

function addToCart(product) {
  // Check if product is already in cart
  const existingItem = cart.value.find(item => item.id === product.id);
  
  if (existingItem) {
    existingItem.quantity += 1;
  } else {
    cart.value.push({
      ...product,
      quantity: 1
    });
  }
  
  // Save cart to localStorage
  localStorage.setItem('cart', JSON.stringify(cart.value));
  
  // Update cart count in header
  const headerComponent = document.querySelector('header').__vueParentComponent.exposed;
  if (headerComponent && headerComponent.updateCartCount) {
    headerComponent.updateCartCount(cart.value.reduce((total, item) => total + item.quantity, 0));
  }
  
  // Show notification (you might want to implement this)
  console.log('Added to cart:', product.title);
}

onMounted(() => {
  // Load cart from localStorage
  const savedCart = localStorage.getItem('cart');
  if (savedCart) {
    cart.value = JSON.parse(savedCart);
    
    // Update cart count in header
    const headerComponent = document.querySelector('header').__vueParentComponent.exposed;
    if (headerComponent && headerComponent.updateCartCount) {
      headerComponent.updateCartCount(cart.value.reduce((total, item) => total + item.quantity, 0));
    }
  }
});
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body {
  font-family: 'Inter', sans-serif;
  background-color: #111827; /* bg-gray-900 */
  color: white;
  scroll-behavior: smooth;
}

/* Global transitions */
.page-enter-active,
.page-leave-active {
  transition: opacity 0.3s;
}
.page-enter-from,
.page-leave-to {
  opacity: 0;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 10px;
}

::-webkit-scrollbar-track {
  background: #1f2937; /* bg-gray-800 */
}

::-webkit-scrollbar-thumb {
  background: #4b5563; /* bg-gray-600 */
  border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
  background: #6b7280; /* bg-gray-500 */
}

/* Focus styles for accessibility */
*:focus-visible {
  outline: 2px solid #ef4444; /* red-600 */
  outline-offset: 2px;
}

/* Button hover effects */
.btn-hover-effect {
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-hover-effect:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

/* Card hover effects */
.card-hover {
  transition: transform 0.3s, box-shadow 0.3s;
}

.card-hover:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}
</style>
