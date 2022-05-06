<script>
    import {copyToClipboard} from "../utils";
    import {refCode} from "../stores/store";
    import {INVITATION_URL, REF_CODE_ERROR_MSG} from "../const";
    import AlertError from "./AlertError.svelte";

    let isCopiedToClipboard = false;

    // Copy to Ref Code
    function copyRefCode() {
        copyToClipboard($refCode.code, () => {
            isCopiedToClipboard = true
        })
    }


</script>

{#if $refCode.error}
    <AlertError msg={REF_CODE_ERROR_MSG}/>
{/if}
<div class="d-flex flex-column flex-md-row justify-content-md-between my-3">
    <div class="col-md-6">
        <h5 class="pt-2">YOUR UNIQUE RECRUITING LINK</h5>
    </div>
    {#if $refCode.loading}
        <div class="spinner-border text-primary mt-md-0 mt-2" role="status">
            <span class="sr-only">Loading...</span>
        </div>
    {:else}
        <div class="col-md-6 mt-md-0 mt-2">
            <div class="input-group mb-3">
                <input type="text"
                       class="form-control {isCopiedToClipboard ? 'border-success' : 'border-primary'}"
                       aria-label="Recipient's username"
                       aria-describedby="button-addon2"
                       value={`${INVITATION_URL}/${$refCode.code}`}
                >
                <div class="input-group-append  ">
                    <button on:click={copyRefCode}
                            class="btn {isCopiedToClipboard ? 'btn-outline-success' : 'btn-outline-primary'}"
                            type="button"
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
    {/if}
</div>