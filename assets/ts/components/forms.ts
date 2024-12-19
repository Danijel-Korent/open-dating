import Alpine from "alpinejs"

document.addEventListener('alpine:init', () => {
  Alpine.data('checkbox', (checked: boolean) => ({
    checked: checked,

    toggle() {
      this.checked = !this.checked
    }

  }))
})
