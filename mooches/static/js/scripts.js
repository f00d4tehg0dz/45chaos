$(document).ready(function() {
  // === Scroll Up Button === //
	var amountScrolled = 700;
	$(window).scroll(function() {
		if ($(window).scrollTop() > amountScrolled) {
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

	// === Date Find Selector === //
	$('form[role="datefind"]').submit(function(ev) {
		$('.sub-info:first').hide();
		ev.preventDefault();
		// get the input value with:
		var date_term = $('#date-info').val();
		// convert from 02/16/1985  to  1985-02-16
		var dateAr = date_term.split('/');
		var newDate = dateAr[2] + '-' + dateAr[0] + '-' + dateAr[1];
		$.ajax({
			type: "POST",
			url: 'data.php',
			data: {
				df: newDate
			},
			success: function(returnData) {
				// blank the search_results div.
				$("#date-results").html('');
				if ($(".date-info").is(":hidden")) {
					$('#date-results').html('');
					$(".date-info").slideDown("slow", function() {
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
	// === Date Selector === //
	// Make your own here: https://eternicode.github.io/bootstrap-datepicker
	var dateSelect = $('#mooch-datepicker');
	var dateMooch = $('#date-mooch');
	var spanDateFormat = 'ddd, MMMM D yyyy';
	dateSelect.datepicker({
		autoclose: true,
		format: "mm/dd/yyyy",
		maxViewMode: 0,
		dateInfo: "now"
	}).on('change', function() {
		var start = $.format.date(dateMooch.datepicker('getDate'), spanDateFormat);
	});
});
