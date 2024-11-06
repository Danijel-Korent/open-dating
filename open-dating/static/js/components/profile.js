class Profile extends HTMLElement {
	static define(tag = "profile") {
		customElements.define(tag, this)
	}

	shadowRoot = this.attachShadow({ mode: "open" })

	constructor() {
		super()
		this.user = user
	}

}

customElements.define('profile', Profile)
