/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				'light-gray': '#222731',
				gray: '#1B1E28'
			}
		}
	},
	plugins: [
		require('daisyui'),
		require('@tailwindcss/typography'),
		require('tailwind-scrollbar')({ nocompatible: true })
	]
};
