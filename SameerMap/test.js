var map, csv;

require([
  "esri/map", 
  "esri/layers/CSVLayer",
  "esri/Color",
  "esri/symbols/SimpleMarkerSymbol",
  "esri/renderers/SimpleRenderer",
  "esri/InfoTemplate",
  "esri/urlUtils",
  "dojo/domReady!"
], function(
  Map, CSVLayer, Color, SimpleMarkerSymbol, SimpleRenderer, InfoTemplate, urlUtils
) {
  map = new Map("map", {
    basemap: "streets",
    center: [-76.61537781, 39.29164287],
    minZoom: 10,
    zoom: 12
  });
  // csv = new CSVLayer("http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.csv", {
  //   copyright: "USGS.gov"
  // });
  csv = new CSVLayer("./polling_location.csv");
  var orangeRed = new Color([238, 69, 0, 0.5]); // hex is #ff4500
  var marker = new SimpleMarkerSymbol("solid", 15, null, orangeRed);
  var renderer = new SimpleRenderer(marker);
  csv.setRenderer(renderer);
  var template = new InfoTemplate("${type}", "${place}");
  csv.setInfoTemplate(template);
  map.addLayer(csv);
  console.log(csv);
});