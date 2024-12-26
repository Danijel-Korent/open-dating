import Alpine from "alpinejs"

document.addEventListener("alpine:init", () => {
	Alpine.data('modal', () => ({
		modalOpen: false,

		toggle() {
			this.modalOpen = !this.modalOpen
		},
		close() {
			this.modalOpen = false
		},
		open() {
			this.modalOpen = true
		}
	}))
})
