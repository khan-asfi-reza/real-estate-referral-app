<script>
    import FlowChart from "../components/FlowChart.svelte";
    import InvitationBox from "../components/InvitationBox.svelte";
    import {Link} from "svelte-navigator";
    import {LOGIN, RECRUITER_REG, DASHBOARD} from "../const";
    import {user} from "../stores/store";
    const reviewPersonImage = ["/referral_static/images/p1.png", "/referral_static/images/p2.png", "/referral_static/images/p3.png", "/referral_static/images/p4.png"]

</script>
<main class="landing">
    <header class="landing-header container">
        <div class="image-container">
            <img src="/referral_static/images/logo.svg" alt="">
        </div>
        <div class="btn-container mob-nav">
            {#if $user.token}
                <Link to={`/${DASHBOARD}`} class="btn btn-outline-light">Dashboard</Link>
            {:else }
                <Link to={`/${LOGIN}`} class="btn text-light">Login</Link>
                <Link to={`/${RECRUITER_REG}`}  class="btn btn-outline-light">Register</Link>
            {/if}
        </div>
    </header>
    <section class="top-section">
        <div class="layer"></div>
        <div  class="top-section-text color-white container">
            <h1 data-aos="fade" class="my-2">
                Shore Capital <br>
                Recruiting Program
            </h1>
            <p data-aos="fade" class="my-2 animate__animated animate__fadeInUp ">
                Recruiting Your Realtor Friends & Earn Thousands
            </p>

            <Link data-aos="fade" to={RECRUITER_REG} class="btn btn-theme">GET STARTED</Link>

        </div>
        <div class="bottom-wave">

        </div>
    </section>

    <FlowChart/>

    <section class="invitation">
        <div class="layer"></div>
        <div class="container position-absolute inv-inner">
            <InvitationBox/>
        </div>
        <div class="top-wave">

        </div>
    </section>

    <section class="container mt-5 d-grid review">
        <div data-aos="slide-right" class="review-image">
            {#each reviewPersonImage as img, i}
                <div class="image-container i-{i}">
                    <div class="img-container">
                        <img src="{img}" alt="Person {i}">
                    </div>
                </div>
            {/each}
        </div>
        <div class="header">
            <h2>Realtor Reviews</h2>
        </div>
        <div data-aos="slide-left" class="review-text">
            <div class="mt-3">
                <div class="quotes-grid">
                    <div class="img-container">
                        <img src="/referral_static/images/quote.svg" alt="">
                    </div>
                    <h3>Elizabeth Howell</h3>
                    <p>Shore Capital uses up-to-date technology to for the administrative back end processes. Everything is online and clearly set up to run a loan or Real Estate transaction through from start to finish. They also have live help available if I have any question. It enables me to focus on my customers to provide efficient services.</p>
                </div>
                <div class="quotes-grid">
                    <div class="img-container">
                        <img src="/referral_static/images/quote.svg" alt="">
                    </div>
                    <h3>Alex Benjamin</h3>
                    <p>Shore Capital is the best company I have ever seen, I have been in touch with them for a long time, for me they are the best, The service is top notch and their system if up to date, Whenever I faced any problem with the system they helped me quickly, I love Shore Capital</p>
                </div>
                <div class="quotes-grid">
                    <div class="img-container">
                        <img src="/referral_static/images/quote.svg" alt="">
                    </div>
                    <h3>Howard Ken</h3>
                    <p>Shore Capital Provides top notch service, I highly recommend them, because of their great system. Their web app is very polished, makes me use their application a lot. Also their service is the best. Shore Capital Corporation is the best Real Estate Company!</p>
                </div>
            </div>
        </div>
    </section>

    <footer class="theme-bg-dark mt-4">
        <div class="container d-grid footer-container">
            <div class="container-grid-1">
                <div class="img-container">
                    <img src="/referral_static/images/logo.svg" alt="">
                </div>
                <p class="text-white my-3">
                    Recruits cannot be changed or applied to a Recruiter after the Real Estate Agent joins the Company
                </p>
                <p class="text-white my-3">
                    *Qualified transactions consist of sales transactions where a full broker fee of $635 is paid.
                </p>
                <p class="text-white my-3">Note: Recruiting bonus is not eligible when recruiting a spouse.</p>
            </div>
            <div class="justify-self-end container-grid-2">
                <h4 class="mb-4 text-white">CONTACT</h4>
                <p class="text-white">
                    <i class="fa fa-map theme-color mr-2"></i>
                    9114 Adams Ave #165
                    Huntington Beach, CA 92646
                </p>
                <p class="text-white">
                    <i class="fa fa-phone theme-color mr-2"></i>
                    714-662-2704
                </p>
            </div>
            <div class="container-grid-3">
                <h4 class="mb-4 text-white">FOLLOW US</h4>
                <div class="my-3 d-flex s-icons ">
                    <a href="https://www.facebook.com" class="sm-link circle mr-3"><i class="fab fa-twitter text-white"></i></a>
                    <a href="https://www.facebook.com" class="sm-link circle mr-3"><i class="fab fa-facebook text-white"></i></a>
                    <a href="https://www.facebook.com" class="sm-link circle mr-3"><i class="fab fa-instagram text-white"></i></a>
                </div>
            </div>
            <div class="container-grid-4">
                <small class="text-white">@2020 Shore Capital Corporation | All right reserved</small>
            </div>
        </div>
    </footer>
</main>