<template>
  <div class="cart min-h-screen bg-gray-900 text-white p-8">
    <h1 class="text-3xl font-bold mb-8">Your Shopping Cart</h1>
    
    <!-- Empty Cart -->
    <div v-if="cart.length === 0" class="text-center py-16">
      <div class="text-gray-400 mb-6">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-24 w-24 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
        <p class="text-xl">Your cart is empty</p>
      </div>
      <NuxtLink to="/store" class="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-6 rounded-md transition-colors duration-300">
        Browse DVDs
      </NuxtLink>
    </div>
    
    <!-- Cart with Items -->
    <div v-else>
      <!-- Cart Items -->
      <div class="bg-gray-800 rounded-lg overflow-hidden mb-8">
        <table class="w-full">
          <thead>
            <tr class="bg-gray-700">
              <th class="py-3 px-4 text-left">Product</th>
              <th class="py-3 px-4 text-center">Price</th>
              <th class="py-3 px-4 text-center">Quantity</th>
              <th class="py-3 px-4 text-right">Total</th>
              <th class="py-3 px-4 text-center">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in cart" :key="item.id" class="border-b border-gray-700">
              <td class="py-4 px-4">
                <div class="flex items-center">
                  <div class="w-16 h-16 bg-gradient-to-r from-gray-700 to-gray-600 flex items-center justify-center rounded mr-4">
                    <span class="text-gray-400 text-xs">{{ item.title }}</span>
                  </div>
                  <div>
                    <h3 class="font-semibold">{{ item.title }}</h3>
                    <p class="text-gray-400 text-sm">{{ item.format }}</p>
                  </div>
                </div>
              </td>
              <td class="py-4 px-4 text-center">${{ item.price }}</td>
              <td class="py-4 px-4">
                <div class="flex items-center justify-center">
                  <button 
                    @click="decreaseQuantity(item)" 
                    class="bg-gray-700 hover:bg-gray-600 text-white w-8 h-8 rounded-l"
                    :disabled="item.quantity <= 1"
                  >-</button>
                  <span class="bg-gray-700 text-white px-4 py-1">{{ item.quantity }}</span>
                  <button 
                    @click="increaseQuantity(item)" 
                    class="bg-gray-700 hover:bg-gray-600 text-white w-8 h-8 rounded-r"
                  >+</button>
                </div>
              </td>
              <td class="py-4 px-4 text-right font-bold">${{ (item.price * item.quantity).toFixed(2) }}</td>
              <td class="py-4 px-4 text-center">
                <button @click="removeItem(item)" class="text-red-500 hover:text-red-400">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Cart Summary -->
      <div class="flex flex-col md:flex-row justify-between gap-8">
        <div class="md:w-1/2">
          <div class="bg-gray-800 rounded-lg p-6">
            <h2 class="text-xl font-semibold mb-4">Order Summary</h2>
            <div class="space-y-2 mb-4">
              <div class="flex justify-between">
                <span>Subtotal</span>
                <span>${{ subtotal.toFixed(2) }}</span>
              </div>
              <div class="flex justify-between">
                <span>Shipping</span>
                <span>${{ shipping.toFixed(2) }}</span>
              </div>
              <div class="flex justify-between">
                <span>Tax</span>
                <span>${{ tax.toFixed(2) }}</span>
              </div>
              <div class="border-t border-gray-700 pt-2 mt-2">
                <div class="flex justify-between font-bold">
                  <span>Total</span>
                  <span>${{ total.toFixed(2) }}</span>
                </div>
              </div>
            </div>
            <button @click="checkout" class="w-full bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-4 rounded transition-colors duration-300">
              Proceed to Checkout
            </button>
          </div>
        </div>
        
        <div class="md:w-1/2">
          <div class="bg-gray-800 rounded-lg p-6">
            <h2 class="text-xl font-semibold mb-4">Have a Promo Code?</h2>
            <div class="flex">
              <input 
                type="text" 
                placeholder="Enter promo code" 
                class="bg-gray-700 text-white rounded-l p-2 border border-gray-600 flex-grow"
              >
              <button class="bg-gray-600 hover:bg-gray-500 text-white font-bold py-2 px-4 rounded-r">
                Apply
              </button>
            </div>
          </div>
          
          <div class="bg-gray-800 rounded-lg p-6 mt-6">
            <h2 class="text-xl font-semibold mb-4">Need Help?</h2>
            <p class="text-gray-400 mb-4">
              Our customer service team is available 24/7 to assist you with your purchase.
            </p>
            <a href="#" class="text-red-500 hover:text-red-400 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
              </svg>
              Contact Support
            </a>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Checkout Success Modal -->
    <div v-if="showCheckoutModal" class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
      <div class="bg-gray-800 rounded-lg p-8 max-w-md w-full">
        <div class="text-center">
          <div class="bg-green-600 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h2 class="text-2xl font-bold mb-2">Order Placed Successfully!</h2>
          <p class="text-gray-400 mb-6">
            Thank you for your purchase. Your order has been placed and will be processed shortly.
          </p>
          <button @click="closeCheckoutModal" class="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-6 rounded transition-colors duration-300">
            Continue Shopping
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

const cart = ref([]);
const showCheckoutModal = ref(false);

// Calculate cart totals
const subtotal = computed(() => {
  return cart.value.reduce((total, item) => total + (parseFloat(item.price) * item.quantity), 0);
});

const shipping = computed(() => {
  return subtotal.value > 50 ? 0 : 5.99;
});

const tax = computed(() => {
  return subtotal.value * 0.08; // 8% tax
});

const total = computed(() => {
  return subtotal.value + shipping.value + tax.value;
});

function increaseQuantity(item) {
  item.quantity += 1;
  updateCart();
}

function decreaseQuantity(item) {
  if (item.quantity > 1) {
    item.quantity -= 1;
    updateCart();
  }
}

function removeItem(item) {
  cart.value = cart.value.filter(cartItem => cartItem.id !== item.id);
  updateCart();
}

function updateCart() {
  // Save cart to localStorage
  localStorage.setItem('cart', JSON.stringify(cart.value));
  
  // Update cart count in header
  const headerComponent = document.querySelector('header').__vueParentComponent.exposed;
  if (headerComponent && headerComponent.updateCartCount) {
    headerComponent.updateCartCount(cart.value.reduce((total, item) => total + item.quantity, 0));
  }
}

function checkout() {
  showCheckoutModal.value = true;
}

function closeCheckoutModal() {
  showCheckoutModal.value = false;
  // Clear cart after checkout
  cart.value = [];
  updateCart();
}

onMounted(() => {
  // Load cart from localStorage
  const savedCart = localStorage.getItem('cart');
  if (savedCart) {
    cart.value = JSON.parse(savedCart);
  }
});
</script>

<style scoped>
/* Additional styling can be added here if needed */
</style> 