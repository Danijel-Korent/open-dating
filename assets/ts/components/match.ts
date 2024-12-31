import { defineComponent } from "../utils";

export default defineComponent((url: string) => ({
	showMatch: false,
	async like() {
		let res = await fetch(url, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ type: 'like' })
		})

		let data = await res.json();
		if (data.match) {
			this.showMatch = true
		}
	},

	async nope() {
		let res = await fetch(url, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				type: 'nope'
			})
		})

		window.location.reload();
	}
}))
