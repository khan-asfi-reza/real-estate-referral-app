<script>
    import { useNavigate, useLocation } from "svelte-navigator";
    import { user } from "../stores/store";
    import {onMount} from "svelte";
    const navigate = useNavigate();
    const location = useLocation();

    function changeRoute(data){
        if (!data.token) {
            navigate("/login", {
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