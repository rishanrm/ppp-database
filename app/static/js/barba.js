function pageTransition() {
    var tl = gsap.timeline();

    tl.to('ul.transition li', { duration: .5, scaleY: 1, transformOrigin: "bottom right", stagger: .2 })
    tl.to('.loader', 0.2, { autoAlpha: 1})
    tl.to('.loader', .1, { autoAlpha: 0, delay: 0.75 })
    tl.to('ul.transition li', { duration: .4, scaleY: 0, transformOrigin: "top left", stagger: .1, delay: .5 })
}

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
            window.scrollTo(0,0); 
        }
    }],
    
    // Load index.js file before entering next page
    views: [
        {namespace: 'data',
            afterLeave({ next }) {
                const myPromise = new Promise((resolve, reject) => {
                    let script = document.createElement('script');
                    script.src = '/js/index.js';
                    next.container.appendChild(script);
                    resolve("Success!")
                })
            },
        },
        {namespace: 'summary-stats',
            afterLeave({ next }) {
                const myPromise = new Promise((resolve, reject) => {
                    let script = document.createElement('script');
                    script.src = '/js/index.js';
                    next.container.appendChild(script);
                    resolve("Success!")
                })
            },
        },
        {namespace: 'data-notes',
            afterLeave({ next }) {
                const myPromise = new Promise((resolve, reject) => {
                    let script = document.createElement('script');
                    script.src = '/js/index.js';
                    next.container.appendChild(script);
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
                    resolve("Success!")
                })                
            },
            beforeEnter() {
                var visitedHome = sessionStorage.getItem("visitedHome")
                if (visitedHome == 'true') {
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
                    resolve("Success!")
                })
            },
        },
    ]
})