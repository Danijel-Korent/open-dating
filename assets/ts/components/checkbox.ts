import Alpine from "alpinejs";

document.addEventListener("alpine:init", () => {
	Alpine.data("checkbox", (checked: string) => ({
		checked: checked === "true" || checked === "True" ? true : false,

		check() {
			this.checked = !this.checked
		}
	}))
})
