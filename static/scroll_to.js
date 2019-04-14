$(document).ready(function() {
  $("#overview-btn").click(function() {
       $('html, body').animate({
           scrollTop: $("#overview").offset().top
       }, 1500);
   });
   $("#home-btn").click(function() {
        $('html, body').animate({
            scrollTop: $("#main-section").offset().top
        }, 1500);
    });
    $("#contact-btn").click(function() {
         $('html, body').animate({
             scrollTop: $("#contact").offset().top
         }, 1500);
     });
});
