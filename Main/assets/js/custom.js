jQuery(function($) {
    /*=============================================================
        Authour URI: www.binarytheme.com
        License: Commons Attribution 3.0

        http://creativecommons.org/licenses/by/3.0/

        100% To use For Personal And Commercial Use.
        IN EXCHANGE JUST GIVE US CREDITS AND TELL YOUR FRIENDS ABOUT US

        ========================================================  */
    /*==========================================
    CUSTOM SCRIPTS
    =====================================================*/

    // CUSTOM LINKS SCROLLING FUNCTION

    $('a[href*="#"]').click(function () {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '')
       && location.hostname == this.hostname) {
            var $target = $(this.hash);
            $target = $target.length && $target
            || $('[name=' + this.hash.slice(1) + ']');
            if ($target.length) {
                var targetOffset = $target.offset().top;
                $('html,body')
                .animate({ scrollTop: targetOffset }, 800); //set scroll speed here
                return false;
            }
        }
    });

    /*==========================================
   SCROLL REVEL SCRIPTS
   =====================================================*/

    // Initialize ScrollReveal with settings that handle page refresh at any scroll position
    ScrollReveal({
        reset: false,           // Don't reset elements when they go out of view
        viewFactor: 0.1,       // Reveal when 10% of element is visible
        mobile: true,          // Enable on mobile
        desktop: true          // Enable on desktop
    }).reveal('[data-scrollreveal]');

    /*==========================================
    WRITE  YOUR  SCRIPTS BELOW
    =====================================================*/

});