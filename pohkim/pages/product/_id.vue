<template>
  <div class="product-detail min-h-screen bg-gray-900 text-white">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center h-64">
      <div class="loader">Loading...</div>
    </div>
    
    <!-- Error State -->
    <div v-else-if="error" class="text-center text-red-500 p-8">
      <p>{{ error }}</p>
      <NuxtLink to="/store" class="mt-4 bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded inline-block">
        Return to Store
      </NuxtLink>
    </div>
    
    <!-- Product Content -->
    <div v-else class="container mx-auto px-4 py-8">
      <!-- Breadcrumbs -->
      <div class="mb-6">
        <div class="flex items-center text-sm text-gray-400">
          <NuxtLink to="/" class="hover:text-white">Home</NuxtLink>
          <span class="mx-2">›</span>
          <NuxtLink to="/store" class="hover:text-white">DVD Store</NuxtLink>
          <span class="mx-2">›</span>
          <span class="text-white">{{ product.title }}</span>
        </div>
      </div>
      
      <!-- Product Main Section -->
      <div class="flex flex-col md:flex-row gap-8 mb-12">
        <!-- Product Image -->
        <div class="md:w-2/5">
          <div class="bg-gray-800 rounded-lg overflow-hidden aspect-[3/4] relative">
            <!-- Placeholder image with gradient background -->
            <div class="absolute inset-0 bg-gradient-to-br from-gray-700 to-gray-900 flex items-center justify-center">
              <span class="text-4xl font-bold text-white opacity-30">{{ product.title.substring(0, 1) }}</span>
            </div>
            
            <!-- Format Badge -->
            <div class="absolute top-4 right-4 bg-red-600 text-white text-xs font-bold px-2 py-1 rounded">
              {{ product.format }}
            </div>
            
            <!-- Rating Stars -->
            <div class="absolute bottom-4 left-4 flex items-center bg-black bg-opacity-50 rounded px-2 py-1">
              <div class="flex">
                <span v-for="i in 5" :key="i" class="text-lg">
                  <span v-if="i <= Math.floor(product.rating)" class="text-yellow-400">★</span>
                  <span v-else-if="i - 0.5 <= product.rating" class="text-yellow-400">★</span>
                  <span v-else class="text-gray-600">★</span>
                </span>
              </div>
              <span class="ml-1 text-sm">{{ product.rating }}/5</span>
            </div>
          </div>
          
          <!-- Watch Trailer Button -->
          <NuxtLink :to="`/video/${product.videoId}`" class="mt-4 w-full bg-gray-800 hover:bg-gray-700 text-white font-bold py-3 px-4 rounded flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Watch Trailer
          </NuxtLink>
        </div>
        
        <!-- Product Info -->
        <div class="md:w-3/5">
          <h1 class="text-3xl font-bold mb-2">{{ product.title }}</h1>
          
          <!-- Director & Release Date -->
          <div class="mb-4 text-gray-400">
            <p>Directed by <span class="text-white">{{ product.director }}</span></p>
            <p>Released: {{ formatDate(product.releaseDate) }}</p>
          </div>
          
          <!-- Price & Stock -->
          <div class="mb-6">
            <div class="flex items-baseline">
              <span class="text-2xl font-bold text-white">${{ productPrice.toFixed(2) }}</span>
              <span v-if="onSale" class="ml-2 text-sm line-through text-gray-500">${{ (productPrice * 1.2).toFixed(2) }}</span>
              <span v-if="onSale" class="ml-2 bg-red-600 text-white text-xs px-2 py-1 rounded">SALE</span>
            </div>
            <div class="mt-1 text-sm">
              <span v-if="inStock" class="text-green-500">In Stock</span>
              <span v-else class="text-red-500">Out of Stock</span>
            </div>
          </div>
          
          <!-- Add to Cart Button -->
          <button 
            @click="addToCart" 
            class="w-full md:w-auto bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-8 rounded mb-6 disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="!inStock"
          >
            <span v-if="inStock">Add to Cart</span>
            <span v-else>Out of Stock</span>
          </button>
          
          <!-- Description -->
          <div class="mb-6">
            <h2 class="text-xl font-semibold mb-2">Description</h2>
            <p class="text-gray-300 leading-relaxed">{{ product.description }}</p>
          </div>
          
          <!-- Details -->
          <div class="mb-6">
            <h2 class="text-xl font-semibold mb-2">Details</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p class="text-gray-400">Genre: <span class="text-white">{{ product.genre }}</span></p>
                <p class="text-gray-400">Runtime: <span class="text-white">{{ product.runtime }} minutes</span></p>
                <p class="text-gray-400">Format: <span class="text-white">{{ product.format }}</span></p>
              </div>
              <div>
                <p class="text-gray-400">Director: <span class="text-white">{{ product.director }}</span></p>
                <p class="text-gray-400">Rating: <span class="text-white">{{ product.rating }}/5</span></p>
              </div>
            </div>
          </div>
          
          <!-- Cast -->
          <div class="mb-6">
            <h2 class="text-xl font-semibold mb-2">Cast</h2>
            <div class="flex flex-wrap gap-2">
              <span 
                v-for="(actor, index) in product.starring" 
                :key="index" 
                class="bg-gray-800 text-white px-3 py-1 rounded-full text-sm"
              >
                {{ actor }}
              </span>
            </div>
          </div>
          
          <!-- Special Features -->
          <div>
            <h2 class="text-xl font-semibold mb-2">Special Features</h2>
            <ul class="list-disc list-inside text-gray-300">
              <li v-for="(feature, index) in product.specialFeatures" :key="index" class="mb-1">
                {{ feature }}
              </li>
            </ul>
          </div>
        </div>
      </div>
      
      <!-- Related Products -->
      <div class="mb-12">
        <h2 class="text-2xl font-bold mb-6">You May Also Like</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          <div 
            v-for="relatedProduct in relatedProducts" 
            :key="relatedProduct.id" 
            class="bg-gray-800 rounded-lg overflow-hidden hover:shadow-lg transition-shadow duration-300"
          >
            <NuxtLink :to="`/product/${relatedProduct.id}`">
              <!-- Placeholder image with gradient background -->
              <div class="aspect-[3/4] relative bg-gradient-to-br from-gray-700 to-gray-900 flex items-center justify-center">
                <span class="text-4xl font-bold text-white opacity-30">{{ relatedProduct.title.substring(0, 1) }}</span>
                
                <!-- Format Badge -->
                <div class="absolute top-2 right-2 bg-red-600 text-white text-xs font-bold px-2 py-1 rounded">
                  {{ relatedProduct.format }}
                </div>
              </div>
              
              <div class="p-4">
                <h3 class="font-bold text-lg mb-1 hover:text-red-500 transition-colors">{{ relatedProduct.title }}</h3>
                <p class="text-gray-400 text-sm mb-2">{{ relatedProduct.director }}</p>
                <div class="flex justify-between items-center">
                  <span class="font-bold">${{ calculatePrice(relatedProduct).toFixed(2) }}</span>
                  <div class="flex">
                    <span v-for="i in 5" :key="i" class="text-xs">
                      <span v-if="i <= Math.floor(relatedProduct.rating)" class="text-yellow-400">★</span>
                      <span v-else class="text-gray-600">★</span>
                    </span>
                  </div>
                </div>
              </div>
            </NuxtLink>
          </div>
        </div>
      </div>
      
      <!-- Customer Reviews -->
      <div>
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-bold">Customer Reviews</h2>
          <button class="bg-gray-800 hover:bg-gray-700 text-white px-4 py-2 rounded">
            Write a Review
          </button>
        </div>
        
        <!-- Reviews List -->
        <div v-if="reviews.length > 0">
          <div 
            v-for="(review, index) in reviews" 
            :key="index" 
            class="mb-6 pb-6 border-b border-gray-800"
          >
            <div class="flex justify-between mb-2">
              <div>
                <h3 class="font-bold">{{ review.title }}</h3>
                <div class="flex items-center">
                  <div class="flex">
                    <span v-for="i in 5" :key="i" class="text-sm">
                      <span v-if="i <= review.rating" class="text-yellow-400">★</span>
                      <span v-else class="text-gray-600">★</span>
                    </span>
                  </div>
                  <span class="ml-2 text-sm text-gray-400">by {{ review.author }}</span>
                </div>
              </div>
              <span class="text-sm text-gray-400">{{ review.date }}</span>
            </div>
            <p class="text-gray-300">{{ review.content }}</p>
          </div>
        </div>
        
        <!-- No Reviews -->
        <div v-else class="text-center py-8 bg-gray-800 rounded-lg">
          <p class="text-gray-400 mb-4">No reviews yet. Be the first to review this product!</p>
          <button class="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded">
            Write a Review
          </button>
        </div>
      </div>
      
      <!-- Cart Notification -->
      <div 
        v-if="showCartNotification" 
        class="fixed bottom-4 right-4 bg-green-600 text-white px-4 py-3 rounded-lg shadow-lg flex items-center"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        <span>Added to cart!</span>
        <NuxtLink to="/cart" class="ml-4 bg-white text-green-600 px-2 py-1 rounded text-sm">
          View Cart
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const loading = ref(true);
const error = ref(null);
const product = ref(null);
const relatedProducts = ref([]);
const reviews = ref([]);
const showCartNotification = ref(false);

