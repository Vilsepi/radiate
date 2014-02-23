function refreshCards()
{
  $.get("/api/getCard/openweathermap", function(data) {
    $( "#left_card" ).html(data);
  });

  $.get("/api/getCard/lissuscraper", function(data) {
    $( "#right_card" ).html(data);
  });
}

function updateClock()
{
  var today=new Date();
  var h=today.getHours();
  var m=today.getMinutes();
  var s=today.getSeconds();

  m=formatTime(m);
  s=formatTime(s);
  $('#clock').html(h+":"+m);

  t=setTimeout(function(){updateClock()},500);
}

// pad minutes and seconds to two digits
function formatTime(i)
{
  if (i<10) {
    i="0" + i;
  }
  return i;
}

// TODO: setting global ajax config is not recommended
$.ajaxSetup ({
    cache: false
});

refreshCards();
window.setInterval(function(){
  refreshCards();
}, 10000);

updateClock();
