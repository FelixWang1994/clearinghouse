
$(document).ready(function() {
	$('#registerexperiment .collapsible').change(function() {
		//$('#mycheckboxdiv').toggle();
		sensor_on_change(this.getAttribute('data-target'), this.checked);
	});
});

function regsiterexperiment(){

	
}