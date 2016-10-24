var map;
function loadMapScenario() {
    map = new Microsoft.Maps.Map(document.getElementById('myMap'), {
        credentials: 'AtzePqCL6lUAr5H98sJ6JHEYBRy5w2ryt_nIsLv3DrpQglPNZoUSEbyB_dWLFHpd'
    });
    
    add_pokemon_layer();
}


//define pokemon data format
map_items = [
    {
        "pokemon_id" : 4,
        "expire" : 1477296019000,
        "latitude" : 32.870739,
        "longitude" : -117.210426
    }
]

function get_count_down_time_from_expire_epoch(epoch) {
    var now_time = new Date().getTime() / 1000;
    var time_left = epoch / 1000 - now_time;
    var minute = Math.floor(time_left / 60);
    var second = Math.floor(time_left % 60);
    if (second < 10) {
        second = "0" + second;
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
    var pokemon_layer = get_pokemon_layer_from_map_items(map_items);
    map.layers.insert(pokemon_layer);
}

//add pokemon count down refresh
