<script>
	import { onMount } from 'svelte';
	import { pb } from '../lib/pocketbase';
	import { marked } from 'marked';
	import Prism from 'prismjs';

	import 'prismjs/components/prism-javascript';
	import 'prismjs/components/prism-css';
	import 'prismjs/components/prism-python';
	import 'prismjs/themes/prism-tomorrow.css';

	/**
	 * @type {any[]}
	 */
	let messages_text = [];
	marked.setOptions({
		highlight: function (code, lang) {
			if (Prism.languages[lang]) {
				return Prism.highlight(code, Prism.languages[lang], lang);
			} else {
				return code; // fallback to no highlighting
			}
		}
	});
	/**
	 * @type {any[]}
	 */
	let messages = [];
	onMount(async () => {
		messages = await pb.collection('messages').getFullList();
	});

	let text = '';

	let contentHTML = '';

	/**
	 * @returns {Promise<void>}
	 */
	const handleOnSubmit = async (event) => {
		const form = event.target;
		const data = new FormData(form);
		const userRes = await pb.collection('messages').create({ role: 'user', body: text });
		messages = [...messages, await userRes];
		const response = await fetch('/api/chat', {
			method: 'POST',
			body: data
		});

		contentHTML = (await response.json()).body;
		console.log(contentHTML);

		const assistantRes = await pb
			.collection('messages')
			.create({ role: 'assistant', body: contentHTML });
		messages = [...messages, await assistantRes];
	};

	$: messages;

	let rows = 1;

	$: rows = text.split('\n').length < 10 ? text.split('\n').length : 10;

	/**
	 * Handle the key press event.
	 * @param {KeyboardEvent} event - The keyboard event object.
	 * @returns {void}
	 */
	const handleOnEnter = (event) => {
		if (event.key === 'Enter' && event.shiftKey) {
			rows = rows + 1;
		}
		if (event.key === 'Enter' && event.shiftKey) {
			handleOnSubmit();
		}
	};
</script>

<div class=" w-full p-14">
	<div class="h-full w-full bg-light-gray rounded-3xl flex flex-col p-8 gap-5">
		<div
			class="h-full w-full pr-2 gap-3 overflow-y-auto scrollbar-thumb-gray scrollbar-thumb-rounded-xl scrollbar-thin"
		>
			{#if messages}
				{#each messages as message}
					{#if message.role === 'user'}
						<div class="w-full rounded-xl p-4 bg-gray">
							<span>{message.body}</span>
						</div>
					{:else}
						<div class="w-full rounded-xl p-4 bg-light-gray">
							{@html marked(message.body)}
						</div>
					{/if}
				{/each}
			{/if}
		</div>
		<form on:submit|preventDefault={handleOnSubmit} class="w-full flex gap-3">
			<textarea
				name="query"
				class="w-full resize-none scrollbar-thin scrollbar-thumb-primary scrollbar-thumb-rounded-md h-full rounded-lg focus:outline-none bg-gray p-3"
				{rows}
				bind:value={text}
				on:keydown={handleOnEnter}
			/>
			<button class="btn btn-primary rounded-lg normal-case">Send</button>
		</form>
	</div>
</div>
