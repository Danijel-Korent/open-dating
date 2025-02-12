// This file is loaded at the start of the HTML and is the entry point for webpack
import 'htmx.org'
import * as htmx from "htmx.org"
import { ChevronDown, createIcons, Minus, Plus, ArrowRight, Group, Check, Heart, Home, RotateCcw, Send, Settings, Sliders, User, Users, X } from "lucide";
import Alpine from 'alpinejs';

import modal from "./components/modal"
import profile from "./components/profile"
import checkbox from './components/checkbox';
import range from './components/range';
import match from './components/match';
import interest from './components/interest';

declare global {
	interface Window { htmx: any, Alpine: any, lucide: () => void }
}

window.htmx = htmx
window.Alpine = Alpine
window.lucide = () => {
	createIcons({ icons: { Home, Heart, User, Group, ArrowRight, Settings, Minus, Plus, Check, Sliders, ChevronDown, Send, RotateCcw, Users, X } })
}

Alpine.data("userProfile", profile)
Alpine.data("modal", modal)
Alpine.data("checkbox", checkbox)
Alpine.data("range", range)
Alpine.data("matchButtons", match)
Alpine.data("interest", interest)

Alpine.start()
window.lucide()

document.addEventListener('htmx:afterRequest', function (evt) {
	window.lucide()
});

