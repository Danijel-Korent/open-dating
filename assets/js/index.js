// This file is loaded at the start of the HTML and is the entry point for webpack
import Alpine from 'alpinejs';

import { ChevronDown, createIcons, Group, Check, Heart, Home, RotateCcw, Send, Settings, Sliders, User, Users, X } from "lucide";
import './components/base';

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

window.Alpine = Alpine

Alpine.start()



createIcons({
  icons: {
    Home, Heart, User, Group, Settings, Check, Sliders, ChevronDown, Send, RotateCcw, Users, X
  }
})
