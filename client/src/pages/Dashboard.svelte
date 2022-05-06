<script>
    import {user} from "../stores/store";

    import BaseDashboard from "../components/Base.svelte";
    import RecruitDashboard from "./Recruits/RecruitDashboard.svelte";
    import RecruiterDashboard from "./Recruiters/RecruiterDashboard.svelte";
</script>

<BaseDashboard>

    {#if $user.user.role === 1}
        <RecruiterDashboard/>
    {:else}
        <RecruitDashboard/>
    {/if}

</BaseDashboard>