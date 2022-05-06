<script>
    import {onMount} from "svelte";
    import {Route, Router} from "svelte-navigator";
    import AuthRoute from "./hoc/AuthRoute.svelte";
    import PrivateRoute from "./hoc/PrivateRoute.svelte";

    import '/public/referral_static/css/aos.css';

    import Cookies from "js-cookie";
    import {
        LOGIN,
        RECRUIT_REG,
        RECRUITER_REG,
        HOME_PAGE,
        DASHBOARD,
        ABOUT,
        LOGIN_URL,
        MY_ACCOUNT,
        tck,
        RECRUITERS_REFERRAL_ROUTE,
        FORGET_PASSWORD,
        RESET_PASSWORD, PROD, INIT
    } from "./const";
    import {authLoading, refCode, user} from "./stores/store";
    import Dashboard from "./pages/Dashboard.svelte";
    import Login from "./pages/Login.svelte";
    import About from "./pages/About.svelte";
    import Home from "./pages/Home.svelte";
    import RecruitReg from "./pages/Recruits/RecruitReg.svelte";
    import RecruiterReg from "./pages/Recruiters/RecruiterReg.svelte";
    import axios from "axios";
    import {getHeaders} from "./utils";
    import ChangeAccount from "./pages/Account/Account.svelte";
    import {getRefCode} from "./api/recruiter";
    import RecruiterOnlyRoute from "./hoc/RecruiterOnlyRoute.svelte";
    import RecruiterReferral from "./pages/Recruiters/RecruiterReferral.svelte";
    import SendEmail from "./pages/ResetPassword/SendEmail.svelte";
    import ResetPassword from "./pages/ResetPassword/ResetPassword.svelte";

    // Loading on auth
    let loading = $authLoading;

    authLoading.subscribe(data => {
        loading = data;
    });

    function setAuthLoading(bool = false) {
        authLoading.set(bool);
    }

    // Loads Ref Code
    function loadRefCode() {
        if ($user.user && $user.user.role === 1) {
            refCode.update(data => {
                return {
                    ...data,
                    loading: true
                }
            })
            getRefCode($user.token)
                .then((res) => {
                    refCode.set({
                        loading: false,
                        error: false,
                        code: res.data.ref_code
                    })
                }).catch((e) => {

            });
        }
    }

    // On Mount Check if token available
    onMount(function () {

        setAuthLoading(true);
        // Grab token from localstorage
        const token = Cookies.get(tck);
        // If token available, get user data
        if (token) {
            axios.get(LOGIN_URL, getHeaders(token))
                .then((res) => {
                    // Set user data
                    user.set(res.data);
                    setAuthLoading(false);
                    loadRefCode()
                }).catch((e) => {
                // Remove token from local storage on error
                Cookies.remove(tck)
                setAuthLoading(false);
            })
        } else {
            setAuthLoading(false);
        }
    });

    $:if ($user.user) {
        loadRefCode()
    }

</script>

{#if $authLoading}
    <div class="w-100 d-flex justify-content-center align-items-center">
        <div class="spinner-border">

        </div>
    </div>
    {:else }
    <Router basepath={"/"}>
        <AuthRoute  path={LOGIN}>
            <Login/>
        </AuthRoute>
        <AuthRoute path={`${RECRUIT_REG}/:ref_code`} let:location>
            <RecruitReg/>
        </AuthRoute>
        <AuthRoute path={RECRUITER_REG}>
            <RecruiterReg/>
        </AuthRoute>
        <AuthRoute path={FORGET_PASSWORD}>
            <SendEmail/>
        </AuthRoute>
        <AuthRoute path={`${RESET_PASSWORD}/:unique_link`} let:location>
            <ResetPassword/>
        </AuthRoute>
        <Route path={HOME_PAGE}>
            <Home/>
        </Route>
        <PrivateRoute path={DASHBOARD}>
            <Dashboard/>
        </PrivateRoute>
        <RecruiterOnlyRoute path={RECRUITERS_REFERRAL_ROUTE}>
            <RecruiterReferral/>
        </RecruiterOnlyRoute>
        <PrivateRoute path={MY_ACCOUNT}>
            <ChangeAccount/>
        </PrivateRoute>
        <PrivateRoute path={ABOUT}>
            <About/>
        </PrivateRoute>
    </Router>
{/if}