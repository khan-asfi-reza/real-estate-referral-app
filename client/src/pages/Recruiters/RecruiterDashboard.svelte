<script>
    import {onMount} from "svelte";
    import {LIST_LOAD_ERROR_MSG} from "../../const";
    import {copyToClipboard, formatDate} from "../../utils";
    import {commissionList, recruiterInfo, refCode, user} from "../../stores/store";
    import {Link} from "svelte-navigator";
    import {getRecruiterInfo, getCommissionList} from "../../api/recruiter";
    import UniqueLink from "../../components/UniqueLink.svelte";
    import AlertError from "../../components/AlertError.svelte";

    // Loading / Error State
    let loading = false;
    let listLoadingError = false;
    let errorLoadData = false;

    // Loads List of Commission Data
    function loadCommissionList() {
        if ($commissionList.nextPage) {
            // Triggers Loader
            commissionList.update(data => {
                return {...data, loading: true}
            })
            // Api Call
            getCommissionList($user.token, $commissionList.nextPage)
                // Api Call Success
                .then((res) => {
                    commissionList.set({
                        nextPage: res.data.next ? $commissionList.nextPage + 1 : null,
                        loading: false,
                        results: [...$commissionList.results, ...res.data.results],
                    })
                    listLoadingError = false;
                })
                // Api Call Error
                .catch((e) => {
                    commissionList.update(data => {
                        return {...data, loading: false}
                    })
                    listLoadingError = true;
                })
        }
    }


    // Load Recruiter Info
    function loadRecruiterInfo() {
        // Update Loading State
        recruiterInfo.update(data => {
            return {
                ...data,
                loading: true
            }
        })
        // Call Api
        getRecruiterInfo($user.token)
            // Success
            .then((res) => {
                recruiterInfo.set(
                    {
                        ...$recruiterInfo,
                        ...res.data,
                        loading: false
                    }
                )
                errorLoadData = false;
            })
            // Update
            .catch((e) => {
                recruiterInfo.update(data => {
                    return {
                        ...data,
                        loading: false
                    }
                })
                errorLoadData = true;
            })
    }

    onMount(function () {
        loadCommissionList()
        loadRecruiterInfo()
    });

    let isCopiedToClipboard = false;

    function copyRefCode() {
        copyToClipboard($refCode.code, () => {
            isCopiedToClipboard = true
        })
    }

</script>


<section>
    <section class="container">

        <UniqueLink/>
        {#if errorLoadData}
            <AlertError msg={LIST_LOAD_ERROR_MSG}/>
        {/if}
        <div class="row">
            <div class="col-md-6">
                <div class="jumbotron text-center bg-white">
                    <div class="row">
                        <div class="col-md-4">
                            <svg viewBox="0 0 24 24" style="color: #007bff;width: 85px;height: 85px;"
                                 stroke="currentColor" stroke-width="2"
                                 fill="none" stroke-linecap="round" stroke-linejoin="round" class="css-i6dzq1">
                                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                                <circle cx="9" cy="7" r="4"></circle>
                                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                            </svg>
                        </div>
                        <div class="col-md-8">
                            <h4>TOTAL RECRUITED</h4>
                            {#if $recruiterInfo.loading}
                                <div class="d-flex justify-content-center align-items-center mt-3">
                                    <div class="spinner-border">

                                    </div>
                                </div>
                                {:else }
                                {#if $recruiterInfo.total_recruited >= 0 }
                                    <h1>{$recruiterInfo.total_recruited}</h1>
                                    {:else }
                                    0
                                {/if}
                            {/if}
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="jumbotron text-center bg-white">
                    <div class="row">
                        <div class="col-md-4">
                            <svg viewBox="0 0 24 24" style="color: #007bff;width: 85px;height: 85px;"
                                 stroke="currentColor" stroke-width="2"
                                 fill="none" stroke-linecap="round" stroke-linejoin="round" class="css-i6dzq1">
                                <line x1="12" y1="1" x2="12" y2="23"></line>
                                <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
                            </svg>
                        </div>
                        <div class="col-md-8">
                            <h4>TOTAL BONUS EARNED</h4>
                            {#if $recruiterInfo.loading}
                                <div class="d-flex justify-content-center align-items-center mt-3">
                                    <div class="spinner-border">

                                    </div>
                                </div>
                            {:else }
                                {#if $recruiterInfo.bonus >= 0 }
                                    <h1>{$recruiterInfo.bonus}</h1>
                                {:else }
                                    0
                                {/if}
                            {/if}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <h2 class="my-5">Your Bonus List</h2>
        {#if listLoadingError}
            <AlertError msg={LIST_LOAD_ERROR_MSG}/>
        {/if}
        <div class="table-container">
            <table class="table ">
                <thead>
                <tr>
                    <td>ID</td>
                    <td>NAME</td>
                    <td>DATE</td>
                    <td>BONUS EARNED</td>
                    <td>STATUS</td>
                </tr>
                </thead>
                {#if $commissionList.results}
                    <tbody>

                    {#each $commissionList.results as {id, commission, recruit, time_stamp, completed}, j}
                        <tr>
                            <td>
                                {id}
                            </td>
                            <td>
                                {recruit.first_name} {recruit.last_name}
                            </td>
                            <td>
                                {formatDate(time_stamp)}
                            </td>
                            <td>
                                {commission}
                            </td>
                            <td>
                                {#if completed}
                                    <div class="d-flex align-items-center">
                                        <i class="fas fa-check text-success mr-1"></i>
                                        <span>Completed</span>
                                    </div>
                                {:else }
                                    <div class="d-flex align-items-center">
                                        <i class="fas fa-circle mr-1 text-warning"></i>
                                        <span>Awaiting</span>
                                    </div>
                                {/if}

                            </td>
                        </tr>
                    {/each}

                    </tbody>

                {/if}
            </table>
            {#if $commissionList.nextPage > 1}
                <button on:click={loadCommissionList} class="btn btn-outline-theme">
                    Load More
                </button>
            {/if}
        </div>
        {#if $commissionList.loading}
            <div class="w-100 d-flex my-3 justify-content-center align-items-center">
                <span class="spinner-border theme-color"></span>
            </div>
        {/if}
        {#if $commissionList.results.length === 0}
            <div class="d-flex justify-content-center align-items-center my-3">
                <div class="img-container" style="width: 40px; margin-right: 10px">
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
</section>
