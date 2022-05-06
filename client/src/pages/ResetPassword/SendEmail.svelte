<script>
    import AuthContainer from "../../components/AuthContainer.svelte";
    import {forgetPasswordSendEmailApi} from "../../api/forgetPassword";
    import ErrorBox from "../../components/ErrorBox.svelte";

    let email = ""
    let msg = null;
    let error = null;
    let loading = false;

    function sendEmail() {
        loading = true;
        forgetPasswordSendEmailApi(email)
            .then((res) => {
                msg = res.data.text
                loading = false;
            }).catch((e) => {
            error = e.response.data;
            loading = false;
        })
    }
</script>
<AuthContainer>
    <h4 class="text-light mb-3 text-center">Forget Password</h4>
    <p class="text-light text-center">An email will be sent to your email, where you will get a password reset link</p>
    {#if error}
        {#if error.msg === 0}
            <div class="alert alert-danger my-4 form-box mx-auto" role="alert">
                <p class="p-0 m-0">Maximum possible email sent, please try again after some time</p>
            </div>
        {:else }
            <ErrorBox error={error}/>
        {/if}
    {/if}
    {#if msg}
        <div class="alert alert-success my-4 form-box mx-auto" role="alert">
            <p class="p-0 m-0">{msg}</p>
        </div>
    {/if}
    <div class="input-box">
        <div class="input-field mt-5">
            <input bind:value={email}  required id="email" class="" type="text">
            <label class="text-white" for="email"><i class="fa fa-envelope mr-2"></i>Email</label>
        </div>
    </div>
    <button on:click={sendEmail} disabled="{email.length === 0 || (error && error.msg === 0) || msg}" class="btn btn-theme mt-5 w-100">
        {#if loading}
            <div class="spinner-border" role="status"></div>
        {:else}
            Send Email
        {/if}
    </button>
</AuthContainer>