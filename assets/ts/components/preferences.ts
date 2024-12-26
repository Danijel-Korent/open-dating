import Alpine from "alpinejs"

document.addEventListener('alpine:init', () => {
  Alpine.data('preferenceModal', () => ({
    modalOpen: true,
    preferences: {
      gender: {
        male: null,
        female: null,
        nonbinary: null
      },
      distance_meters: null,
      age_min: null,
      age_max: null
    },

    async init() {
      const preferences = await fetch("/api/preferences", { method: "GET" })
      this.preferences = await preferences.json()
    },

    async submit() {
      await fetch("/api/preferences", { method: "POST", headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(this.preferences) })
    }
  }))

})

