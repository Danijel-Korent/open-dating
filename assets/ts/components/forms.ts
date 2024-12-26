import Alpine from "alpinejs"

document.addEventListener('alpine:init', () => {
  Alpine.data('checkbox', (checked: boolean = false) => ({
    checked: checked,

    toggle() {
      this.checked = !this.checked
    }

  }))
})
