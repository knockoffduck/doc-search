import { compile } from 'mdsvex';

/** @type {import('./$types').Actions} */
export const actions = {
	default: async (event) => {
		console.log(event);
	}
};