// Computed properties
const productPrice = computed(() => {
  return calculatePrice(product.value);
});

const onSale = computed(() => {
  // For this prototype, we'll randomly put some products on sale
  return product.value && product.value.id % 3 === 0;
});

const inStock = computed(() => {
  // For this prototype, we'll randomly make some products out of stock
  return product.value && product.value.id % 7 !== 0;
});

// Helper functions
function calculatePrice(product) {
  if (!product) return 0;
  
  // Base price calculation based on format and rating
  let basePrice = 0;
  
  if (product.format.includes('4K')) {
    basePrice = 29.99;
  } else if (product.format.includes('Blu-ray')) {
    basePrice = 24.99;
  } else {
    basePrice = 19.99;
  }
  
  // Adjust price based on rating
  basePrice += (product.rating - 4) * 2;
  
  // Apply sale discount if applicable
  if (product.id % 3 === 0) {
    basePrice = basePrice * 0.8; // 20% off
  }
  
  return parseFloat(basePrice.toFixed(2));
}

function formatDate(dateString) {
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Date(dateString).toLocaleDateString(undefined, options);
}

function addToCart() {
  // Get existing cart from localStorage
  let cart = [];
  const cartJson = localStorage.getItem('pohkimCart');
  
  if (cartJson) {
    try {
      cart = JSON.parse(cartJson);
    } catch (e) {
      console.error('Error parsing cart data:', e);
      cart = [];
    }
  }
  
  // Check if product is already in cart
  const existingProductIndex = cart.findIndex(item => item.id === product.value.id);
  
  if (existingProductIndex >= 0) {
    // Increment quantity if already in cart
    cart[existingProductIndex].quantity += 1;
  } else {
    // Add new product to cart
    cart.push({
      id: product.value.id,
      title: product.value.title,
      price: productPrice.value,
      format: product.value.format,
      quantity: 1
    });
  }
  
  // Save updated cart to localStorage
  localStorage.setItem('pohkimCart', JSON.stringify(cart));
  
  // Update cart count in header
  if (typeof window !== 'undefined' && window.$nuxt) {
    window.$nuxt.$emit('update-cart');
  }
  
  // Show notification
  showCartNotification.value = true;
  setTimeout(() => {
    showCartNotification.value = false;
  }, 3000);
}

