function pageTransition() {

    var tl = gsap.timeline();

    tl.to('ul.transition li', { duration: .5, scaleY: 1, transformOrigin: "bottom right", stagger: .2 })
    tl.to('.loader', 3, { autoAlpha: 1})
    tl.to('ul.transition li', { duration: .5, scaleY: 0, transformOrigin: "top left", stagger: .1, delay: .1 })
}

function contentAnimation() {
    var tl = gsap.timeline();
    tl.from('.left', { duration: 1.5, translateY: 50, opacity: 0 })
    tl.to('img', { clipPath: "polygon(0 0, 100% 0, 100% 100%, 0% 100%)" }, "-=1.1")
}

function delay(n) {
    n = n || 2000;
    return new Promise(done => {
        setTimeout(() => {
            done();
        }, n);
    });
}

barba.init({
    sync: true,
    transitions: [{
        async leave(data) {
            const done = this.async();
            pageTransition();
            await delay(1500);
            done();
        },
        async enter (data) {
            contentAnimation(); 
        },
        async once (data) {
            contentAnimation(); 
        }
    }]
})




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