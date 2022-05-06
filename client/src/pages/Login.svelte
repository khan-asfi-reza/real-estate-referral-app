<script>
    import {useNavigate, useLocation, Link} from "svelte-navigator";
    import {user} from "../stores/store";
    import {RECRUITER_REG, tck, FORGET_PASSWORD} from "../const";
    import {getFrom} from "../utils";
    import {loginApi} from "../api/login";

    const navigate = useNavigate();
    const location = useLocation();
    import Cookies from "js-cookie";
    import AuthContainer from "../components/AuthContainer.svelte";
    import ErrorBox from "../components/ErrorBox.svelte";

    // State
    let email = "";
    let password = "";
    let error;
    let loading;
    let checked = false;
    let passwordInput;

    function changePasswordVisibility(){
        if(passwordInput.type === "password"){
            passwordInput.type = "text"
        }else{
            passwordInput.type = "password"
        }
    }


    // Authenticate User
    async function authenticate() {
        // Loading set to true
        loading = true;
        // Login with cred
        loginApi(email, password)
            .then((res) => {
                // Set User Credentials
                user.set(res.data);
                loading = false;
                // Set localstorage
                if (checked) {
                    Cookies.set(tck, res.data.token, {expires: 365});
                } else {
                    Cookies.set(tck, res.data.token);
                }
                // To Home Page
                navigate(getFrom($location), {replace: true});
            }).catch((e) => {
            loading = false;
            try {
                error = e.response.data;
            } catch (e) {
                error = ""
            }
        })
    }


</script>

<AuthContainer>
    <ErrorBox error={error}/>

    <div class="input-box">
        <div class="input-field mt-5">
            <input bind:value={email}  required id="email" class="" type="text">
            <label class="text-white" for="email"><i class="fa fa-envelope mr-2"></i>Email</label>
        </div>
        <div class="input-field mt-5 password-input">
            <input bind:this={passwordInput} bind:value={password} required id="password" class="" type="password">
            <label class="text-white" for="password"><i class="fas fa-lock mr-2"></i>Password</label>
            {#if passwordInput && passwordInput.type === "password"}
                <button on:click={changePasswordVisibility} class="password-visible color-off-white"><i class="fas fa-eye"></i></button>
                {:else}
                <button on:click={changePasswordVisibility} class="password-visible color-off-white"><i class="fas fa-eye-slash"></i></button>
            {/if}
        </div>
    </div>

    <div class="mt-5 d-flex other-inp-box">
        <div class="d-flex align-items-center">
            <label class="checkbox-container mr-3">
                <input type="checkbox" bind:checked={checked}>
                <span class="checkmark"></span>
            </label>
            <span class="text-white">Remember Me</span>
        </div>
        <span class="text-white mx-3">|</span>
        <Link to={`/${FORGET_PASSWORD}`} class="text-white text-decoration-none">Forgot Password ></Link>
    </div>
    <button on:click={authenticate} class="btn btn-theme mt-5 w-100">
        {#if loading}
            <div class="spinner-border" role="status"></div>
        {:else}
            LOGIN
        {/if}
    </button>
    <div class="mt-5 d-flex align-items-center">
        <small class="text-white mr-2">If you are a recruiter, click to register</small>
        <Link to={`/${RECRUITER_REG}`} type="button" class="btn btn-outline-light">
            CREATE AN ACCOUNT
        </Link>
    </div>
</AuthContainer>
