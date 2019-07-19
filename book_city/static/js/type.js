// 菜单固定
$(function(){
    //获取要定位元素距离浏览器顶部的距离
    var menuH = $("#book_menu").offset().top;
    // 获取菜单宽度
    var menuW = $("#book_menu").width();
    $(window).scroll(function(){
    //获取滚动条的滑动距离
    var scroH = $(this).scrollTop();
    //滚动条的滑动距离大于等于定位元素距离浏览器顶部的距离，就固定，反之就不固定
    if(scroH>=menuH){
        $("#book_menu").css({"position":"fixed", "top":"0", "width":menuW+"px"});
    }else if(scroH<menuH){
        $("#book_menu").css({"position":"relative"});
    }
})
})