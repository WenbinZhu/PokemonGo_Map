var map_manager = {
    map : null,
    map_items : []
}

//define pokemon data format
map_manager.map_items = [
//     {
//         "pokemon_id" : 4,
//         "expire" : 1477296019000,
//         "latitude" : 32.870739,
//         "longitude" : -117.210426
//     }
]

function set_user_current_location() {
    // Change initial view if possible
    if (navigator.geolocation) {
        function set_initial_view(position) {
            map_manager.map.setView({
                center: new Microsoft.Maps.Location(position.coords.latitude, position.coords.longitude),
                zoom: 16
            });
        }
        navigator.geolocation.getCurrentPosition(set_initial_view);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function loadMapScenario() {    
    map_manager.map = new Microsoft.Maps.Map(document.getElementById('myMap'), {
        credentials: 'AtzePqCL6lUAr5H98sJ6JHEYBRy5w2ryt_nIsLv3DrpQglPNZoUSEbyB_dWLFHpd'
    });
    
    set_user_current_location();
    
    add_pokemon_layer();
}

function get_count_down_time_from_expire_epoch(epoch) {
    var now_time = new Date().getTime() / 1000;
    var time_left = epoch / 1000 - now_time;
    var minute = Math.floor(time_left / 60);
    var second = Math.floor(time_left % 60);
    if (minute < 0 || second < 0) {
        return "00:00"
    }
    if (second >= 0 && second < 10) {
        second = "0" + second;
    }
    if (minute >= 0 && minute < 10) {
        minute = "0" + minute;
    }
    
    return minute + ":" + second;
}

//put pokemon image on map
function get_pokemon_layer_from_map_items(map_items) {
    var pushpins = [];
    for (var i in map_items) {
        map_item = map_items[i];

        var pushpin = new Microsoft.Maps.Pushpin(new Microsoft.Maps.Location(map_item["latitude"], map_item["longitude"]), 
                                                { icon: "images/pushpin_images/pokemon/" + map_item["pokemon_id"] + ".png",
                                                  title: get_count_down_time_from_expire_epoch(map_item["expire"]) });
        pushpins.push(pushpin);
    }
    
    var layer = new Microsoft.Maps.Layer();
    layer.add(pushpins);
    
    return layer;
}

function add_pokemon_layer() {
    var pokemon_layer = get_pokemon_layer_from_map_items(map_manager.map_items);
    map_manager.map.layers.insert(pokemon_layer);
}


//add pokemon count down refresh
function refresh_pokemon_layer() {
    var pokemon_layer = get_pokemon_layer_from_map_items(map_manager.map_items);
    map_manager.map.layers.clear();
    map_manager.map.layers.insert(pokemon_layer);
}


//connect REST API
function refresh_pokemon_data() {
    var bounds = map_manager.map.getBounds();
    var apigClient = apigClientFactory.newClient();
    
    var params = {
        //This is where any header, path, or querystring request params go. The key is the parameter named as defined in the API
        east : bounds.getEast(),
        north : bounds.getNorth(),
        south : bounds.getSouth(),
        west : bounds.getWest()
    };
    
    var body = {};
    var additionalParams = {};

    apigClient.mapPokemonsGet(params, body, additionalParams)
        .then(function(result){
            //This is where you would put a success callback
            map_manager.map_items = result.data;
        }).catch( function(result){
            //This is where you would put an error callback
            console.log(result);
    });   
    
    // hide and show progress_bar logic
    var progress_bar = document.getElementById('map_progressbar');
    if (map_manger.map_items.length > 20)
        progress_bar.style.visibility = "hidden";
    else
        progress_bar.style.visibility = "";
}

window.setInterval(refresh_pokemon_layer, 1000);
window.setInterval(refresh_pokemon_data, 1000);

