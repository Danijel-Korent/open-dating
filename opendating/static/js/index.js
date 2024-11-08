
document.addEventListener('alpine:init', () => {
	Alpine.data('imgPreview', (initialImg) => ({
		imgsrc: initialImg || null,
		previewFile() {
			let file = this.$refs.imageInput.files[0]
			if (!file || file.type.indexOf('image/') === -1) return;
			this.imgsrc = null;
			let reader = new FileReader();

			reader.onload = e => {
				this.imgsrc = e.target.result;
			}

			reader.readAsDataURL(file)
		}
	}))
})


var socket = io()
socket.on('connect', function() {
	socket.emit('connectedEvent', { data: "Connection established" })
	console.log("Connection established")
})
