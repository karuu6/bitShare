$(document).ready(function() {
  var xmlhttp;
  xmlhttp = new XMLHttpRequest();
  xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var resp = JSON.parse(this.responseText);
      var price = (resp.bpi.USD.rate).toString();
      price = price.replace(',','');
      price = parseFloat(price).toFixed(2);
      $('#price').text(price + '$');
    }
  };
  xmlhttp.open("GET", "https://api.coindesk.com/v1/bpi/currentprice.json", true);
  xmlhttp.send();
})
