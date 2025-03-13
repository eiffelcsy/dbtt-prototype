<template>
  <div class="store min-h-screen bg-gray-900 text-white p-8">
    <div class="mb-8">
      <h1 class="text-3xl font-bold mb-6">DVD Store</h1>
      
      <!-- Filters -->
      <div class="filters flex flex-wrap gap-4 mb-6">
        <div class="filter-group">
          <label class="block text-gray-400 text-sm mb-2">Genre</label>
          <select v-model="selectedGenre" class="bg-gray-800 text-white rounded p-2 border border-gray-700 w-full md:w-48">
            <option value="">All Genres</option>
            <option v-for="genre in genres" :key="genre" :value="genre">{{ genre }}</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label class="block text-gray-400 text-sm mb-2">Sort By</label>
          <select v-model="sortBy" class="bg-gray-800 text-white rounded p-2 border border-gray-700 w-full md:w-48">
            <option value="title">Title</option>
            <option value="price">Price (Ascending)</option>
            <option value="releaseDate">Release Date</option>
          </select>
        </div>
        
        <div class="filter-group ml-auto">
          <label class="block text-gray-400 text-sm mb-2">Search</label>
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Search DVDs..." 
            class="bg-gray-800 text-white rounded p-2 border border-gray-700 w-full md:w-64"
          >
        </div>
      </div>
    </div>
    
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center h-64">
      <div class="loader">Loading...</div>
    </div>
    
    <!-- Error State -->
    <div v-else-if="error" class="text-center text-red-500 p-8">
      <p>{{ error }}</p>
      <button @click="loadProducts" class="mt-4 bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
        Try Again
      </button>
    </div>
    
    <!-- Product Grid -->
    <div v-else>
      <div v-if="filteredProducts.length === 0" class="text-center text-gray-400 p-16">
        <p>No DVDs found matching your criteria.</p>
      </div>
      
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
        <ProductCard 
          v-for="product in filteredProducts" 
          :key="product.id" 
          :product="product" 
          @add-to-cart="addToCart"
          @open-overlay="openProductOverlay" 
        />
      </div>
    </div>
    
    <!-- Added to Cart Notification -->
    <div 
      v-if="showCartNotification" 
      class="fixed bottom-4 right-4 bg-green-600 text-white p-4 rounded-lg shadow-lg z-50 animate-fade-in-up"
    >
      <div class="flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        <span>Added to cart!</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import ProductCard from '~/components/ProductCard.vue';
import { useProductStore } from '~/composables/useProductStore';

const products = ref([]);
const loading = ref(true);
const error = ref(null);
const searchQuery = ref('');
const selectedGenre = ref('');
const sortBy = ref('title');
const showCartNotification = ref(false);
const cart = ref([]);
const productStore = useProductStore();

const genres = computed(() => {
  const genreSet = new Set(products.value.map(product => product.genre));
  return [...genreSet];
});

const filteredProducts = computed(() => {
  let result = [...products.value];
  
  // Filter by genre
  if (selectedGenre.value) {
    result = result.filter(product => product.genre === selectedGenre.value);
  }
  
  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(product => 
      product.title.toLowerCase().includes(query) || 
      product.description.toLowerCase().includes(query)
    );
  }
  
  // Sort products
  result.sort((a, b) => {
    if (sortBy.value === 'title') {
      return a.title.localeCompare(b.title);
    } else if (sortBy.value === 'price') {
      return a.price - b.price;
    } else if (sortBy.value === 'releaseDate') {
      return new Date(b.releaseDate) - new Date(a.releaseDate);
    }
    return 0;
  });
  
  return result;
});

async function loadProducts() {
  loading.value = true;
  error.value = null;
  
  try {
    // In a real app, this would be a separate API endpoint for products
    const response = await fetch('/videos.json');
    if (!response.ok) {
      throw new Error('Failed to fetch products');
    }
    
    const data = await response.json();
    
    // Transform video data into product data with prices
    products.value = data.map(video => ({
      ...video,
      price: (Math.random() * 20 + 9.99).toFixed(2), // Random price between $9.99 and $29.99
      inStock: Math.random() > 0.2, // 80% chance of being in stock
      format: Math.random() > 0.5 ? 'DVD' : 'Blu-ray',
    }));
  } catch (err) {
    console.error('Error loading products:', err);
    error.value = 'There was a problem loading products. Please try again.';
  } finally {
    loading.value = false;
  }
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
  
  // Save cart to localStorage (in a real app, this might be in a store)
  localStorage.setItem('cart', JSON.stringify(cart.value));
  
  // Update cart count in header
  const headerComponent = document.querySelector('header').__vueParentComponent.exposed;
  if (headerComponent && headerComponent.updateCartCount) {
    headerComponent.updateCartCount(cart.value.reduce((total, item) => total + item.quantity, 0));
  }
  
  // Show notification
  showCartNotification.value = true;
  setTimeout(() => {
    showCartNotification.value = false;
  }, 3000);
}

function openProductOverlay(product) {
  productStore.openProductOverlay(product);
}

onMounted(() => {
  loadProducts();
  
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

.animate-fade-in-up {
  animation: fadeInUp 0.3s ease-out forwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style> 