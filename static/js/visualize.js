$(document).ready(function() {
    var visualization = new Visualization("#map", "#range", "#iteration");
    visualization.setData(DATA);
    $("#controls input[type=checkbox]").change(function() {
        var autoUpdate = $(this).is(":checked");
        visualization.setAutoUpdateMapLocation(autoUpdate);
    });
});

