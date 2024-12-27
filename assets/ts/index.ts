// This file is loaded at the start of the HTML and is the entry point for webpack
import 'htmx.org'
import * as htmx from "htmx.org"
import { ChevronDown, createIcons, Group, Check, Heart, Home, RotateCcw, Send, Settings, Sliders, User, Users, X } from "lucide";
import Alpine from 'alpinejs';

import modal from "./components/modal"
import profile from "./components/profile"
import checkbox from './components/checkbox';

declare global {
	interface Window { htmx: any, Alpine: any }
}

window.Alpine = Alpine
window.htmx = htmx

Alpine.start()
Alpine.data("userProfile", profile)
Alpine.data("modal", modal)
Alpine.data("checkbox", checkbox)


createIcons({
	icons: {
		Home, Heart, User, Group, Settings, Check, Sliders, ChevronDown, Send, RotateCcw, Users, X
	}
})
