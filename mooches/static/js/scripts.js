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
