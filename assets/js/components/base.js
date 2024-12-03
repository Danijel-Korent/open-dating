// This file defines basic AlpineJS components for common patterns. These are usually parent containers for things like modals
import Alpine from 'alpinejs'

document.addEventListener('alpine:init', () => {
	Alpine.data('modal', () => ({
		modalOpen: false
	}))
})
