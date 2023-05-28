import { compile } from 'mdsvex';
import { messages, pb } from '../../../lib/pocketbase';

export const POST = async (event) => {
	const data = await event.request.formData();
	const query = data.get('query');

	//await pb.collection('messages').create({ role: 'user', body: query });

	const response = await fetch('http://127.0.0.1:5000/api/answer_query', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
			// like application/json or text/xml
		},
		body: JSON.stringify({
			query: query
		})
	});

	const reply = (await response.json()).result;

	return new Response(JSON.stringify({ success: true, body: reply }), {
		headers: {
			'Content-Type': 'application/json'
		}
	});
};
