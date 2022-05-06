<script>
    import Dashboard from "../components/Base.svelte";
    import FlowChart from "../components/FlowChart.svelte";
    import InvitationBox from "../components/InvitationBox.svelte";
    import Splide from "@splidejs/splide";
    import {onMount} from "svelte";

    onMount(()=>{
        new Splide( '.splide' ).mount();
    })

</script>


<Dashboard>
    <section class="container">
        <div class="text-center">
            <p>Shore Capital Corporation</p>
            <h2>Recruiting Program</h2>
        </div>

        <div class="d-grid my-5 grid-auto-row-minmax">
            <div class="jumbotron bg-white d-flex align-items-center">
                <div class="img-container w-50 mr-3">
                    <img src="/referral_static/images/money.png" alt="">
                </div>
                <p>Earn thousands of dollars by recruiting your friends</p>
            </div>
            <div class="jumbotron bg-white d-flex align-items-center">
                <div class="img-container w-50 mr-3">
                    <img src="/referral_static/images/hand.png" alt="">
                </div>
                <p>Shore Capital Corporation will pay you $100 every time your recruit closes a qualified transaction</p>
            </div>
            <div class="jumbotron bg-white d-flex align-items-center">
                <div class="img-container w-50 mr-3">
                    <img src="/referral_static/images/ap.png" alt="">
                </div>
                <p>Receive recurring residual income for the first two years for every recruit you bring on board!
                </p>
            </div>
        </div>

        <div class="jumbotron bg-white my-4">
            <FlowChart/>
        </div>

        <div class="my-3 d-grid grid-auto-row-minmax about-page grid-row-400px">
            <div class="img-container overflow-hidden gr-md-2">
                <img src="/referral_static/images/meeting.png" alt="">
            </div>
            <InvitationBox/>
        </div>

        <div class="my-3">
            <div class="jumbotron bg-white">
                <h4 class="mb-5 text-center">Realtor Reviews</h4>

                <div class="mt-4">
                    <div class="splide">
                        <div class="splide__track">
                            <ul class="splide__list">
                                <li class="splide__slide">
                                    <div class="d-grid grid-auto-row-minmax">
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
                                </li>
                                <li class="splide__slide">
                                    <div class="d-grid grid-auto-row-minmax">
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
                                    </div>
                                </li>
                                <li class="splide__slide">
                                    <div class="d-grid grid-auto-row-minmax">
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
                                            <h3>Howard Ken</h3>
                                            <p>Shore Capital Provides top notch service, I highly recommend them, because of their great system. Their web app is very polished, makes me use their application a lot. Also their service is the best. Shore Capital Corporation is the best Real Estate Company!</p>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</Dashboard>