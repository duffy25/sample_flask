/**
 * Created by duffy on 2014/9/22.
 */


//$("#weight").val( "new value" );
$(document).ready(function () {
    $("#weight").keyup(function () {
        var weight = $("#weight").val();
        var result = Number(weight) * Number(2.2046226218488).toFixed(6);
        var res = ( Math.round(result * 100000) / 100000 ).toFixed(5);
        $("#lbs").val(res);
    });

    $("#lbs").keyup(function () {
        var lb = $("#lbs").val();
        var re = Number(lb) * Number(0.4535923699997481).toFixed(6);
        var rr = ( Math.round(re * 100000) / 100000 ).toFixed(5);
        $("#weight").val(rr);
    });
});