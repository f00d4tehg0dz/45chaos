$(document).ready(function() {


var amountScrolled = 700;

$(window).scroll(function() {
    if ( $(window).scrollTop() > amountScrolled ) {
        $('.to-the-top').fadeIn('slow');
    } else {
        $('.to-the-top').fadeOut('slow');
    }
});

$('.to-the-top').click(function() {
    $('html, body').animate({
        scrollTop: 0
    }, 700);
    return false;
});

// Menu Btn Slides in Mooches Calc
    $('.menu-btn').click(function() {
      $(this).toggleClass("menu-btn-left");
      $('.slide-out').toggleClass('slide-in');
    });

// Add wrapper to Table to Add Fixed Height
  $('.row.no-gutters.f-table-row').wrapAll('<div id="f-table-container">');
if ($('#f-table-container').css('overflow') == 'hidden'){
  $('#f-table-container').after('<div class="load-more-btn btn">Load The Rest! </div>')
}
// Load More Button to remove height and overflow from Wrapper above
$('.load-more-btn').click(function(){
  $('#f-table-container').css('overflow','none');
$('#f-table-container').css('height','100%');
$('.load-more-btn').hide();
})

// Load More Button for Showing For Auto Load - No longer needed
$('.load-more').before('</div>');

// Searches Autocomplete
    $(function() {
        $( ".searchs" ).autocomplete({
            source: 'search.php'
        });
    });
    $('form[role="search"]').submit(function(ev) {
      $( ".date-info" ).hide();
  ev.preventDefault();
  // get the input value with:
  var search_term = $('#search_box').val().trim();
  $.ajax({
    type: "GET",
    url: 'search.php',
    data: {
      q: search_term
    },
    success: function(returnData) {
      //Blank the search_results div.
      $('#search_results').html('');
      if ( $( ".sub-info:first" ).is( ":hidden" ) ) {
          $('#search_results').html('');
          $("#search_results").html(returnData);
          $( ".sub-info" ).slideDown( "slow", function() {
   // $('.sub-info').css('padding', '5rem 0');

     })



   } else {
        $("#search_results").html(returnData);
       // $( ".sub-info" ).hide();
     }

    }
  });
});
// Date Find Selector
$('form[role="datefind"]').submit(function(ev) {
  $('.sub-info:first').hide();
ev.preventDefault();
// get the input value with:

var date_term = $('#date-info').val();
// convert from 02/16/1985  to  1985-02-16
//var dateAr = '2014-01-06'.split('-');
var dateAr = date_term.split('/');
var newDate = dateAr[2] + '-' + dateAr[0] + '-' + dateAr[1];

console.log(newDate);
$.ajax({
type: "POST",
url: 'data.php',
data: {
  df: newDate
},
success: function(returnData) {
  //blank the search_results div.
    $("#date-results").html('');
  if ( $( ".date-info" ).is( ":hidden" ) ) {
      $('#date-results').html('');
      $( ".date-info" ).slideDown( "slow", function() {

          $("#date-results").html('');
   $("#date-results").html(returnData);
 })
 } else {
$("#date-results").html(returnData);
   // $( ".date-info" ).hide();
 }

}
});
});






//Date Selector Pretty
// Make your own here: https://eternicode.github.io/bootstrap-datepicker

var dateSelect     = $('#mooch-datepicker');
var dateMooch    = $('#date-mooch');
var spanDateFormat = 'ddd, MMMM D yyyy';

dateSelect.datepicker({
  autoclose: true,
  format: "mm/dd/yyyy",
  maxViewMode: 0,
  dateInfo: "now"
}).on('change', function() {
  var start = $.format.date(dateMooch.datepicker('getDate'), spanDateFormat);
});


/**
* Convert french date interval "d/m/Y au d/m/Y" in a string which can be properly compared lexicographically
* For example, converts "01/04/2017 au 05/06/2018" to "2017-04-01-2018-06-05"
* @param value
* @returns {string}
*/
function convertDateInterval(value) {
    var matches = value.match(/([0-9]{2}\/[0-9]{2}\/[0-9]{4}) au ([0-9]{2}\/[0-9]{2}\/[0-9]{4})/);
    var date1Parts = matches[1].split('/');
    var date2Parts = matches[2].split('/');

    return date1Parts[2] + '-' + date1Parts[1] + '-' + date1Parts[0] + '-' + date2Parts[2] + '-' + date2Parts[1] + '-' + date2Parts[0];

}

  /* === Disable Lazy Load, no longer needed === */
    // InfiniteTable();


    function InfiniteTable() {


      $(window).scroll(function() {
          var numItems = $('.cards').length;
            if (numItems == 25) {
                $('.number-tables').html("Showing the first&nbsp"  +numItems+ ",&nbspscroll to load more")
            } else if (numItems == 137) {
              $('.number-tables').html("Showing all&nbsp"  +numItems)
            }


            var lastID = $('.load-more').attr('lastID');
            if ($(window).scrollTop()  >= $(document).innerHeight() - $(window).height() - 60 && (lastID != 0)) {


var request;
       if(request) {
           request.abort();
       }
           request = $.ajax({
            type: 'POST',
            url: 'data.php',
            async:true,
            data: {
              id: lastID
            },
            beforeSend: function() {
              $('.load-more').show();
            },
            success: function(html) {

              $('.load-more').remove();

              $('.f-table').append(html);
            }

          }); //ajax

        }
        }) // scroll

    } // InfiniteTimeline


});
