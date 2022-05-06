<script>
    import {Link, useNavigate} from "svelte-navigator";
    import {user} from "../stores/store"
    import {DASHBOARD, ABOUT, MY_ACCOUNT, tck, RECRUITERS_REFERRAL_ROUTE} from "../const";
    import Cookies from "js-cookie"
    let navigate = useNavigate();

    function logout() {
        user.set({user:null, token: null});
        Cookies.remove(tck)
        navigate("/login/");
    }

    let leftPanelOn = true;

    function navFunction(){
        leftPanelOn = !leftPanelOn;
    }


</script>
<div class="">
    <button on:click={navFunction} id="expandButton2" class="hidden-expand-button btn">
        <i class="fa fa-bars"></i>
    </button>
</div>

<aside id="left-panel" class="left-panel d-flex flex-column {leftPanelOn ? '' : 'nav-off'}">
    <div class="d-flex justify-content-center head">
        <div class="img-container w-75">
            <img src="/referral_static/images/logo.svg" alt="Shore Capital Corporation">
        </div>
    </div>
    <div class="divider-border mt-3">  </div>
    <nav class="flex-1 d-flex w-75 m-auto">
        <div class="flex-1 d-flex flex-column">
            <ul class="d-flex flex-column flex-1 list-style-none p-0 ">
                <li class="nav-item mt-3 d-flex align-items-center justify-content-end">
                    <Link to={`/${DASHBOARD}`}>
                        <span class="nav-text text-white">Dashboard </span>
                    </Link>
                    <i class="ml-3 fas fa-columns text-white"></i>
                </li>
                {#if $user.user && $user.user.role === 1}
                    <li class="nav-item mt-3 d-flex align-items-center justify-content-end">
                        <Link to={`/${RECRUITERS_REFERRAL_ROUTE}`}>
                            <span class="nav-text text-white">My Recruits</span>
                        </Link>
                        <i class="ml-3 fa fa-users text-white" aria-hidden="true"></i>
                    </li>
                {/if}
                <li class="nav-item mt-3 d-flex align-items-center justify-content-end">
                    <Link to={`/${MY_ACCOUNT}`}>
                        <span class="nav-text text-white">My Account</span>
                    </Link>
                    <i class="ml-3 fas fa-user text-white"></i>
                </li>
                <li class="nav-item mt-3 d-flex align-items-center justify-content-end">
                    <Link to={`/${ABOUT}`}>
                        <span class="nav-text text-white">About The Program </span>
                    </Link>
                    <i class="ml-3 fas fa-question-circle text-white"></i>
                </li>
            </ul>
            <ul class="mt-5 d-flex flex-column list-style-none p-0">
                <li class="nav-item ">
                    <button class="btn  text-white" on:click={logout}>Logout <i class="ml-3 fas fa-sign-out-alt"></i></button>
                </li>
            </ul>
        </div>
    </nav>
</aside>