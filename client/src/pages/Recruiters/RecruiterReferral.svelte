<script>
    import {getReferralList} from "../../api/recruiter";
    import {referralList, user} from "../../stores/store";
    import {formatDate} from "../../utils";
    import {Link} from "svelte-navigator";
    import BaseDashboard from "../../components/Base.svelte"
    import {onMount} from "svelte";
    import UniqueLink from "../../components/UniqueLink.svelte";
    import AlertError from "../../components/AlertError.svelte";
    import {LIST_LOAD_ERROR_MSG} from "../../const";

    // Copy State
    let error = false;


    // Loads Referral List
    function loadReferral() {
        if ($referralList.nextPage) {
            // Trigger Loader
            referralList.update((data) => {
                return {
                    ...data,
                    loading: true
                }
            })
            // Call Api
            getReferralList($user.token, $referralList.nextPage)
                // Api Success
                .then(res => {
                    referralList.set({
                        nextPage: res.data.next ? $referralList.nextPage + 1 : null,
                        loading: false,
                        results: [...$referralList.results, ...res.data.results],
                    })
                    error = false;
                }).catch((e) => {
                error = false;
                referralList.update((data) => {
                    return {
                        ...data,
                        loading: false
                    }
                })
            })
        }
    }

    onMount(() => {
        loadReferral()
    })
</script>


<BaseDashboard>
    <section class="container">
        <UniqueLink/>
        <h2 class="my-5">Your Recruit List</h2>
        {#if error}
            <AlertError msg={LIST_LOAD_ERROR_MSG}/>
        {/if}
        <div class="table-container">
            <table class="table ">
                <thead>
                <tr>
                    <td>ID</td>
                    <td>RECRUIT NAME</td>
                    <td>RECRUIT EMAIL</td>
                    <td>DATE JOINED</td>
                </tr>
                </thead>
                {#if $referralList.results}
                    <tbody>
                    {#each $referralList.results as {id, recruit, time_stamp,}, j}
                        <tr>
                            <td>
                                {id}
                            </td>
                            <td>
                                {recruit.first_name} {recruit.last_name}
                            </td>
                            <td>
                                {recruit.email}
                            </td>
                            <td>
                                {formatDate(time_stamp)}
                            </td>

                        </tr>
                    {/each}

                    </tbody>
                {/if}
            </table>
            {#if $referralList.nextPage}
                <button on:click={loadReferral} class="btn btn-outline-theme">
                    Load More
                </button>
            {/if}
        </div>
        {#if $referralList.loading}
            <div class="w-100 d-flex my-3 justify-content-center align-items-center">
                <span class="spinner-border theme-color"></span>
            </div>
        {/if}
        {#if $referralList.results.length === 0}
            <div class="d-flex justify-content-center align-items-center my-3">
                <div class="img-container mr-2" style="width: 40px; margin-right: 10px">
                    <img width="100%" src="/referral_static/images/box.svg" alt="">
                </div>
                <p>No recruits</p>
            </div>
        {/if}


        <br>
        <br>
        <p class="text-center">For More Information About our recruiting program, click here
            <Link to="/about" class="btn btn-outline-theme">LEARN MORE</Link>
        </p>
    </section>
</BaseDashboard>
