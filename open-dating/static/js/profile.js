import Alpine from 'alpine'

document.addEventListener('alpine:init', () => {
	Alpine.data('userProfile', (user_react) => ({
		hasButtons: false,
		matchPopup: false,

		async like() {
			let res = await fetch(user_react, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ type: 'like' })
			})

			let data = await res.json();
			if (data.match) {
				this.matchPopup = true
			}
		},

		async nope() {
			let res = await fetch('{{url_for('dating.react_user', user=user.username)}}', {
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




	}));
})
