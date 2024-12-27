import { defineComponent, stringToBoolean } from "../utils";

export default defineComponent((shown: string) => ({
	height: 0,
	shown: stringToBoolean(shown),
	init() {
		this.setHeight();
		window.addEventListener("resize", () => {
			this.setHeight();
		})
		this.$watch("shown", () => this.setHeight())
	},
	setHeight() {
		this.height = this.$refs.profileWrapper.getBoundingClientRect().height;
	}
}))




