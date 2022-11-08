// Global varrible declarations
// Limit addition of new ones!

var stateOfZipCodeLayers = true;
var selectedLat;
var selectedLng;
var selectedSize;

function requestFloodData(lat, lng, size) {
    console.log("Attempting to send data to Flask!");
    serverRoute = '/sendPoint';
    payload = JSON.stringify({
        "x": lat,
        "y": lng,
        "size": size
    });

    $.ajax({
        url: serverRoute,
        type: 'POST',
        data: payload,
        success: function(response) {
            requestGeneratedGIF(lat, lng, size);
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function requestGeneratedGIF(lat, lng, size) {
    var serverRoute = '/getGifBounds?lat='+ lat + '&lng=' + lng + '&size=' + size;
    $.ajax({
        url: serverRoute,
        type: 'GET',
        success: function(response) {
            console.log(response);
            topLeftBounds = [response.TL[0], response.TL[1]];
            bottomRightBounds = [response.BR[0], response.BR[1]];
            console.log(topLeftBounds, bottomRightBounds);
            
            var imageUrl = "/getGIF?timestamp=" + new Date().getTime();
            imageBounds = [topLeftBounds, bottomRightBounds];
            L.imageOverlay(imageUrl, imageBounds).addTo(map);
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function changeOpacity(value) {
    $('.leaflet-image-layer').css("opacity" , value);
}

function centerOnLocation(lat, lng){
    map.setView([lat, lng], 13);
}

function selectAddress(zipCode) {
    var geoCodingBaseString = "http://api.positionstack.com/v1/forward?access_key=658f861c60d13e7c19b77473a1d95164&query="
    $.ajax({
        url: geoCodingBaseString + zipCode,
        type: 'GET',
        success: function(response) {
            console.log(response);
            var validAddress = response.data.some(address => {
                if (address.county == 'Delaware County') {
                    centerOnLocation(address.latitude, address.longitude);
                    requestFloodData(address.latitude, address.longitude, 50);
                    return true;
                }
            });
            if (!validAddress) {
                console.log('Invalid address entered');
                alert("The address is outside of Delaware County, please try again.");
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function selectZipCode(zipCode) {
    var zipCodeStatus = verifyZipCode(zipCode);
    if (zipCodeStatus.valid) {
        console.log(`ZIP code ${zipCode} Selected`);
        requestFloodData(zipCodeStatus.lat, zipCodeStatus.lng, zipCodeStatus.size);
    }
    else {
        console.log("ZIP code not supported.");
    }
}

function verifyZipCode(zipCode) {
    const ZipCodes = Object.freeze(makeZipCodeEnum());

    if (ZipCodes.hasOwnProperty(zipCode)) {
        return {
            valid: true,
            lat: ZipCodes.zipCode[0],
            lng: ZipCodes.zipCode[1],
            size: ZipCodes.zipCode[2]
        }
    }
    else {
        return {
            valid: false
        }
    }
}

function makeZipCodeEnum() {
    zipCodeEnum = {}
    const zipCodeArr = [19003, 19008, 19010, 19013, 19014, 19015, 19018, 19022, 19023, 19026, 19029, 19032, 19033, 19036, 19041, 19043, 19050, 19060, 19061, 19063, 19064, 19070, 19073, 19074, 19076, 19078, 19079, 19081, 19082, 19083, 19085, 19086, 19087, 19094, 19096, 19113, 19153, 19312, 19317, 19319, 19342, 19373, 19382];
    zipCodeArr.forEach(function (zipCode) {
        zipCodeEnum[zipCode.toString()] = zipCode;
    });
    return zipCodeEnum;
}

function toggleZipCodeZones() {
    if (stateOfZipCodeLayers) {
        stateOfZipCodeLayers = false;
        removeLayers();
    }
    else {
        stateOfZipCodeLayers = true;
        writeCountyZones();
        //writeZipCodeZones();
    }
}

function removeLayers() {
    map.eachLayer(function(layer) {
        if (!!layer.toGeoJSON) {
        map.removeLayer(layer);
        }
    });
}

function bindLatLongClickToLayers(feature, layer) {
    console.log("layers binded!");
    
    layer.on({
        click: function(evt) {
            //Set lat and long of where user clicked
            selectedLat = evt.latlng.lat;
            selectedLng = evt.latlng.lng;
            selectedSize = 50;
        }
    });
}

function writeCountyZones() {
    var cnty42045 = {fillColor: "#6F763B",weight: 0.5,opacity: 1,color: "white",fillOpacity: 0.5};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/cnty/cnty42045_ls.geojson',function(Data){L.geoJson( Data,{style: cnty42045, onEachFeature: bindLatLongClickToLayers}).bindPopup('Select Location<br><button id="selectLocation" onclick="requestFloodData(selectedLat, selectedLng, selectedSize);">Select</button>', {'maxWidth': '200','className' : 'cnty42045'}).addTo(map);});
}

function writeZipCodeZones() {
    var s19003 = {fillColor: "#544AFD",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19003.geojson',function(Data){L.geoJson( Data,{style: s19003}).bindPopup('Zip Code 19003<br><button onclick="selectZipCode(19003)">Select</button>',{'maxWidth': '200','className' : 'zc19003'}).addTo(map);})
    var s19008 = {fillColor: "#A8756F",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19008.geojson',function(Data){L.geoJson( Data,{style: s19008}).bindPopup('Zip Code 19008<br><button onclick="selectZipCode(19008)">Select</button>',{'maxWidth': '200','className' : 'zc19008'}).addTo(map);})
    var s19010 = {fillColor: "#F5B312",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19010.geojson',function(Data){L.geoJson( Data,{style: s19010}).bindPopup('Zip Code 19010<br><button onclick="selectZipCode(19010)">Select</button>',{'maxWidth': '200','className' : 'zc19010'}).addTo(map);})
    var s19013 = {fillColor: "#323C54",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19013.geojson',function(Data){L.geoJson( Data,{style: s19013}).bindPopup('Zip Code 19013<br><button onclick="selectZipCode(19013)">Select</button>',{'maxWidth': '200','className' : 'zc19013'}).addTo(map);})
    var s19014 = {fillColor: "#1FC0E0",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19014.geojson',function(Data){L.geoJson( Data,{style: s19014}).bindPopup('Zip Code 19014<br><button onclick="selectZipCode(19014)">Select</button>',{'maxWidth': '200','className' : 'zc19014'}).addTo(map);})
    var s19015 = {fillColor: "#74CD9C",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19015.geojson',function(Data){L.geoJson( Data,{style: s19015}).bindPopup('Zip Code 19015<br><button onclick="selectZipCode(19015)">Select</button>',{'maxWidth': '200','className' : 'zc19015'}).addTo(map);})
    var s19018 = {fillColor: "#DBA92A",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19018.geojson',function(Data){L.geoJson( Data,{style: s19018}).bindPopup('Zip Code 19018<br><button onclick="selectZipCode(19018)">Select</button>',{'maxWidth': '200','className' : 'zc19018'}).addTo(map);})
    var s19022 = {fillColor: "#3420E8",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19022.geojson',function(Data){L.geoJson( Data,{style: s19022}).bindPopup('Zip Code 19022<br><button onclick="selectZipCode(19022)">Select</button>',{'maxWidth': '200','className' : 'zc19022'}).addTo(map);})
    var s19023 = {fillColor: "#02CDD1",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19023.geojson',function(Data){L.geoJson( Data,{style: s19023}).bindPopup('Zip Code 19023<br><button onclick="selectZipCode(19023)">Select</button>',{'maxWidth': '200','className' : 'zc19023'}).addTo(map);})
    var s19026 = {fillColor: "#3AC947",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19026.geojson',function(Data){L.geoJson( Data,{style: s19026}).bindPopup('Zip Code 19026<br><button onclick="selectZipCode(19026)">Select</button>',{'maxWidth': '200','className' : 'zc19026'}).addTo(map);})
    var s19029 = {fillColor: "#E24CED",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19029.geojson',function(Data){L.geoJson( Data,{style: s19029}).bindPopup('Zip Code 19029<br><button onclick="selectZipCode(19029)">Select</button>',{'maxWidth': '200','className' : 'zc19029'}).addTo(map);})
    var s19032 = {fillColor: "#AB19AD",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19032.geojson',function(Data){L.geoJson( Data,{style: s19032}).bindPopup('Zip Code 19032<br><button onclick="selectZipCode(19032)">Select</button>',{'maxWidth': '200','className' : 'zc19032'}).addTo(map);})
    var s19033 = {fillColor: "#C50291",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19033.geojson',function(Data){L.geoJson( Data,{style: s19033}).bindPopup('Zip Code 19033<br><button onclick="selectZipCode(19033)">Select</button>',{'maxWidth': '200','className' : 'zc19033'}).addTo(map);})
    var s19036 = {fillColor: "#0F5CA0",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19036.geojson',function(Data){L.geoJson( Data,{style: s19036}).bindPopup('Zip Code 19036<br><button onclick="selectZipCode(19036)">Select</button>',{'maxWidth': '200','className' : 'zc19036'}).addTo(map);})
    var s19041 = {fillColor: "#EA9589",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19041.geojson',function(Data){L.geoJson( Data,{style: s19041}).bindPopup('Zip Code 19041<br><button onclick="selectZipCode(19041)">Select</button>',{'maxWidth': '200','className' : 'zc19041'}).addTo(map);})
    var s19043 = {fillColor: "#D7FE58",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19043.geojson',function(Data){L.geoJson( Data,{style: s19043}).bindPopup('Zip Code 19043<br><button onclick="selectZipCode(19043)">Select</button>',{'maxWidth': '200','className' : 'zc19043'}).addTo(map);})
    var s19050 = {fillColor: "#86D1C6",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19050.geojson',function(Data){L.geoJson( Data,{style: s19050}).bindPopup('Zip Code 19050<br><button onclick="selectZipCode(19050)">Select</button>',{'maxWidth': '200','className' : 'zc19050'}).addTo(map);})
    var s19060 = {fillColor: "#E3E8E8",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19060.geojson',function(Data){L.geoJson( Data,{style: s19060}).bindPopup('Zip Code 19060<br><button onclick="selectZipCode(19060)">Select</button>',{'maxWidth': '200','className' : 'zc19060'}).addTo(map);})
    var s19061 = {fillColor: "#A18A7D",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19061.geojson',function(Data){L.geoJson( Data,{style: s19061}).bindPopup('Zip Code 19061<br><button onclick="selectZipCode(19061)">Select</button>',{'maxWidth': '200','className' : 'zc19061'}).addTo(map);})
    var s19063 = {fillColor: "#04BB2A",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19063.geojson',function(Data){L.geoJson( Data,{style: s19063}).bindPopup('Zip Code 19063<br><button onclick="selectZipCode(19063)">Select</button>',{'maxWidth': '200','className' : 'zc19063'}).addTo(map);})
    var s19064 = {fillColor: "#5C65D5",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19064.geojson',function(Data){L.geoJson( Data,{style: s19064}).bindPopup('Zip Code 19064<br><button onclick="selectZipCode(19064)">Select</button>',{'maxWidth': '200','className' : 'zc19064'}).addTo(map);})
    var s19070 = {fillColor: "#48A2F7",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19070.geojson',function(Data){L.geoJson( Data,{style: s19070}).bindPopup('Zip Code 19070<br><button onclick="selectZipCode(19070)">Select</button>',{'maxWidth': '200','className' : 'zc19070'}).addTo(map);})
    var s19073 = {fillColor: "#FC6B03",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19073.geojson',function(Data){L.geoJson( Data,{style: s19073}).bindPopup('Zip Code 19073<br><button onclick="selectZipCode(19073)">Select</button>',{'maxWidth': '200','className' : 'zc19073'}).addTo(map);})
    var s19074 = {fillColor: "#2B12B9",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19074.geojson',function(Data){L.geoJson( Data,{style: s19074}).bindPopup('Zip Code 19074<br><button onclick="selectZipCode(19074)">Select</button>',{'maxWidth': '200','className' : 'zc19074'}).addTo(map);})
    var s19076 = {fillColor: "#A2FBF3",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19076.geojson',function(Data){L.geoJson( Data,{style: s19076}).bindPopup('Zip Code 19076<br><button onclick="selectZipCode(19076)">Select</button>',{'maxWidth': '200','className' : 'zc19076'}).addTo(map);})
    var s19078 = {fillColor: "#9B8836",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19078.geojson',function(Data){L.geoJson( Data,{style: s19078}).bindPopup('Zip Code 19078<br><button onclick="selectZipCode(19078)">Select</button>',{'maxWidth': '200','className' : 'zc19078'}).addTo(map);})
    var s19079 = {fillColor: "#EDEA80",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19079.geojson',function(Data){L.geoJson( Data,{style: s19079}).bindPopup('Zip Code 19079<br><button onclick="selectZipCode(19079)">Select</button>',{'maxWidth': '200','className' : 'zc19079'}).addTo(map);})
    var s19081 = {fillColor: "#F927CA",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19081.geojson',function(Data){L.geoJson( Data,{style: s19081}).bindPopup('Zip Code 19081<br><button onclick="selectZipCode(19081)">Select</button>',{'maxWidth': '200','className' : 'zc19081'}).addTo(map);})
    var s19082 = {fillColor: "#68BDE8",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19082.geojson',function(Data){L.geoJson( Data,{style: s19082}).bindPopup('Zip Code 19082<br><button onclick="selectZipCode(19082)">Select</button>',{'maxWidth': '200','className' : 'zc19082'}).addTo(map);})
    var s19083 = {fillColor: "#E97983",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19083.geojson',function(Data){L.geoJson( Data,{style: s19083}).bindPopup('Zip Code 19083<br><button onclick="selectZipCode(19083)">Select</button>',{'maxWidth': '200','className' : 'zc19083'}).addTo(map);})
    var s19085 = {fillColor: "#F0DC9F",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19085.geojson',function(Data){L.geoJson( Data,{style: s19085}).bindPopup('Zip Code 19085<br><button onclick="selectZipCode(19085)">Select</button>',{'maxWidth': '200','className' : 'zc19085'}).addTo(map);})
    var s19086 = {fillColor: "#9C3B74",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19086.geojson',function(Data){L.geoJson( Data,{style: s19086}).bindPopup('Zip Code 19086<br><button onclick="selectZipCode(19086)">Select</button>',{'maxWidth': '200','className' : 'zc19086'}).addTo(map);})
    var s19087 = {fillColor: "#501D23",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19087.geojson',function(Data){L.geoJson( Data,{style: s19087}).bindPopup('Zip Code 19087<br><button onclick="selectZipCode(19087)">Select</button>',{'maxWidth': '200','className' : 'zc19087'}).addTo(map);})
    var s19094 = {fillColor: "#29CF49",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19094.geojson',function(Data){L.geoJson( Data,{style: s19094}).bindPopup('Zip Code 19094<br><button onclick="selectZipCode(19094)">Select</button>',{'maxWidth': '200','className' : 'zc19094'}).addTo(map);})
    var s19096 = {fillColor: "#5BE56B",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19096.geojson',function(Data){L.geoJson( Data,{style: s19096}).bindPopup('Zip Code 19096<br><button onclick="selectZipCode(19096)">Select</button>',{'maxWidth': '200','className' : 'zc19096'}).addTo(map);})
    var s19113 = {fillColor: "#FBE40C",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19113.geojson',function(Data){L.geoJson( Data,{style: s19113}).bindPopup('Zip Code 19113<br><button onclick="selectZipCode(19113)">Select</button>',{'maxWidth': '200','className' : 'zc19113'}).addTo(map);})
    var s19153 = {fillColor: "#9F8157",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19153.geojson',function(Data){L.geoJson( Data,{style: s19153}).bindPopup('Zip Code 19153<br><button onclick="selectZipCode(19153)">Select</button>',{'maxWidth': '200','className' : 'zc19153'}).addTo(map);})
    var s19312 = {fillColor: "#3DD9EB",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19312.geojson',function(Data){L.geoJson( Data,{style: s19312}).bindPopup('Zip Code 19312<br><button onclick="selectZipCode(19312)">Select</button>',{'maxWidth': '200','className' : 'zc19312'}).addTo(map);})
    var s19317 = {fillColor: "#B33C09",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19317.geojson',function(Data){L.geoJson( Data,{style: s19317}).bindPopup('Zip Code 19317<br><button onclick="selectZipCode(19317)">Select</button>',{'maxWidth': '200','className' : 'zc19317'}).addTo(map);})
    var s19319 = {fillColor: "#039116",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19319.geojson',function(Data){L.geoJson( Data,{style: s19319}).bindPopup('Zip Code 19319<br><button onclick="selectZipCode(19319)">Select</button>',{'maxWidth': '200','className' : 'zc19319'}).addTo(map);})
    var s19342 = {fillColor: "#D99CDD",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19342.geojson',function(Data){L.geoJson( Data,{style: s19342}).bindPopup('Zip Code 19342<br><button onclick="selectZipCode(19342)">Select</button>',{'maxWidth': '200','className' : 'zc19342'}).addTo(map);})
    var s19373 = {fillColor: "#4BCBC2",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19373.geojson',function(Data){L.geoJson( Data,{style: s19373}).bindPopup('Zip Code 19373<br><button onclick="selectZipCode(19373)">Select</button>',{'maxWidth': '200','className' : 'zc19373'}).addTo(map);})
    var s19382 = {fillColor: "#E44BE9",weight: 0.5,opacity: 1,color: "black",fillOpacity: 0.7};
    $.getJSON('https://s3.amazonaws.com/gm-zdm/gj/zc/US_ZC_19382.geojson',function(Data){L.geoJson( Data,{style: s19382}).bindPopup('Zip Code 19382<br><button onclick="selectZipCode(19382)">Select</button>',{'maxWidth': '200','className' : 'zc19382'}).addTo(map);})
    
    bindLatLongClickToLayers();
}
