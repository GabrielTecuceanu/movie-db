import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { cubicOut } from "svelte/easing";
import type { TransitionConfig } from "svelte/transition";

export function cn(...inputs: ClassValue[]) {
	return twMerge(clsx(inputs));
}

type FlyAndScaleParams = {
	y?: number;
	x?: number;
	start?: number;
	duration?: number;
};

export const flyAndScale = (
	node: Element,
	params: FlyAndScaleParams = { y: -8, x: 0, start: 0.95, duration: 150 }
): TransitionConfig => {
	const style = getComputedStyle(node);
	const transform = style.transform === "none" ? "" : style.transform;

	const scaleConversion = (
		valueA: number,
		scaleA: [number, number],
		scaleB: [number, number]
	) => {
		const [minA, maxA] = scaleA;
		const [minB, maxB] = scaleB;

		const percentage = (valueA - minA) / (maxA - minA);
		const valueB = percentage * (maxB - minB) + minB;

		return valueB;
	};

	const styleToString = (
		style: Record<string, number | string | undefined>
	): string => {
		return Object.keys(style).reduce((str, key) => {
			if (style[key] === undefined) return str;
			return str + `${key}:${style[key]};`;
		}, "");
	};

	return {
		duration: params.duration ?? 200,
		delay: 0,
		css: (t) => {
			const y = scaleConversion(t, [0, 1], [params.y ?? 5, 0]);
			const x = scaleConversion(t, [0, 1], [params.x ?? 0, 0]);
			const scale = scaleConversion(t, [0, 1], [params.start ?? 0.95, 1]);

			return styleToString({
				transform: `${transform} translate3d(${x}px, ${y}px, 0) scale(${scale})`,
				opacity: t
			});
		},
		easing: cubicOut
	};
};

export const apiKey = import.meta.env.VITE_API_URL;
export const imgBaseUrl = "https://image.tmdb.org/t/p";
export const imgSizeSmall = "w300"; // Use desired size: w300, w780, w1280, original
export const imgSizeMedium = "w780"; // Use desired size: w300, w780, w1280, original
export const imgSizeBig = "w1280"; // Use desired size: w300, w780, w1280, original
export const imgOriginal = "original"; // Use desired size: w300, w780, w1280, original
export function redirectTo(path) {
	if (path === '#')
		return;
	window.location.href = path;
}

export const topGradientSoftness = 30;
export const bottomGradientSoftness = 0.5;

let movieGenres = null;
export async function getMovieGenres() {
	if (movieGenres != null)
		return movieGenres;

	try {
		const response = await fetch(`${apiKey}/genre/movie/list`);
		if (!response.ok) {
			throw new Error(
				`Could not get movie genres: ${response.status}`,
			);
		}

		const data = await response.json();
		movieGenres = data.genres
	} catch (e) {
		console.error(e)
	}

	return movieGenres;
}

let tvGenres = null;
export async function getTVGenres() {
	if (tvGenres != null)
		return tvGenres;

	try {
		const response = await fetch(`${apiKey}/genre/tv/list`);
		if (!response.ok) {
			throw new Error(
				`Could not get movie genres: ${response.status}`,
			);
		}

		const data = await response.json();
		tvGenres = data.genres
	} catch (e) {
		console.error(e)
	}

	return tvGenres;
}

export function clamp(num: number, lower: number, upper: number) {
	return Math.min(Math.max(num, lower), upper);
}

export function formatCurrency(number) {
	let formattedNumber = number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");

	return `$${formattedNumber}`;
}

export function combineAndShuffle(arr1, arr2) {
	let combinedArray = [...arr1, ...arr2];

	for (let i = combinedArray.length - 1; i > 0; i--) {
		const j = Math.floor(Math.random() * (i + 1));
		[combinedArray[i], combinedArray[j]] = [combinedArray[j], combinedArray[i]];
	}

	return combinedArray;
}

export function shuffle(arr) {
	for (let i = arr.length - 1; i > 0; i--) {
		const j = Math.floor(Math.random() * (i + 1));

		[arr[i], arr[j]] = [arr[j], arr[i]];
	}

	return arr;
}

export const getCookie = (name) => {
	const cookies = document.cookie.split('; ');
	const foundCookie = cookies.find((cookie) => cookie.startsWith(`${name}=`));
	return foundCookie ? foundCookie.split('=')[1] : null;
};

export enum mediaStatus {
	NONE,
	WATCHLIST,
	FINISHED,
}

export enum friendStatus {
	ME,
	FRIEND,
	STRANGER,
}

export async function fetchUsername(token) {
	try {
		let response = await fetch(`${apiKey}/token`, {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				Authorization: `Bearer ${token}`,
			},
		});
		if (!response.ok) {
			throw new Error(`Could not get username: ${response.status}`);
		}

		const data = await response.json();
		return data;
	} catch (e) {
		console.error(e);
	}
}