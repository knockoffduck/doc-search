<script>
	import '../app.css';
	import { pb } from '../lib/pocketbase';
	import { slide } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

	let popup = false;
	let status = '';

	const ingest = async () => {
		const response = await fetch('http://127.0.0.1:5000/api/build_database');
		status = (await response.json()).status === 'success' ? 'Documents Ingested' : 'Failed';
		popup = true;
		setTimeout(() => {
			popup = false;
		}, 1000);
	};

	const clearDocs = async () => {
		const response = await fetch('http://127.0.0.1:5000/api/delete_database');
		const documents = await pb.collection('messages').getFullList();
		for (const message of documents) {
			await pb.collection('messages').delete(message.id);
		}

		status = (await response.json()).status === 'success' ? 'Documents Cleared' : 'Failed';
		popup = true;
		setTimeout(() => {
			popup = false;
		}, 1000);
	};

	const clearChat = async () => {
		let status = '';
		try {
			const documents = await pb.collection('messages').getFullList();
			for (const message of documents) {
				await pb.collection('messages').delete(message.id);
			}
			status = 'success';
		} catch (error) {
			console.log(error);
			status = 'failed';
		}
		popup = true;
		setTimeout(() => {
			popup = false;
		}, 1000);
	};
</script>

<div class="h-screen w-screen bg-gray flex">
	<div class="flex flex-col h-full w-44 p-4 border-r border-r-light-gray">
		<button on:click={ingest} class="btn btn-ghost normal-case">Ingest</button>
		<button on:click={clearDocs} class="btn btn-ghost normal-case">Clear Docs</button>
		<button on:click={clearChat} class="btn btn-ghost normal-case">Clear Chats</button>
	</div>

	<slot />
	{#if popup}
		<div in:slide out:slide class="fixed inset-0 flex h-fit justify-center top-3 z-50">
			<div class="alert w-fit alert-success shadow-lg">
				<div>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="stroke-current flex-shrink-0 h-6 w-6"
						fill="none"
						viewBox="0 0 24 24"
						><path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
						/></svg
					>
					<span>{status}</span>
				</div>
			</div>
		</div>
	{/if}
</div>
