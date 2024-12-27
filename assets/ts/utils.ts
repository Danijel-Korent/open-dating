import { AlpineComponent } from "alpinejs"

export const stringToBoolean = (val: string): boolean => {
	return val === "true" || val === "TRUE" || val === "true"
}

export const defineComponent = <P, T>(fn: (params: P) => AlpineComponent<T>) => {
	return fn
}
