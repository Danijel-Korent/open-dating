export default () => ({
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
})

