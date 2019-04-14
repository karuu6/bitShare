const particles = '#particles-js'
const buttonWidth = document.getElementById('buy-btn').offsetWidth
const pageWidth = $(window).width();
const pageHeight = screen.height;

$(document).ready(function() {
  $(particles).css('opacity', '1');
  $('#buy-btn').css('left', (100 - (buttonWidth/pageWidth * 100))/2 + 'vw');
  $('#contact').css('top', (100 + (80/pageHeight * 100)) + 'vh');
  $('#contact').css('height', (100 - (80/pageHeight * 100)) + 'vh');
  console.log();
  console.log(buttonWidth/pageWidth)

})
