<script>
    import { useNavigate, useLocation } from "svelte-navigator";
    import { user } from "../stores/store";
    import {onMount} from "svelte";
    const navigate = useNavigate();
    const location = useLocation();

    function changeRoute(data){
        if (data.user && data.user.role !== 1) {
            navigate("/", {
                state: { from: $location.pathname },
                replace: true,
            });
        }
    }

    user.subscribe(data => {
        changeRoute(data)
    })

    onMount(()=>{
        changeRoute($user)
    })

</script>

{#if $user.token}
    <slot />
{/if}