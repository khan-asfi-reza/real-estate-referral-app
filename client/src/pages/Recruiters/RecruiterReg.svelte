<script>
    // State
    import {DASHBOARD, tck} from "../../const";
    import {user} from "../../stores/store";
    import {useNavigate} from "svelte-navigator";
    import {capitalize, formatPhoneNumber, passwordValidation} from "../../utils";
    import {usaStates} from "../../assets/usa";
    import {recruiter} from "../../api/recruiter";
    import Cookies from "js-cookie";
    import {emailValidation} from "../../api/emailValidation";

    let navigate = useNavigate();

    let error = null;
    let loading = false;
    let authLoading = false;

    // Input State
    let first_name = "";
    let last_name = "";
    let email = "";
    let phone_number = "";
    let password = "";
    let confirm_password = "";
    let address = "";
    let city = "";
    let state = "";
    let zip = "";
    let checked = false;
    let emailAvailable = true;

    // Validation State
    let firstPageValidation, secondPageValidation, validatePassword
    $: validatePassword = passwordValidation(password, confirm_password)
    $: firstPageValidation = first_name && last_name && email && phone_number && password && confirm_password && checked && validatePassword[0]
    $: secondPageValidation = address && city && state && zip && firstPageValidation;


    let passwordInput;
    let cPasswordInput;

    function __changePassVisibility(passInp){
        if(passInp.type === "password"){
            passInp.type = "text"
        }else{
            passInp.type = "password"
        }
    }

    function changePasswordVisibility(){
        __changePassVisibility(passwordInput)
    }

    function changeCPasswordVisibility(){
        __changePassVisibility(cPasswordInput)
    }

    // Post Method
    function buttonOnClick() {
        if (secondPageValidation) {
            authLoading = true;
            recruiter({
                user: {
                    first_name: first_name,
                    last_name: last_name,
                    email: email,
                    password: password,
                    city: city,
                    state: state,
                    address: address,
                    zip: zip,
                    phone_number: phone_number
                },
            })
                .then(response => {
                    // Set User
                    user.set({user: response.data.data.user, token: response.data.token});
                    authLoading = false;
                    // Set localstorage
                    Cookies.set(tck, response.data.token);
                    // To Home Page
                    navigate(`/${DASHBOARD}`, {replace: true});
                }).catch((err) => {
                authLoading = false;
                error = err.response.data;

            })
        }
    }
    function onEmailChange(e){
        if(e.target.value.includes("@")){
            emailValidation({email: e.target.value})
                .then((res) => {
                    emailAvailable = res.data.msg === 1
                })
                .catch((e) => {
                    emailAvailable = false;
                })
        }
    }


    // Current Page
    let current = 0;

    // Change to next page
    function moveToNextPage() {
        if (firstPageValidation) {
            current = current === 0 ? current + 1 : current
        }
    }

    // Go To prev page
    function moveToBackPage() {
        current = current ? current - 1 : current
    }

    function phoneNumberOnChange(e){
        e.target.value = formatPhoneNumber(e.target.value)
        phone_number = e.target.value
    }


