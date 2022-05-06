<script>
    import DashboardSidebar from "./DashboardSidebar.svelte";
    import {refCode, user} from "../stores/store";
    import {INVITATION_URL} from "../const";
    import {copyToClipboard} from "../utils";
    // Copy State
    let isCopiedToClipboard = false;
    let modal;

    // Copy to Ref Code
    function copyRefCode(){
        copyToClipboard($refCode.code, ()=>{isCopiedToClipboard=true})
    }

    // Modal Methods
    function modalOpen(){
        modal.style.display = "block";
    }

    function modalClose(){
        modal.style.display = "none";
    }



</script>
<div class="dashboard">
    <DashboardSidebar/>
    <div class="right-panel  dashboard-bg">
        {#if $user.user && $user.user.role === 1}
            <header class="navbar bg-white navbar-light">
                <div class="container d-flex justify-content-between align-items-center">
                    <h4>Recruits</h4>
                    <button on:click={modalOpen} class="btn btn-outline-theme">
                        Your Unique Link
                    </button>
                </div>
            </header>
            <div bind:this={modal} id="myModal" class="modal">
                <div class="modal-content">
                    <div class="d-flex align-items-center justify-content-between mb-3">
                        <h3>Your Recruit Unique Link</h3>
                        <button class="btn close-btn text-danger" on:click={modalClose}>
                            <i class="far fa-times-circle"></i>
                        </button>
                    </div>
                    <div class="input-group mb-3">
                        <input type="text" class="form-control {isCopiedToClipboard ? 'border-success' : 'border-primary'}"
                               aria-label="Recipient's username"
                               aria-describedby="button-addon2"
                               value={`${INVITATION_URL}/${$refCode.code}`}
                        >
                        <div class="input-group-append  ">
                            <button on:click={copyRefCode} class="btn {isCopiedToClipboard ? 'btn-outline-success' : 'btn-outline-primary'}" type="button"
                                    id="button-addon2">
                                <svg viewBox="0 0 24 24" width="24" height="22" stroke="currentColor"
                                     stroke-width="2"
                                     fill="none" stroke-linecap="round" stroke-linejoin="round" class="css-i6dzq1">
                                    <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>
                                    <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        {/if}
        <slot>

        </slot>
    </div>
</div>