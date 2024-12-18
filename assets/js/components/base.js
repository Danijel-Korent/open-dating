// This file defines basic AlpineJS components for common patterns. These are usually parent containers for things like modals
import Alpine from 'alpinejs'

document.addEventListener('alpine:init', () => {
  Alpine.data('modal', () => ({
    modalOpen: false
  }))
  Alpine.data('userProfile', () => ({
    profileHeight: 0,

    initHeight() {
      this.profileHeight = this.$refs.profileWrapper.getBoundingClientRect().height;

      window.addEventListener('resize', () => {
        this.profileHeight = this.$refs.profileWrapper.getBoundingClientRect().height;
      });
    },

  }));
})
