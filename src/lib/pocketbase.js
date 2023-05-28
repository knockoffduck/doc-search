import PocketBase from 'pocketbase';

import { writable } from 'svelte/store';

export const pb = new PocketBase('http://127.0.0.1:8090');

const authData = await pb.admins.authWithPassword('ddarm4@gmail.com', '#%fw6%f8CX!vMjnZQGZ');
