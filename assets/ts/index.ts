// This file is loaded at the start of the HTML and is the entry point for webpack
import 'htmx.org'
import * as htmx from "htmx.org"
import { ChevronDown, createIcons, Group, Check, Heart, Home, RotateCcw, Send, Settings, Sliders, User, Users, X } from "lucide";
import Alpine from 'alpinejs';

import "./components/modal.ts"
import "./components/checkbox.ts"

declare global {
	interface Window { htmx: any, Alpine: any }
}

window.Alpine = Alpine
window.htmx = htmx

Alpine.start()


createIcons({
	icons: {
		Home, Heart, User, Group, Settings, Check, Sliders, ChevronDown, Send, RotateCcw, Users, X
	}
})
