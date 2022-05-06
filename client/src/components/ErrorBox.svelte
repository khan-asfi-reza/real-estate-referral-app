<script>
    import {capitalize} from "../utils";

    export let error;

</script>


{#if error && Object.keys(error).length}
<div class="alert alert-danger my-4 form-box mx-auto" role="alert">
    {#each Object.keys(error) as err, i}
        <div class="my-2">
        {capitalize(err)} {error[err]}
        </div>
    {/each}
</div>
{/if}