async function loadProduct() {
  loading.value = true;
  error.value = null;
  
  try {
    // In a real app, this would be an API call
    // For this prototype, we'll load from the static JSON file
    const response = await fetch('/products.json');
    if (!response.ok) {
      throw new Error('Failed to load products');
    }
    
    const products = await response.json();
    const productId = parseInt(route.params.id);
    
    // Find the product by ID
    const foundProduct = products.find(p => p.id === productId);
    
    if (foundProduct) {
      product.value = foundProduct;
      
      // Get related products (same genre, excluding current product)
      relatedProducts.value = products
        .filter(p => p.genre === foundProduct.genre && p.id !== productId)
        .slice(0, 4); // Limit to 4 related products
      
      // Generate some fake reviews
      generateFakeReviews();
    } else {
      error.value = 'Product not found';
    }
  } catch (err) {
    console.error('Error loading product:', err);
    error.value = 'There was a problem loading this product. Please try again.';
  } finally {
    loading.value = false;
  }
}

function generateFakeReviews() {
  // Only generate reviews for some products
  if (product.value.id % 2 === 0) {
    reviews.value = [
      {
        title: 'Excellent purchase!',
        rating: 5,
        author: 'MovieFan2023',
        date: '2 weeks ago',
        content: 'This is one of the best films I\'ve seen this year. The picture quality on this DVD is outstanding, and the special features are worth the price alone. Highly recommended!'
      },
      {
        title: 'Good movie, great extras',
        rating: 4,
        author: 'FilmCollector',
        date: '1 month ago',
        content: 'The film itself is very good, but what really impressed me were the special features. The director\'s commentary provides fascinating insights into the making of the film.'
      }
    ];
    
    // Add a critical review for some products
    if (product.value.id % 4 === 0) {
      reviews.value.push({
        title: 'Disappointed with the quality',
        rating: 2,
        author: 'QualityMatters',
        date: '3 weeks ago',
        content: 'While the movie itself is good, I was disappointed with the DVD quality. There were some artifacts in dark scenes, and the audio was not as clear as I expected.'
      });
    }
  } else {
    reviews.value = [];
  }
}

onMounted(() => {
  loadProduct();
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
</style> 