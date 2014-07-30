$(document).ready(function() {
    var visualization = new Visualization("#map", "#range", "#iteration");
    visualization.setData(DATA);
    $("#controls input[type=checkbox]").change(function() {
        var autoUpdate = false;
        if($(this).is(":checked")) {
            autoUpdate = true;
        }
        visualization.setAutoUpdateMapLocation(autoUpdate);
    });
});

