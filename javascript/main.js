$(document).ready(function(){
	$(".form-select").on('change', function() {
		if (this.value == "filterby") {
			console.log(this.value)

			let textelement = $('<input id="filterinput" type="text" placeholder="Enter Condition">');
			$(".select-form").append( textelement );	
		} else {
			console.log(this.value);
			$("#filterinput").remove();	
		}
	});
}); 