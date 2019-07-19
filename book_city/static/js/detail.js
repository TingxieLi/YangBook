$(function (){
    //小屏幕滑轮
    $(window).on("resize", function(){
        let $books = $(".books");
        let parentW = $books.parent().width();
        let $book_list = $(".books .book");
        let totalW = 0;
        $book_list.each(function(){
            totalW += $(this).outerWidth(true);
        });
        if(totalW>parentW){
            $books.css({
                width: totalW + 'px'
            })
        }else{
            $books.removeAttr("style");
        }
    });
    $(window).trigger("resize");

});