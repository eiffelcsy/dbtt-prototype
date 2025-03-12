<template>
  <header class="header bg-gray-900 text-white border-b border-gray-800 sticky top-0 z-30">
    <div class="container mx-auto px-4">
      <div class="flex items-center justify-between py-4">
        <!-- Logo -->
        <NuxtLink to="/" class="text-red-600 font-bold text-2xl">POHKIM</NuxtLink>
        
        <!-- Desktop Navigation -->
        <nav class="hidden md:flex space-x-6">
          <NuxtLink to="/" class="nav-link">Home</NuxtLink>
          <NuxtLink to="/store" class="nav-link">DVD Store</NuxtLink>
          <NuxtLink to="/forum" class="nav-link">Community</NuxtLink>
          <NuxtLink to="/about" class="nav-link">About</NuxtLink>
        </nav>
        
        <!-- Right Side - Search, User, and Cart -->
        <div class="flex items-center space-x-4">
          <div class="hidden md:block">
            <div class="relative">
              <input 
                type="text" 
                placeholder="Search..." 
                class="bg-gray-800 text-white rounded-full py-1 px-4 w-48 focus:outline-none focus:ring-1 focus:ring-red-600"
              >
              <button class="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400">
                🔍
              </button>
            </div>
          </div>
          
          <!-- Cart Icon -->
          <NuxtLink to="/cart" class="relative">
            <div class="text-white hover:text-red-500 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              <span v-if="cartItemCount > 0" class="absolute -top-2 -right-2 bg-red-600 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                {{ cartItemCount }}
              </span>
            </div>
          </NuxtLink>
          
          <div class="user-profile">
            <button class="flex items-center space-x-2">
              <div class="w-8 h-8 rounded-full bg-red-600 flex items-center justify-center">
                <span class="font-bold">P</span>
              </div>
              <span class="hidden md:inline">My Account</span>
            </button>
          </div>
          
          <!-- Mobile Menu Button -->
          <button class="md:hidden" @click="mobileMenuOpen = !mobileMenuOpen">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7" />
            </svg>
          </button>
        </div>
      </div>
      
      <!-- Mobile Menu -->
      <div v-if="mobileMenuOpen" class="md:hidden py-4 border-t border-gray-800">
        <div class="flex flex-col space-y-4">
          <NuxtLink to="/" class="nav-link block" @click="mobileMenuOpen = false">Home</NuxtLink>
          <NuxtLink to="/store" class="nav-link block" @click="mobileMenuOpen = false">DVD Store</NuxtLink>
          <NuxtLink to="/forum" class="nav-link block" @click="mobileMenuOpen = false">Community</NuxtLink>
          <NuxtLink to="/about" class="nav-link block" @click="mobileMenuOpen = false">About</NuxtLink>
          
          <div class="pt-2">
            <div class="relative">
              <input 
                type="text" 
                placeholder="Search..." 
                class="bg-gray-800 text-white rounded-full py-1 px-4 w-full focus:outline-none focus:ring-1 focus:ring-red-600"
              >
              <button class="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400">
                🔍
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed } from 'vue';

const mobileMenuOpen = ref(false);

// This would typically come from a store in a real application
const cartItemCount = ref(0);

// Function to update cart count (for demo purposes)
function updateCartCount(count) {
  cartItemCount.value = count;
}

// Expose the function to be used by other components
defineExpose({
  updateCartCount
});
</script>

<style scoped>
.nav-link {
  position: relative;
  font-weight: 500;
  padding: 0.25rem 0;
  transition: color 0.3s;
}

.nav-link:hover {
  color: #EF4444;
}

.nav-link.router-link-active {
  color: #EF4444;
}

.nav-link.router-link-active::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: #EF4444;
}
</style> 