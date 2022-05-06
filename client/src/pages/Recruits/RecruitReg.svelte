<script>
    import {useLocation, useNavigate, useParams} from "svelte-navigator";
    import {onMount} from "svelte";
    import {capitalize, formatPhoneNumber, passwordValidation} from "../../utils";
    import {DASHBOARD, tck} from "../../const";
    import {user} from "../../stores/store"
    import {recruitCreate, refCodeGet} from "../../api/recruit";
    import {usaStates} from "../../assets/usa";
    import {emailValidation} from "../../api/emailValidation";
    import Cookies from "js-cookie";

    const navigate = useNavigate();
    const location = useLocation();
    let params = useParams();
    let ref_code = $params.ref_code;

    // State
    let recruiter = {
      full_name: "",
      email: ""
    };

    let error = null;
    let loading = false;
    let authLoading = false;

    // Input State
    let first_name = "";
    let last_name = "";
    let email = "";
    let phone_number = "";
    let dre_license = "";
    let nmls_number = "";
    let ca = false;
    let association = "";
    let password = "";
    let confirm_password = "";
    let address = "";
    let city = "";
    let state = "";
    let zip = "";
    let checked = false;
    let emailAvailable = true;

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

    let firstPageValidation, secondPageValidation, validatePassword
    $: validatePassword = passwordValidation(password, confirm_password)
    $: firstPageValidation = first_name && last_name && email && phone_number && password && confirm_password && checked && validatePassword[0] && emailAvailable
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

    onMount(() => {
        loading = true;
        refCodeGet({
            ref_code: ref_code
        }).then(res => {
            recruiter = res.data;
            loading = false;
        })
            .catch(e => {
                error = e.response.data;
                loading = false;
                // navigate("/",)
            })
    });

    // API
    function buttonOnClick() {
        authLoading = true;
        recruitCreate({
            ref_code: ref_code,
            user: {
                first_name: first_name,
                last_name: last_name,
                email: email,
                password: password,
                phone_number: phone_number,
                role: 2,
                city: city,
                state: state,
                zip: zip,
                address: address
            },
            nmls_number: nmls_number,
            cba_licence: ca,
            association: association,
            dre_license: dre_license
        }).then(response => {
            // Set Store
            user.set({user: response.data.data.user, token: response.data.token});
            authLoading = false;
            // Set localstorage
            Cookies.set(tck, response.data.token);
            // To Home Page
            navigate(`/${DASHBOARD}`, {replace: true});
        }).catch((error) => {
            authLoading = false;
            try {
                error = error.response.data.error;
            } catch (error) {
                error = ""
            }
        })
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
    <section class="dashboard-bg  rec-reg">
        <div class="container py-5">
            <div class="text-center">
                <small>Shore Capital Corporation</small>
                <h4 class="mb-4">Associate License Application</h4>
            </div>

            {#if error && Object.keys(error).length}
                <div class="alert alert-danger my-4 form-box mx-auto" role="alert">
                    {#each Object.keys(error) as err, i}
                        <div class="my-2">
                            {capitalize(err)} {error[err]}
                        </div>
                    {/each}
                </div>
            {/if}

            <div class="jumbotron bg-white form-box mx-auto">
                {#if current === 0}
                    <h4 class="text-center">Enter your information</h4>
                    <div class="d-grid grid-auto-row-minmax input-box grid-row-gap-40 mt-5">
                        <div class="reg-form-input">
                            <label class="theme-sm-dark-color" for="first_name">Your First Name*</label>
                            <input bind:value={first_name} required id="first_name" type="text">
                        </div>
                        <div class="reg-form-input">
                            <label class="theme-sm-dark-color" for="last_name">Your Last Name*</label>
                            <input bind:value={last_name} required id="last_name" type="text">
                        </div>
                    </div>

                    <div class="input-box mt-4">
                        <div class="reg-form-input">
                            <label class="theme-sm-dark-color" for="phonenumber">Phone Number*</label>
                            <input  on:keypress={phoneNumberOnChange} bind:value={phone_number} required id="phonenumber"
                                   type="text">
                        </div>
                    </div>

                    <div class="input-box mt-4">
                        <div class="reg-form-input">
                            <label class="theme-sm-dark-color" for="email">Email Address*</label>
                            <input bind:value={email} on:change={onEmailChange} required id="email" type="text">
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
                    <div class="d-grid grid-auto-row-minmax input-box grid-row-gap-40 mt-4">
                        <div class="reg-form-input">
                            <label class="theme-sm-dark-color" for="dre_license">DRE License Number</label>
                            <input bind:value={dre_license} required
                                   id="dre_license" type="text">
                        </div>
                        <div class="reg-form-input">
                            <label class="theme-sm-dark-color" for="nmls_license">NMLS License Number</label>
                            <input bind:value={nmls_number} required id="nmls_license"
                                   type="text">
                        </div>
                    </div>

                    <div class="d-flex align-items-center mt-4">
                        <label class="checkbox-container mr-3">
                            <input bind:checked={ca} type="checkbox">
                            <span class="checkmark"></span>
                        </label>
                        <span class="theme-sm-dark-color">Check if you have a CBA license</span>
                    </div>

                    <div class="input-box mt-4">
                        <div class="reg-form-input">
                            <label class="theme-sm-dark-color" for="referred_by">Referred By</label>
                            <input value={recruiter ? recruiter.full_name.length > 2 ? recruiter.full_name : recruiter.email : ""}
                                   readonly required id="referred_by" type="text">
                        </div>
                    </div>


                    <div class="input-box mt-4">
                        <div class="reg-form-input">
                            <label class="theme-sm-dark-color" for="association">Association</label>
                            <input bind:value={association} required id="association"
                                   type="text">
                        </div>
                    </div>

                    <div class="w-100 mt-4">
                        <div class="d-flex align-items-center mt-4">
                            <label class="checkbox-container mr-3">
                                <input type="checkbox" bind:checked={checked}>
                                <span class="checkmark"></span>
                            </label>
                            <span class="theme-sm-dark-color">I accept the terms of the INDEPENDENT CONTRACTOR AGREEMENT</span>
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
                                <input bind:value={address} required id="address"
                                       type="text">
                            </div>
                        </div>

                        <div class="input-box mt-4">
                            <div class="reg-form-input">
                                <label class="theme-sm-dark-color" for="city">City*</label>
                                <input bind:value={city} required id="city" type="text">
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
                                <input bind:value={zip} required id="zipcode" type="text">
                            </div>
                        </div>
                    </div>
                {/if}

                <button disabled={current === 0 ? !firstPageValidation : !secondPageValidation}
                        on:click={current === 0? moveToNextPage : buttonOnClick} class="btn btn-theme w-100 mt-4">
                    {#if authLoading}
                        <div class="spinner-border">
                        </div>
                    {:else}
                        {current === 0 ? "Next" : "Join Now"}
                    {/if}
                </button>

            </div>
        </div>
    </section>
</main>
