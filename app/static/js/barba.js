function pageTransition() {

    var tl = gsap.timeline();

    tl.to('ul.transition li', { duration: .5, scaleY: 1, transformOrigin: "bottom left", stagger: .5})
    tl.to('ul.transition li', {duration: .5, scaleY: 0, transformOrigin: "bottom left", stagger: .5, delay: .1})
}

function contentAnimation() {
    var tl = gsap.timeline();
    tl.from('.left', {duration: 1.5, translateY: 50, opacity: 0})
    tl.to('img', {clipPath: "polygon(0 0, 100% 0, 100% 100%, 0% 100%)"}, "-=1.1")
}

function delay(n) {
    n = n || 2000;
    return new Promise(done => {
        setTimeout(() => {
            done();
        }, n);
    });
}

console.log("HERE IN JS")

// barba.init({

//     sync: true,

//     transitions: [{

//         async leave(data) {

//             const done = this.async();

//             pageTransition();
//             await delay(1500);
//             done();
//         },

//         async enter (data) {
//             contentAnimation(); 
//         },

//         async once (data) {
//             contentAnimation(); 
//         }
//     }]
// })




// GSAP 2ND TUTORIAL
// reset position of the loading screen
gsap.set(loader, {
    scaleX: 0,
    rotation: 10,
    xPercent: -5,
    yPercent: -50,
    transformOrigin: 'left center',
    autoAlpha: 1
});

// barba.init({
//     transitions: [{
//         async leave() {
//             await loaderIn();
//         },
//         enter() {
//             loaderAway();
//         }
//     }]
// });

function loaderIn() {
    // GSAP tween to stretch the loading screen across the whole screen
    return gsap.fromTo(loader,
        {
            rotation: 10,
            scaleX: 0,
            xPercent: -5
        },
        {
            duration: 0.8,
            xPercent: 0,
            scaleX: 1,
            rotation: 0,
            ease: 'power4.inOut',
            transformOrigin: 'left center'
        });
}

function loaderAway() {
    // GSAP tween to hide loading screen
    return gsap.to(loader, {
        duration: 0.8,
        scaleX: 0,
        xPercent: 5,
        rotation: -10,
        transformOrigin: 'right center',
        ease: 'power4.inOut'
    });
}

// do something before the transition starts
barba.hooks.before(() => {
    document.querySelector('html').classList.add('is-transitioning');
});
// do something after the transition finishes
barba.hooks.after(() => {
    document.querySelector('html').classList.remove('is-transitioning');
});

.is - transitioning {
    pointer - events: none;
    cursor: progress;
}

// scroll to the top of the page
barba.hooks.enter(() => {
    window.scrollTo(0, 0);
});







barba.init({
    transitions: [{
        name: 'opacity-transition',
        leave(data) {
            return gsap.to(data.current.container, {
                opacity: 0
            });
        },
        enter(data) {
            return gsap.from(data.next.container, {
                opacity: 0
            });
        }
    }]
});