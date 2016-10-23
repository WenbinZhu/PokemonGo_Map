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
        "pokemon_id" : 12,
        "expire" : 1476338470000,
        "latitude" : 32.871181,
        "longitude" : -117.210763
    }
]


//put pokemon image on map
function get_pokemon_layer_from_map_items(map_items) {
    var pushpins = Microsoft.Maps.TestDataGenerator.getPushpins(10, map.getBounds());
    var layer = new Microsoft.Maps.Layer();
    layer.add(pushpins);
    
    return layer;
}

function add_pokemon_layer() {
    var pokemon_layer = get_pokemon_layer_from_map_items(map_items);
    map.layers.insert(pokemon_layer);
}

//add pokemon count down refresh
