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
  var date=new Date();
  var h=date.getHours();
  var m=date.getMinutes();
  var s=date.getSeconds();

  m=formatTime(m);
  s=formatTime(s);
  $('#clock').html(h+":"+m);
  $('#date').html(date.getDate() + "." + (date.getMonth()+1) + "." + date.getFullYear());

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
