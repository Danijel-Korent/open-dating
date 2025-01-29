import { defineComponent } from "../utils";

//This is a bad way to do this. In future, we should fetch all interest info in one go. It's ok for prototyping though.
export default defineComponent((id: string) => ({
	icon: "",
	name: "",

	async getInterest() {
		const res = await fetch(`/api/get_interest/${id}`)
		const interest = await res.json()

		if (interest) {
			this.icon = interest.icon
			this.name = interest.name
		}
	},

	init() {
		this.getInterest()
	}
}))
