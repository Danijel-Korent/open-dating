import { defineComponent, stringToBoolean } from "../utils";

export default defineComponent((checked: string) => ({
	checked: stringToBoolean(checked),

	check() {
		this.checked = !this.checked
	}
}))


