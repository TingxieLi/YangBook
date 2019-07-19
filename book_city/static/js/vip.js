$(function(){
    $("#vip_time label").each(function(){
        $(this).click(function() {
            let price = $(this).children('input').val();
            $("#price").text(price);
        })
    });
});