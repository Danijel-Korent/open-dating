import Alpine from "alpinejs"

document.addEventListener('alpine:init', () => {
  Alpine.data('preferenceModal', () => ({
    modalOpen: true,

    async submit(preferences: any) {
      await fetch("/api/preferences", { method: "POST", headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(preferences) })
    }
  }))

})

