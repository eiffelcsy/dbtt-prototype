<template>
  <header class="header bg-gray-900 text-white border-b border-gray-800 sticky top-0 z-30">
    <div class="container mx-auto px-4">
      <div class="flex items-center justify-between py-4">
        <!-- Logo -->
        <NuxtLink to="/" class="text-red-600 font-bold text-2xl">POHKIM</NuxtLink>
        
        <!-- Desktop Navigation -->
        <nav class="hidden md:flex space-x-6">
          <NuxtLink to="/" class="nav-link">Home</NuxtLink>
          <NuxtLink to="/movies" class="nav-link">Movies & Shows</NuxtLink>
          <NuxtLink to="/about" class="nav-link">About</NuxtLink>
        </nav>
        
        <!-- Right Side - Search and User -->
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
          <NuxtLink to="/movies" class="nav-link block" @click="mobileMenuOpen = false">Movies & Shows</NuxtLink>
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
import { ref } from 'vue';

const mobileMenuOpen = ref(false);
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