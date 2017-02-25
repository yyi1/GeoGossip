/**
 * Created by baishi on 11/26/16.
 */
var type = 'group';
var method = 'keyword';
var userDisabled = false;

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function() {
    $('#lat-box').hide();
    $('#lat').val('');
    $('#lon-box').hide();
    $('#lon').val('');
    $('#radius-box').hide();
    $('#radius').val('');
    $('#keyword-search').click(function () {
        method = 'keyword';
        $('#method').html('Key Word<span class="caret"></span>');
        $('#user-box').removeClass('disabled');
        userDisabled = false;
        $('#keyword-box').show();
        $('#lat-box').hide();
        $('#lat').val('');
        $('#lon-box').hide();
        $('#lon').val('');
        $('#radius-box').hide();
        $('#radius').val('');
    });
    $('#location-search').click(function () {
        method = 'location';
        $('#method').html('Location<span class="caret"></span>');
        $('#user-box').addClass('disabled');
        userDisabled = true;
        $('#keyword-box').hide();
        $('#keyword').val('');
        $('#lat-box').show();
        $('#lon-box').show();
        $('#radius-box').show();
        if (type == 'user') {
            type = 'group';
            $('#type').html('Group<span class="caret"></span>');
        }
    });
    $('#group-search').click(function () {
        type = 'group';
        $('#type').html('Group<span class="caret"></span>');
    });
    $('#business-search').click(function () {
        type = 'business';
        $('#type').html('Business<span class="caret"></span>');
    });
    $('#user-search').click(function () {
        if (!userDisabled) {
            type = 'user';
            $('#type').html('User<span class="caret"></span>');
        }
    });
    var csrftoken = getCookie('csrftoken');
    $('#send').click(function (event) {
        event.preventDefault();
        $('#results').empty();
        var keyword = $('#keyword').val();
        var lat = $('#lat').val();
        var lon = $('#lon').val();
        var radius = $('#radius').val();
        $.ajax({
            type: 'POST',
            url: '/geogossip/search',
            headers: {
                'X-CSRFToken': csrftoken
            },
            dataType: 'json',
            data: {
                type: type,
                method: method,
                keyword: keyword,
                lat: lat,
                lon: lon,
                radius: radius
            },
            async: true,
            success: function (json) {
                $('#keyword').val('');
                $('#lat').val('');
                $('#lon').val('');
                $('#radius').val('');
                var results = JSON.parse(json);
                console.log(results);
                for (var i = 0;i < results.length;i++) {
                    if (results[i].model == 'geogossip.group') {
                        $('#results').append('<a href="/geogossip/group-chat/' +
                            results[i].pk +
                            '" class="list-group-item"><h4>' +
                            results[i].fields['name'] +
                            '</h4><p>' +
                            results[i].fields['description'] +
                            '</p></a>')
                    } else if (results[i].model == 'geogossip.business') {
                        var description = 'categories: ' + results[i].fields['categories'] + '<br>' +
                            'contact phone number: ' + results[i].fields['display_phone'] + '<br>' +
                            'popularity: ' + results[i].fields['review_count'] + ' reviews<br>' +
                            'rating: ' + results[i].fields['rating'] + ' stars<br><img src="' +
                            results[i].fields['image_url'] + '"/>';
                        $('#results').append(
                            '<li class="list-group-item"><h4>' +
                            results[i].fields['name'] +
                            '</h4><p>' +
                            description +
                            '</p></li>')
                    } else if (results[i].model == 'auth.user') {
                        $('#results').append('<a href="/geogossip/profile/' +
                            results[i].pk +
                            '" class="list-group-item">' +
                            results[i].fields['username'] +
                            '</a>')
                    }
                }
            },
            error: function (jqXHR) {
                alert(jqXHR.responseText);
            }
        })
    });
});