</script>
<main class="">

    <header class="navbar theme-bg-dark navbar-light">
        <div class="container d-flex justify-content-center align-items-center">
            <div class="img-container">
                <img src="/referral_static/images/logo.svg" alt="">
            </div>
        </div>
    </header>
    <section class="dashboard-bg h-100vh rec-reg">
        <div class="container py-5">
            <div class="text-center">
                <small>Shore Capital Corporation</small>
                <h4 class="mb-4">Recruiter Registration</h4>
            </div>

            {#if error && Object.keys(error).length}
                <div class="alert alert-danger my-4" role="alert">
                    {#each Object.keys(error) as err, i}
                        <div class="my-2">
                            {capitalize(err)} {error[err]}
                        </div>
                    {/each}
                </div>
            {/if}

            <div class="jumbotron bg-white form-box m-auto">
                {#if current === 0}
                    <div id="content-0">
                        <h4 class="mb-5 text-center">Enter your information</h4>
                        <div class="d-grid grid-auto-row-minmax input-box grid-row-gap-40 mt-5">
                            <div class="reg-form-input">
                                <label class="theme-sm-dark-color" for="first_name">Your First Name*</label>
                                <input bind:value={first_name}  required id="first_name" type="text">
                            </div>
                            <div class="reg-form-input">
                                <label class="theme-sm-dark-color" for="last_name">Yout Last Name*</label>
                                <input bind:value={last_name}  required id="last_name" type="text">
                            </div>
                        </div>

                        <div class="input-box mt-4">
                            <div class="reg-form-input">
                                <label class="theme-sm-dark-color" for="phonenumber">Phone Number*</label>
                                <input on:keypress={phoneNumberOnChange}  required id="phonenumber"
                                       type="text">
                            </div>
                        </div>


                        <div class="input-box mt-4">
                            <div class="reg-form-input">
                                <label class="theme-sm-dark-color" for="email">Email Address*</label>
                                <input bind:value={email} on:keyup={onEmailChange}  required id="email" type="text">
                            </div>
                        </div>
                        {#if !emailAvailable}
                            <div>
                                <p class="text-danger mb-0 p-0">Email is already used</p>
                            </div>
                        {/if}

                        <div class="d-grid grid-auto-row-minmax input-box mt-4">
                            <div class="reg-form-input">
                                <label class="theme-sm-dark-color" for="password">Password</label>
                                <input bind:this={passwordInput} bind:value={password} required
                                       id="password" type="password">
                                {#if passwordInput && passwordInput.type === "password"}
                                    <button on:click={changePasswordVisibility} class="password-visible color-off-white"><i class="fas fa-eye"></i></button>
                                {:else}
                                    <button on:click={changePasswordVisibility} class="password-visible color-off-white"><i class="fas fa-eye-slash"></i></button>
                                {/if}
                            </div>
                            <div class="reg-form-input password-input">
                                <label class="theme-sm-dark-color" for="cpasswprd">Confirm Password</label>
                                <input bind:this={cPasswordInput} bind:value={confirm_password} required
                                       id="cpasswprd" type="password">
                                {#if cPasswordInput && cPasswordInput.type === "password"}
                                    <button on:click={changeCPasswordVisibility} class="password-visible color-off-white"><i class="fas fa-eye"></i></button>
                                {:else}
                                    <button on:click={changeCPasswordVisibility} class="password-visible color-off-white"><i class="fas fa-eye-slash"></i></button>
                                {/if}
                            </div>
                        </div>
                        {#if !validatePassword[0] && validatePassword[1] !== "INVALID"}
                            <div>
                                <p class="text-danger mb-0 p-0">{validatePassword[1]}</p>
                            </div>
                        {/if}

                        <div class="w-100 mt-4">
                            <div class="d-flex align-items-center mt-4">
                                <label class="checkbox-container mr-3">
                                    <input type="checkbox" bind:checked={checked}>
                                    <span class="checkmark"></span>
                                </label>
                                <span class="theme-sm-dark-color">I accept the terms of the INDEPENDENT CONTRACTOR AGREEMENT</span>
                            </div>
                        </div>
                    </div>
                {:else}
                    <div>
                        <div class="d-grid button-top-grid  mb-5">
                            <button on:click={moveToBackPage} class="btn btn-outline-theme w-100 mr-1">
                                <i class="fas fa-arrow-left"></i>
                            </button>
                            <h4 class="text-center">Your Address</h4>
                        </div>
                        <div class="input-box mt-4">
                            <div class="reg-form-input">
                                <label class="theme-sm-dark-color" for="address">Address*</label>
                                <input bind:value={address}  required id="address"
                                       type="text">
                            </div>
                        </div>

                        <div class="input-box mt-4">
                            <div class="reg-form-input">
                                <label class="theme-sm-dark-color" for="city">City*</label>
                                <input bind:value={city}  required id="city" type="text">
                            </div>
                        </div>

                        <div class="d-grid grid-auto-row-minmax input-box grid-row-gap-40 mt-4">
                            <div class="reg-form-input">
                                <label class="theme-sm-dark-color" for="state">State</label>
                                <select id="state" bind:value={state}>
                                    {#each usaStates as state, i}
                                        <option value={state.abbreviation}>{state.name}</option>
                                    {/each}
                                </select>
                            </div>
                            <div class="reg-form-input">
                                <label class="theme-sm-dark-color" for="zipcode">Zip Code</label>
                                <input bind:value={zip}  required id="zipcode" type="text">
                            </div>
                        </div>
                    </div>
                {/if}

                <div class="d-flex align-items-center mt-4">
                    <button disabled={current === 0 ? !firstPageValidation : !secondPageValidation}
                            on:click={current === 0? moveToNextPage : buttonOnClick} class="btn btn-theme w-100">
                        {#if authLoading}
                            <div class="spinner-border">
                            </div>
                        {:else}
                            {current === 0 ? "Next" : "Signup"}
                        {/if}
                    </button>
                </div>
            </div>
        </div>
    </section>
</main>