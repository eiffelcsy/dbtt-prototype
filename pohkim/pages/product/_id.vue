<template>
  <div>Redirecting...</div>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router';
import { onMounted } from 'vue';
import { useProductStore } from '~/composables/useProductStore';

const router = useRouter();
const route = useRoute();
const productStore = useProductStore();

onMounted(async () => {
  const productId = route.params.id;
  
  try {
    // In a real app, you would fetch the product data from an API
    // For this prototype, we'll create mock data
    const response = await fetch('/videos.json');
    if (!response.ok) {
      throw new Error('Failed to fetch products');
    }
    
    const videos = await response.json();
    const video = videos.find(v => v.id === productId || v.productId === productId);
    
    if (video) {
      // Convert video to product format
      const product = {
        ...video,
        id: video.productId || video.id,
        price: (Math.random() * 20 + 9.99).toFixed(2),
        inStock: Math.random() > 0.2,
        format: Math.random() > 0.5 ? 'DVD' : 'Blu-ray',
      };
      
      // Open the product overlay
      productStore.openProductOverlay(product);
    }
    
    // Redirect to store page
    router.replace('/store');
  } catch (error) {
    console.error('Error fetching product:', error);
    // Redirect to store page on error
    router.replace('/store');
  }
});
</script> 