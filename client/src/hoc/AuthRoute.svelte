<script>
    import { Route } from "svelte-navigator";
    import AuthRouteGuard from "./AuthRouteGuard.svelte";
    export let path;
</script>

<Route {path} let:params let:location let:navigate>
    <AuthRouteGuard>
        <slot {params} {location} {navigate} />
    </AuthRouteGuard>
</Route>
