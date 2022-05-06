<script>
    import {user} from "../../stores/store";
    import {capitalize} from "../../utils";
    import {usaStates} from "../../assets/usa";
    import {accountUpdateApi} from "../../api/accountUpdate";


    // User State from User Store
    let userInfo = $user.user;
    let token = $user.token;

    // Triggers user data local state update on User Store Change
    user.subscribe(data => {
        userInfo = data.user;
        token = data.token;
    })

    // Local State
    let authLoading = false;
    let error = null;
    let success = false;

    // Button On Click
    function buttonOnClick() {
        // Set Auth Loading
        authLoading = true;
        // Send Api Post Request
        accountUpdateApi({
            first_name: userInfo.first_name,
            last_name: userInfo.last_name,
            phone_number: userInfo.phone_number,
            address: userInfo.address,
            city: userInfo.city,
            state: userInfo.state,
            zip: userInfo.zip,
        }, token)
        // Success
        .then(res => {
            success = true;
            error = null;
            authLoading = false;
            user.set({token: token, user: res.data})
        }).catch(e => {
            authLoading = false;
            error = e.response.data;
        })
    }


</script>


<div class="card bg-white mt-3">
    <div class="card-header bg-white">
        <a class="btn w-100" data-bs-toggle="collapse" href="#changeAccount" role="button" aria-expanded="false"
           aria-controls="changePassword">
            <div class="d-flex justify-content-between">
                Change Account
            </div>
        </a>
    </div>
    <div class="collapse card-body rec-reg" id="changeAccount">
        {#if error}
            <div class="mb-5 mt-3 alert alert-danger">
                {#each Object.keys(error) as err, i}
                    <div class="my-2">
                        {capitalize(err)} {error[err]}
                    </div>
                {/each}
            </div>
        {/if}
        {#if success}
            <div class="alert alert-success alert-dismissible fade show mb-5 mt-3" role="alert">
                <span>Your account has been updated</span>
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        {/if}
        <div class="d-grid grid-auto-row-minmax input-box grid-row-gap-40 mt-2">
            <div class="reg-form-input">
                <label class="theme-sm-dark-color" for="first_name">Your First Name*</label>
                <input bind:value={userInfo.first_name} placeholder="John" required id="first_name" type="text">
            </div>
            <div class="reg-form-input">
                <label class="theme-sm-dark-color" for="last_name">Yout Last Name*</label>
                <input bind:value={userInfo.last_name} placeholder="Smith" required id="last_name" type="text">
            </div>
        </div>

        <div class="input-box mt-4">
            <div class="reg-form-input">
                <label class="theme-sm-dark-color" for="phonenumber">Phone Number*</label>
                <input bind:value={userInfo.phone_number} placeholder="123 456 789" required id="phonenumber" type="text">
            </div>
        </div>


        <div class="input-box mt-4">
            <div class="reg-form-input">
                <label class="theme-sm-dark-color" for="address">Address*</label>
                <input bind:value={userInfo.address} placeholder="Your Address Here" required id="address" type="text">
            </div>
        </div>

        <div class="input-box mt-4">
            <div class="reg-form-input">
                <label class="theme-sm-dark-color" for="city">City*</label>
                <input bind:value={userInfo.city} placeholder="Your City" required id="city" type="text">
            </div>
        </div>

        <div class="d-grid grid-auto-row-minmax input-box grid-row-gap-40 mt-4">
            <div class="reg-form-input">
                <label class="theme-sm-dark-color" for="state">State</label>
                <select id="state" bind:value={userInfo.state}>
                    {#each usaStates as state, i}
                        <option value={state.abbreviation}>{state.name}</option>
                    {/each}
                </select>
            </div>
            <div class="reg-form-input">
                <label class="theme-sm-dark-color" for="zipcode">Zip Code</label>
                <input bind:value={userInfo.zip} placeholder="Your Zip Code" required id="zipcode" type="text">
            </div>
        </div>


        <button on:click={buttonOnClick} class="btn btn-theme mt-4">
            {#if authLoading}
                <div class="spinner-border">

                </div>
            {:else}
                Update Account
            {/if}
        </button>
    </div>
</div>