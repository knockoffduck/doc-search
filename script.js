import { ChromaClient } from 'chromadb';

const client = new ChromaClient();

import { OpenAIEmbeddingFunction } from 'chromadb';
const embedder = new OpenAIEmbeddingFunction({
	openai_api_key: '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'
});
const collection = await client.createCollection({
	name: 'my_collection',
	embeddingFunction: embedder
});
