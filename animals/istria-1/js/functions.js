// PARALLAX EFFECT
function EasyPeasyParallax() {
	scrollPos = $(this).scrollTop();
	$('#section-1').css({
		'background-position' : '50% ' + (-scrollPos/4)+"px"
	});
	$('#title-1').css({		
		'opacity': 1-(scrollPos/450)
	});
}
$(document).ready(function(){
	$(window).scroll(function() {
		EasyPeasyParallax();
	});
});
// STICKY NAV
$(window).scroll(function() {

    if ($(window).scrollTop() > 100) {
        $('.main_h').addClass('sticky');
    } else {
        $('.main_h').removeClass('sticky');
    }
});

// Mobile Navigation
$('.mobile-toggle').click(function() {
    if ($('.main_h').hasClass('open-nav')) {
        $('.main_h').removeClass('open-nav');
    } else {
        $('.main_h').addClass('open-nav');
    }
});

$('.main_h li a').click(function() {
    if ($('.main_h').hasClass('open-nav')) {
        $('.navigation').removeClass('open-nav');
        $('.main_h').removeClass('open-nav');
    }
});

 // SMOTH SCROLL
$(function() {
  $('a[href*=#]:not([href=#])').click(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
      if (target.length) {
        $('html,body').animate({
          scrollTop: target.offset().top
        }, 1200);
        return false;
      }
    }
  });
});

// MAKE SELECTED ELEMENTS THE SAME HEIGHT
$(function() {
    $('.column').matchHeight();
});
$(function() {
    $('.column2').matchHeight();
});
$(function() {
    $('.column3').matchHeight();
});
$(function() {
    $('.column4').matchHeight();
});
$(function() {
    $('.column5').matchHeight();
});
$(function() {
    $('.column6').matchHeight();
});
$(function() {
    $('.column7').matchHeight();
});

// animation wow js
var wow = new WOW(
  {
    boxClass:     'wow',      // animated element css class (default is wow)
    animateClass: 'animated', // animation css class (default is animated)
    offset:       200,          // distance to the element when triggering the animation (default is 0)
    mobile:       true,       // trigger animations on mobile devices (default is true)
    live:         true,       // act on asynchronously loaded content (default is true)
    callback:     function(box) {
      // the callback is fired every time an animation is started
      // the argument that is passed in is the DOM node being animated
    },
    scrollContainer: null // optional scroll container selector, otherwise use window
  }
);
wow.init();


// ANIMISTION
  $(document).ready(function() {
    $('.animsition-overlay').animsition({
      inClass: 'overlay-slide-in-bottom',
      outClass: 'overlay-slide-out-top',
      overlay : true,
      overlayClass : 'animsition-overlay-slide',
      overlayParentElement : 'body'
    })
    .one('animsition.inStart',function(){

      $('body').removeClass('bg-init');

      $(this)
        .find('.item')
        .append('<h2 class="target">Callback: Start</h2>');

      console.log('event -> inStart');
    })
    .one('animsition.inEnd',function(){
      $('.target', this).html('Callback: End');
      console.log('event -> inEnd');
    })
    .one('animsition.outStart',function(){
      console.log('event -> outStart');
    })
    .one('animsition.outEnd',function(){
      $('.target', this).html('Callback: End');
      console.log('event -> outEnd');
    });

  });

