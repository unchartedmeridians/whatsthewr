$(document).ready(function() {
	$("#id_game_as_text").autocomplete({
	 source: function(request, response) {
			$.ajax({
				url: "/ajax/autocomplete/game/",
				dataType: "json",
				data: {
					term: request.term
				},
				success: function(data) {
					response(data.games)
				}
			});
		}});
});
