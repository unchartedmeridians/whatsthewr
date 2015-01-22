function makeCatSelector(cats) {
    var catSelector = '<select id="category-choices">'
        + $.map(cats, function (e, i) {
            return '<option value="' + e + '">' + e + '</option>'
        })
        .join('')
        + '<option value="new">New category:</option></select>';
    return catSelector;
}

function fadeOutFadeInElem(target, replacement) {
    target.hide()
    .parent()
    .append(replacement)
    .fadeIn();
}

function renderSelector(game) {
    $.ajax({
        url: '/ajax/autocomplete/category/',
        dataType: 'json',
        data: {
            term: game
        },
        success: function (cats) {
            if (cats.length > 0) {
                var catSelector = makeCatSelector(cats);
                $('#id_category_as_text').hide()
                    .parent().find('label').after(catSelector)
                    .fadeIn();
                $('#category-choices').change(function() {
                    if ($(this).val() === 'new') {
                        $('#id_category_as_text').fadeIn();
                    } else {
                        $('#id_category_as_text').hide();
                    }});
            } else {
                $('#category-choices').fadeOut().remove();
                $('#id_category_as_text').fadeIn();
            }}});
}

$(document).ready(function () {
    var lastVal = '';
    $('#id_game_as_text').on('autocompleteclose keyup', function () {
        if ($(this).val().toUpperCase() !== lastVal) {
            lastVal = $(this).val().toUpperCase();
            renderSelector(lastVal);
            }});
    });
