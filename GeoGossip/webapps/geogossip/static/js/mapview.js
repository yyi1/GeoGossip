var map = null;
var circles = [];
var myPosition = null;

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

function error (err) {
    $('#no-gps').alert();
    console.log(err)
}

function initMap (position) {
    if (position == undefined) {
        position = {
            coords: {
                latitude: 40.4427420976,
                longitude: -79.9460211396
            }
        }
    }
    map = new GMaps({
        div: '#map',
        lat: position.coords.latitude,
        lng: position.coords.longitude,
        zoom: 17,
        dblclick: function(event) {
            window.location.href =
                '/geogossip/create-group-with-latlon/' +
                event.latLng.lat() +
                '/' +
                event.latLng.lng();
        }
    });
    map.addMarker({
        animation: google.maps.Animation.DROP,
        lat: position.coords.latitude,
        lng: position.coords.longitude,
        icon: {
            url: 'https://geogossipteam257.s3.amazonaws.com/img/pin.png',
            size: new google.maps.Size(100, 100),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(18, 35),
            scaledSize: new google.maps.Size(36, 36)
        }
    });
    var csrftoken = getCookie('csrftoken');
    getGroups(position, csrftoken);
    getBusinesses(position, csrftoken);
}

function getGroups(position, csrftoken) {
    $.ajax({
        type: 'POST',
        url: '/geogossip/get-groups',
        headers: {
            'X-CSRFToken': csrftoken
        },
        dataType: 'json',
        data: {
            lat: position.coords.latitude,
            lon: position.coords.longitude
        },
        success: function(json) {
            var list_groups = $('#group-list');
            list_groups.empty();
            var groups = JSON.parse(json);
            for (var i = 0;i < groups.length;i++) {
                var insert =
                    '<a type="button" class="list-group-item" href="/geogossip/group-chat/' +
                    groups[i].pk +
                    '">' +
                    groups[i].fields['name'] +
                    '</a>';
                list_groups.prepend($(insert));
                var circle = new google.maps.Circle({
                    radius: groups[i].fields['radius'],
                    lat: groups[i].fields['lat'],
                    lng: groups[i].fields['lon'],
                    strokeColor: '#BBD8E9',
                    strokeOpacity: 0.5,
                    strokeWeight: 3,
                    fillColor: '#BBD8E9',
                    fillOpacity: 0.3,
                    map: map.map,
                    center: {
                        lat: groups[i].fields['lat'],
                        lng: groups[i].fields['lon']
                    }
                });
                circles.push(circle);
                var marker = map.createMarker({
                    groupId: groups[i].pk,
                    lat: groups[i].fields['lat'],
                    lng: groups[i].fields['lon'],
                    title: groups[i].fields['name'],
                    description: groups[i].fields['description'],
                    icon: {
                        url: 'https://geogossipteam257.s3.amazonaws.com/img/marker.png',
                        size: new google.maps.Size(100, 100),
                        origin: new google.maps.Point(0, 0),
                        anchor: new google.maps.Point(15, 29),
                        scaledSize: new google.maps.Size(30, 30)
                    },
                    click: function() {
                        var infowindow = new google.maps.InfoWindow({
                            content: '<h4>' +
                            this.title +
                            '</h4><br><p>' +
                            this.description + '</p><br><a type="button" class="btn btn-primary" href="/geogossip/group-chat/' +
                            this.groupId +
                            '">join this group</a>'
                        });
                        infowindow.open(map, this);
                    }
                });
                map.addMarker(marker)
            }
        },
        async: true
    });
}

function getBusinesses(position, csrftoken) {
    $.ajax({
        type: 'POST',
        url: '/geogossip/get-businesses',
        headers: {
            'X-CSRFToken': csrftoken
        },
        dataType: 'json',
        data: {
            lat: position.coords.latitude,
            lon: position.coords.longitude
        },
        success: function(json) {
            var businesses = JSON.parse(json);
            for (var i = 0;i < businesses.length;i++) {
                var description = 'categories: ' + businesses[i].fields['categories'] + '<br>' +
                    'contact phone number: ' + businesses[i].fields['display_phone'] + '<br>' +
                    'popularity: ' + businesses[i].fields['review_count'] + ' reviews<br>' +
                    'rating: ' + businesses[i].fields['rating'] + ' stars<br><img src="' +
                    businesses[i].fields['image_url'] +
                    '"/>';
                var marker = map.createMarker({
                    lat: businesses[i].fields['lat'],
                    lng: businesses[i].fields['lon'],
                    title: businesses[i].fields['name'],
                    description: description,
                    icon: {
                        url: 'https://geogossipteam257.s3.amazonaws.com/img/business.png',
                        size: new google.maps.Size(100, 100),
                        origin: new google.maps.Point(0, 0),
                        anchor: new google.maps.Point(12, 23),
                        scaledSize: new google.maps.Size(24, 24)
                    },
                    click: function() {
                        var infowindow = new google.maps.InfoWindow({
                            content: '<h4>' + this.title + '</h4><p>' + this.description + '</p>'
                        });
                        infowindow.open(map, this);
                    }
                });
                map.addMarker(marker)
            }
        },
        async: true
    });
}

function success (position) {
    myPosition = position;
    $(".alert").alert('close');
    console.log('lat:' + position.coords.latitude + '\t lon:' + position.coords.longitude);
    map.removeMarkers();
    for (var i = 0;i < circles.length;i++) {
        circles[i].setMap(null);
    }
    circles = [];
    if (map == null) {
        initMap(position);
    } else {
        map.addMarker({
            lat: position.coords.latitude,
            lng: position.coords.longitude,
            icon: {
                url: 'https://geogossipteam257.s3.amazonaws.com/img/pin.png',
                size: new google.maps.Size(100, 100),
                origin: new google.maps.Point(0, 0),
                anchor: new google.maps.Point(18, 35),
                scaledSize: new google.maps.Size(36, 36)
            }
        });
        var csrftoken = getCookie('csrftoken');
        getGroups(position, csrftoken);
        getBusinesses(position, csrftoken);
    }
}

$(document).ready(function() {
    // $('[data-toggle="tooltip"]').tooltip();
    // $("#map").popover({
    //     title: 'Enter Mobile Number',
    //     content: "Please enter 10 digit mobile number prefixed by country code eg +911234567890",
    //     trigger: 'hover'
    // });
    if (navigator.geolocation) {
        $(".alert").alert('close');
        window.setInterval(function () {
            navigator.geolocation.getCurrentPosition(success, error);
        }, 5000);
    } else {
        $('#no-gps').alert();
    }
});
