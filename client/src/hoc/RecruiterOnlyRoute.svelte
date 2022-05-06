<script>
    import RecruiterGuard from "./RecruiterGuard.svelte";
    import PrivateRoute from "./PrivateRoute.svelte";

    export let path;
</script>

<PrivateRoute {path} let:params let:location let:navigate>
    <RecruiterGuard>
        <slot {params} {location} {navigate} />
    </RecruiterGuard>
</PrivateRoute>
