function pageTransition() {

    var tl = gsap.timeline();

    tl.to('ul.transition li', { duration: .5, scaleY: 1, transformOrigin: "bottom right", stagger: .2 })
    tl.to('.loader', 0.2, { autoAlpha: 1})
    tl.to('.loader', .1, { autoAlpha: 0, delay: 0.75 })
    tl.to('ul.transition li', { duration: .4, scaleY: 0, transformOrigin: "top left", stagger: .1, delay: .5 })
}

function contentAnimation() {
    var tl = gsap.timeline();
    tl.from('.left', { duration: 1.5, translateY: 50, opacity: 0 })
    tl.to('img', { clipPath: "polygon(0 0, 100% 0, 100% 100%, 0% 100%)" }, "-=1.1")
}

// Barba.Dispatcher.on('newPageReady', function(current, prev, container) {
//     history.scrollRestoration = 'manual';
// });

function delay(n) {
    n = n || 2000;
    return new Promise(done => {
        setTimeout(() => {
            done();
        }, n);
    });
}

var indexJS = $("script[src*='" + 'index.js' + "']")

sessionStorage.setItem("visitedHome", false)

barba.init({
    sync: true,
    transitions: [{
        async leave(data) {
            const done = this.async();
            pageTransition();
            await delay(1500);
            done();
        
        }


        
        // INDIVIDUAL COMPONENT ANIMATION
        // },
        // async enter (data) {
        //     contentAnimation(); 
        // },
        // async once (data) {
        //     contentAnimation(); 
        // }

    }],
    
    
    // Load index.js file before entering next page
    views: [
        {namespace: 'data',
            afterLeave({ next }) {
                const myPromise = new Promise((resolve, reject) => {
                    let script = document.createElement('script');
                    script.src = '/js/index.js';
                    next.container.appendChild(script);
                    console.log("RAN INIT ON BARBA RIGHT HERE");
                    resolve("Success!")
                })
            },
        },
        {namespace: 'home',
            afterLeave({ next }) {
                const myPromise = new Promise((resolve, reject) => {
                    let script = document.createElement('script');
                    script.src = '/js/index.js';
                    next.container.appendChild(script);
                    console.log("RAN INIT ON BARBA RIGHT HERE");
                    resolve("Success!")
                })                
                // myPromise.then((successMessage) => {
                //     $table.bootstrapTable();
                //     console.log(successMessage)
                // }).catch((message) => {
                //     console.log("Error")
                //     setTimeout(() => {
                //         $table.bootstrapTable();
                //         console.log("TIMEOUT FUNCTION");
                //     }, 500);
                // });
            },
            beforeEnter() {
                var visitedHome = sessionStorage.getItem("visitedHome")
                if (visitedHome == 'true') {
                    console.log('script ran')
                    var tl = gsap.timeline();
                    tl.to('.first-line', { translateY: 0, translateX: 0, opacity: 1, duration: 0.0, ease: 'Power2.easeOut', delay: 0.0})
                    tl.to('.second-line', { translateY: 0, translateX: 0, opacity: 1, duration: 0.0, ease: 'Power2.easeOut', delay: 0.0})
                    tl.staggerFromTo('.nav-item', 0.8, { translateY: 0, translateX: 0, scaleY: .5, scaleX: .5, opacity: 0 }, { translateY: 0, translateX: 0, scaleY: 1, scaleX: 1, opacity: 1 }, 0.1);
                } else {
                    var tl = gsap.timeline();
                    tl.fromTo('.first-line', { translateY: -50, translateX: 0, opacity: 0 }, { translateY: 0, translateX: 0, opacity: 1, duration: 1.0, ease: 'Power2.easeOut', delay: 1.0})
                    tl.fromTo('.second-line', { translateY: 100, translateX: 0, opacity: 0 }, { translateY: 0, translateX: 0, opacity: 1, duration: 1.0, ease: 'Power2.easeOut', delay: 0.0})
                    tl.staggerFromTo('.nav-item', 0.8, { translateY: 0, translateX: 0, scaleY: .5, scaleX: .5, opacity: 0 }, { translateY: 0, translateX: 0, scaleY: 1, scaleX: 1, opacity: 1 }, 0.1);
                    sessionStorage.setItem("visitedHome", true)
                }
            }
        },
        {namespace: 'contact',
            beforeEnter({ next }) {
                const myPromise = new Promise((resolve, reject) => {
                    let script = document.createElement('script');
                    script.src = 'https://www.google.com/recaptcha/api.js';
                    next.container.appendChild(script);
                    resolve("Success!")
                })
                function onSubmit(token) {
                    document.getElementById("demo-form").submit();
                    }
                const myPromise2 = new Promise((resolve, reject) => {
                    let script2 = document.createElement('script');
                    script2.src = 'https://www.google.com/recaptcha/api.js?render=reCAPTCHA_site_key';
                    next.container.appendChild(script2);
                    resolve("Success!")
                })
                // function onClick(e) {
                //     e.preventDefault();
                //     grecaptcha.ready(function () {
                //         grecaptcha.execute('reCAPTCHA_site_key', { action: 'submit' }).then(function (token) {
                //             // Add your logic to submit to your backend server here.
                //         });
                //     });
                // }
                function onSubmit(token) {
                    document.getElementById("demo-form").submit();
                }
                function onClick(e) {
                    e.preventDefault();
                    grecaptcha.ready(function () {
                        grecaptcha.execute('reCAPTCHA_site_key', { action: 'submit' }).then(function (token) {
                            // Add your logic to submit to your backend server here.
                        });
                    });
                }
            },
            afterLeave({ next }) {
                const myPromise = new Promise((resolve, reject) => {
                    let script = document.createElement('script');
                    script.src = '/js/index.js';
                    next.container.appendChild(script);
                    console.log("RAN INIT ON BARBA RIGHT HERE");
                    resolve("Success!")
                })
            },
        },
        {namespace: 'about',
            afterLeave({ next }) {
                const myPromise = new Promise((resolve, reject) => {
                    let script = document.createElement('script');
                    script.src = '/js/index.js';
                    next.container.appendChild(script);
                    console.log("RAN INIT ON BARBA RIGHT HERE");
                    resolve("Success!")
                })
            },
        },
        {namespace: 'privacy',
            afterLeave({ next }) {
                const myPromise = new Promise((resolve, reject) => {
                    let script = document.createElement('script');
                    script.src = '/js/index.js';
                    next.container.appendChild(script);
                    console.log("RAN INIT ON BARBA RIGHT HERE");
                    resolve("Success!")
                })
            },
        },
        {namespace: 'terms',
            afterLeave({ next }) {
                const myPromise = new Promise((resolve, reject) => {
                    let script = document.createElement('script');
                    script.src = '/js/index.js';
                    next.container.appendChild(script);
                    console.log("RAN INIT ON BARBA RIGHT HERE");
                    resolve("Success!")
                })
            },
        },
        {namespace: 'sitemap',
            afterLeave({ next }) {
                const myPromise = new Promise((resolve, reject) => {
                    let script = document.createElement('script');
                    script.src = '/js/index.js';
                    next.container.appendChild(script);
                    console.log("RAN INIT ON BARBA RIGHT HERE");
                    resolve("Success!")
                })
            },
        },
    ]
})

