$(document).ready(function(){
//var key = "330288167098249"
var key = $("#mypid").attr('value');
var time = "1369045609"
var pAPI = "http://gsample.pythonanywhere.com/searchermsg?uid="+key+"&time="+time+"&callback=?";

setInterval(function(){
//function fetch() {


$.getJSON( pAPI, {
})
.done(function( data ) {
$('#fetcher').html("");
$.each( data.ids, function( i, item ) {
    $k = $("<h4></h4> <br/>");
    $k.appendTo("#fetcher");
    $k.append(" "+item +" " );
});
});

//}

//fetch();

},10000);
//alert("hi");
//setInterval(
//function () {fetch();}
//,10000);

var pst = "http://gsample.pythonanywhere.com/postme";
//var pst = "http://127.0.0.1:5000/postme"
$("#mybutton").click(function()
{
//e.preventDefault();
$.get(pst, { msg: $("#textbx").val() ,puid:key})
.done(function(data) {
//alert("Data Loaded: " + data);
 data.appendTo("#fetcher");
});
});

});
