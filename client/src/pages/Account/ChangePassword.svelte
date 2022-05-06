<script>
    import {capitalize} from "../../utils";
    import {user} from "../../stores/store";
    import {changePasswordApi} from "../../api/passwordChange";

    // States
    let oldPassword = "";
    let password = "";
    let cPassword = "";
    let passwordSame = true;
    let passwordError = null;
    let passwordSuccess = null;
    let loading = false;

    // Check if password is same
    function checkPasswordSame(e) {
        passwordSame = e.target.value === password;
    }

    // Change Password API
    function changePassword() {
        if (password === cPassword) {
            // Change Password Api Call
            loading = true;
            changePasswordApi({old_password: oldPassword, new_password: password}, $user.token)
                .then((res) => {
                    // Pause Loading
                    loading = false;
                    // Set User
                    user.set({user: $user.user, token: res.data.token});
                    // Token Set
                    localStorage.setItem("token", res.data.token)
                    // State Clear
                    passwordError = null;
                    passwordSuccess = true;
                    oldPassword = "";
                    password = "";
                    cPassword = ""
                }).catch((e) => {
                // Error Phase
                loading = false;
                passwordError = e.response.data;
                passwordSuccess = false;
                oldPassword = "";
                password = "";
                cPassword = ""
            })
        }
    }
</script>


<div class="card bg-white">
    <div class="card-header bg-white">
        <a class="btn w-100" data-bs-toggle="collapse" href="#changePassword" role="button" aria-expanded="false"
           aria-controls="changePassword">
            <div class="d-flex justify-content-between">
                Change Password
            </div>
        </a>
    </div>
    <div class="collapse card-body rec-reg" id="changePassword">
        {#if passwordError}
            <div class="mb-5 mt-3 alert alert-danger">
                {#each Object.keys(passwordError) as err, i}
                    <div class="my-2">
                        {capitalize(err)} {passwordError[err]}
                    </div>
                {/each}
            </div>
        {/if}

        {#if passwordSuccess}
            <div class="alert alert-success alert-dismissible fade show mb-5 mt-3" role="alert">
                <span>Your password has been changed</span>
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        {/if}

        <div class="input-box mt-2">
            <div class="reg-form-input">
                <label class="theme-sm-dark-color" for="oldPassword">Old Password</label>
                <input bind:value={oldPassword} placeholder="Your Old Password" required id="oldPassword"
                       type="password">
            </div>
        </div>

        <div class="input-box mt-4">
            <div class="reg-form-input">
                <label class="theme-sm-dark-color" for="password">New Password</label>
                <input bind:value={password} placeholder="Your New Password" required id="password" type="password">
            </div>
        </div>

        <div class="input-box mt-4">
            <div class="reg-form-input">
                <label class="theme-sm-dark-color" for="cPassword">Confirm Password</label>
                <input on:change={checkPasswordSame} bind:value={cPassword} placeholder="Type again to confirm password"
                       required id="cPassword" type="password">
            </div>
        </div>

        {#if password !== cPassword && !passwordSame}
            <div class="my-2">
                <p class="text-danger">Passwords are not same</p>
            </div>
        {/if}
        <div class="mt-3 mb-2">
            <button on:click={changePassword} class="btn btn-theme">
                {#if loading}
                    <div class="spinner-border">

                    </div>
                {:else}
                    Change Password
                {/if}
            </button>
        </div>
    </div>
</div>