import { defineComponent } from "../utils";

export default defineComponent((value: number) => ({
	value: value,

	increment(amount: number) {
		this.value += amount
	},
	decrement(amount: number) {
		this.value -= amount
	}
}))
