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
        "pokemon_id" : 5,
        "expire" : 1476338470000,
        "latitude" : 40.7477663774335,
        "longitude" : -73.998796414357
    }
]


//put pokemon image on map
function get_pokemon_layer_from_map_items(map_items) {
    var pushpins = [];
    for (var i in map_items) {
        map_item = map_items[i];
        var pushpin = new Microsoft.Maps.Pushpin(new Microsoft.Maps.Location(map_item["latitude"], map_item["longitude"]), 
                                                { icon: "images/pushpin_images/pokemon/" + map_item["pokemon_id"] + ".png" });
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
