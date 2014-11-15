$(document).ready(function() {
	var lastVal = "";
	$("#id_game_as_text").on('change autocompleteclose', function() {
			$.ajax({
				url: "/ajax/autocomplete/category/",
			    dataType: "json",
				data: {
					term: $(this).val()
				},
				success: function(categories) {
                    var categoryP = $('#id_category_as_text').closest('p')
					if ($('#id_game_as_text').val().toUpperCase() != lastVal) {
						lastVal = $('#id_game_as_text').val().toUpperCase();

						if (categories.length > 0) {
							var catSelector = '<div id="category-choices">'
								+ $.map(categories, function(e, i) {
									return '<input type="radio"'
                                    + ' name="category-choice"'
                                    + ' class="category-choice"'
                                    + ' id="category-choice-' + i
                                    + '" value="' + e + '">'
                                    + ' <label for="category-choice-' + i + '">'
                                    + e + '</label><br />';
								})
								.join("")
								+ '<input type="radio" name="category-choice"'
                                + ' id="new-category" value="new">'
								+ '<label for="new-category"'
                                + ' id="new-category-label">New:</label>'
								+ '<input id="new-category-input"'
                                + ' maxlength="100" name="new-category"'
                                + ' type="text" /></div>';

								categoryP
								.find('input')
								.hide();

								categoryP.hide();

								categoryP
								.find('label')
								.addClass('category-choices-label');

								categoryP
								.append(catSelector)
								.fadeIn();
							}

						else {
							if ($('#category-choices').length) {
								categoryP.find('#category-choices').remove();
								categoryP.find('input').show();
								categoryP.find('label').removeClass('category-choices-label')
							}
						}
					}
					}
				});
		});
	$('p').on('click', '#new-category-input', function() { $('#new-category').prop('checked', true); });
});
