$(function (){
    $(window).on("resize", function(){
        let $books = $(".books");
        let parentW = $books.parent().width();
        let totalW = $(".books .type_book:first").outerWidth()*8;
        if(totalW>parentW){
            $books.css({
                width: totalW + 'px'
            })
        }else{
            $books.removeAttr("style");
        }
    })
    $(window).trigger("resize");
})