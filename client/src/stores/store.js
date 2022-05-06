import { writable } from "svelte/store";

export let user = writable({
    token: null,
    user: null,
});

export let authLoading = writable(true);

export let refCode = writable({
    code: null,
    loading: false,
    error: false,
});

export let referralList = writable({
    nextPage: 1,
    loading: false,
    results: []
});

export let commissionList = writable({
    nextPage: 1,
    loading: false,
    results: []
});

export let recruiterInfo = writable(
    {
        loading: false,
        total_recruited: null,
        bonus: null
    }
)