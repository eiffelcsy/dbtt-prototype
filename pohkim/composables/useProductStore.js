import { ref } from 'vue';

// Create a singleton store instance that persists across imports
let _selectedProduct = null;

export const useProductStore = () => {
  // Initialize the store if it hasn't been initialized yet
  if (_selectedProduct === null) {
    _selectedProduct = ref(null);
  }

  // Function to open the product overlay
  const openProductOverlay = (product) => {
    _selectedProduct.value = product;
  };

  // Function to close the product overlay
  const closeProductOverlay = () => {
    _selectedProduct.value = null;
  };

  return {
    selectedProduct: _selectedProduct,
    openProductOverlay,
    closeProductOverlay,
  };
}; 