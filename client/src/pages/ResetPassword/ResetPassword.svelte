<script>
    import AuthContainer from "../../components/AuthContainer.svelte";
    import {resetPasswordApi, validatePasswordReset} from "../../api/forgetPassword";
    import ErrorBox from "../../components/ErrorBox.svelte";
    import {useLocation, useNavigate, useParams} from "svelte-navigator";
    import {HOME_PAGE, LOGIN} from "../../const";
    import {passwordValidation} from "../../utils";
    import {onMount} from "svelte";

    const navigate = useNavigate();
    const location = useLocation();
    let params = useParams();
    let unique_link = $params.unique_link;

    let email = ""
    let password = ""
    let cPassword = ""
    let msg = null;
    let error = null;
    let loading = false;
    let passwordValidate;
    let authLoading = false;

    $:passwordValidate = passwordValidation(password, cPassword)

    function validateUniqueLink(){
        validatePasswordReset(unique_link)
            .then((res) => {
                if(res.data.msg !== 1){
                    navigate(HOME_PAGE, {replace: true})
                }
            })
            .catch((e) => {
                navigate(HOME_PAGE, {replace: true})
            })
    }


    function resetPassword() {
        if(!msg){
            loading = true;
            resetPasswordApi({
                email: email,
                password: password,
                unique_link: unique_link
            })
                .then((res) => {
                    console.log(res.data)
                    msg = res.data.text
                    loading = false;
                    setTimeout(()=>{
                        navigate(`/${LOGIN}`)
                    }, 5000)
                }).catch((e) => {
                error = e.response.data;
                loading = false;
            })
        }
    }

    onMount(()=>{
        validateUniqueLink()
    })

</script>
{#if authLoading}
    <div class="w-100 d-flex justify-content-center align-items-center">
        <div class="spinner-border" role="status"></div>
    </div>
{:else}
    <AuthContainer>
        <h4 class="text-light mb-3 text-center">Reset your password</h4>
        <p class="text-light text-center">Enter your email and new password to reset</p>
        {#if error}
            {#if error.msg === 0}
                <div class="alert alert-danger my-4 form-box mx-auto" role="alert">
                    <p class="p-0 m-0">{error.text}</p>
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
            <div class="input-field mt-5">
                <input bind:value={password} id="password" required class="" type="password">
                <label class="text-white" for="password"><i class="fas fa-lock mr-2"></i>Password</label>
            </div>
            <div class="input-field mt-5">
                <input bind:value={cPassword} id="cpassword" required class="" type="password">
                <label class="text-white" for="cpassword"><i class="fas fa-lock mr-2"></i>Confirm Password</label>
            </div>
            {#if !passwordValidate[0] && passwordValidate[1] !== "INVALID"}
                <p class="text-danger">{passwordValidate[1]}</p>
            {/if}
        </div>
        <button on:click={resetPassword} disabled="{email.length === 0 || (error && error.msg === 0) || msg || !passwordValidate[0]}" class="btn btn-theme mt-5 w-100">
            {#if loading}
                <div class="spinner-border" role="status"></div>
            {:else}
                Reset Password
            {/if}
        </button>
    </AuthContainer>
{/if}