Barba.Prefetch.init()


// Barba.Pjax.start();
// Barba.Prefetch.init()


// var transitionAnimation = Barba.BaseTransition.extend({

//     start: function () {

//         Promise
//             .all([this.newContainerLoading, this.startTransition()])
//             .then(this.fadeIn.bind(this));

//     },

//     startTransition: function () {

//         var transitionPromise = new Promise(function (resolve) {

//             var outTransition = new TimelineMax();


//             outTransition

//                 .to(".title", 1, { y: -50, autoAlpha: 0, ease: Power2.easeOut })
//                 .set(".color-wipe", { display: 'block', y: "100%" }, "-=0.7")
//                 .staggerFromTo(".color-wipe", 1, { y: "100%" }, { y: "-100%", ease: Expo.easeOut }, 0.2, "-=0.7")

//                 .to(".loader", 1, {
//                     autoAlpha: 1, onComplete: function () {
//                         resolve();
//                     }
//                 })



//                 .staggerFromTo(".color-wipe", 1, { y: "-100%" }, { y: "-200%", ease: Expo.easeIn }, 0.2, "-=0.5")
//                 .set(".color-wipe", { display: 'none' })



//         });



//         return transitionPromise;

//     },





//     fadeIn: function () {

//         $(window).scrollTop(0);

//         var _this = this;
//         var $el = $(this.newContainer);

//         TweenMax.set($(this.oldContainer), { display: "none" });
//         TweenMax.set($el, { visibility: "visible", opacity: 0, });


//         TweenMax.to(".loader", 1, { y: -50, autoAlpha: 0, ease: Expo.easeOut })
//         TweenMax.fromTo(".title", 1.5, { y: 30, autoAlpha: 0 }, { delay: 0.8, y: 0, autoAlpha: 1, ease: Expo.easeOut })

//         TweenMax.to($el, 0.1, {
//             opacity: 1,
//             onComplete: function () {
//                 _this.done();
//                 console.log("done");
//             }
//         });
//     }
// });


// Barba.Pjax.getTransition = function () {
//     /**
//      * Here you can use your own logic!
//      * For example you can use different Transition based on the current page or link...
//      */
//     return transitionAnimation;

// };