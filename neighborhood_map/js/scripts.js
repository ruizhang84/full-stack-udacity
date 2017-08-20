// hiddern bar
var viewModel = {
  showMessage: ko.observable(true),
  hiddenBar: function(){
    this.showMessage(! this.showMessage());
  },
  restaurant: ko.observableArray(),
  filtered: ko.observable("")
};

ko.applyBindings(viewModel);

// google maps
var map;
var infowindow;
const maxSearch = 11;

function initMap() {
  const Boston = {lat: 42.364506, lng: -71.038887};
  let zoomView = 13;
  let rad = 10000;
  let interest = 'restaurant';

  try {
    map = new google.maps.Map(document.getElementById('map'), {
      center: Boston,
      zoom: zoomView
    });

    infowindow = new google.maps.InfoWindow();
    var service = new google.maps.places.PlacesService(map);
    service.nearbySearch({
          location: Boston,
          radius: rad,
          type: interest
        }, search);
  }
  catch(err){
    alert("error!");
    console.log(err.message);
  }
}

function search(results, status){
  if (status === google.maps.places.PlacesServiceStatus.OK) {
    for (var i = 0; i < results.length && i < maxSearch; i++) {
      createMarker(results[i]);
    }
  }
}

mapError = () => {
  // Error handling
  console.log("error on maps!");
  alert("map loading error!");

};

// maps marker & foursquare review
const clientId = '1BKIHPJRF4X1IYNYTVG3KVQU01D554SFUQTO5YUQSSH1ERVL';
const clientSecret = 'ZTPSRIOAUPU4XC1XUPJZBGHOSBC5NWBZFZCQYEUHN50IPGWI';
const d = new Date();
const currnetDate = d.getFullYear() +
    ((d.getMonth()+1)<10 ? '0' : '') + (d.getMonth()+1) +
    (d.getDate()<10 ? '0' : '') + d.getDate();
var markers = [];

function createMarker(place) {
  let placeLoc = place.geometry.location;
  var marker = new google.maps.Marker({
    map: map,
    position:placeLoc,
    animation: google.maps.Animation.DROP
  });
  markers.push([place, marker]);

  // add viewModel and listener for markers
  viewModel.restaurant.push([place, marker]);     // !build up the restraurant list
  google.maps.event.addListener(marker, 'click', function(){
    markerSelect(place, marker);
  });
}


function markerSelect (place, marker) {
  let content = '<p class="h4 text-primary">' + place.name + '</p>';

  // ajax to retreive info
  $.ajax({
    url:'https://api.foursquare.com/v2/venues/search',
    data: {
           ll: place.geometry.location.lat()+','+place.geometry.location.lng(), 
           limit: 1,
           query: place.name,
           client_id: clientId, 
           client_secret: clientSecret, 
           v: currnetDate
          },
    dataType: "json",
    success: function( data ) {
      var place_data = data.response.venues[0];
      if (place_data.contact.hasOwnProperty('formattedPhone'))
          content += '<p>' + place_data.contact.formattedPhone +'</p>';
      if (place_data.location.hasOwnProperty('formattedAddress'))
          content += '<p>' + place_data.location.formattedAddress + '</p>';
      if (place_data.hasOwnProperty('url'))
          content += '<p>' + place_data.url;
      if (place_data.contact.hasOwnProperty('twitter'))
          content += '<p> Twitter: @' + place_data.contact.twitter + '</p>';
      //console.log( JSON.stringify(place_data) );
      infowindow.setContent(content);
      infowindow.open(map, marker);
      marker.setAnimation(google.maps.Animation.BOUNCE);
      setTimeout(function() {
        marker.setAnimation(null)
      }, 2000);
    }
  })
  .fail(function() {
    console.log("error");
    // place name as only info
    content += '<p> error loading info.. </p>'
    infowindow.setContent(content);
    infowindow.open(map, marker);
  });
}


// filter
function filterMap(){
  viewModel.restaurant.removeAll();
  for (var i = 0; i < markers.length; i++) {
    // filter by substring
    let place_name = markers[i][0].name;
    if (place_name.indexOf(viewModel.filtered()) !== -1){
      // Sets the map on all markers in the array.
      markers[i][1].setMap(map);
      viewModel.restaurant.push(markers[i]);
    }else{
      markers[i][1].setMap(null);
    }
  }
}

// update the restaurant locations list, color changes for selected
function colorChange(idx){
  var lItems = document.getElementsByClassName('restaurantli');
  for (var i = 0; i <lItems.length; i++) {
    if (i == idx){
      lItems[i].className = "restaurantli active";
    }else{
      lItems[i].className = "restaurantli";
    }
  }
}



