$(function(){
    // 修改资料按钮
    $("#modify").click(function(){
        $("#nickname, #address, #mobile, #gender, #save").each(function(){
            $(this).attr("disabled",false);
        })
    })

    // 选择头像预览
    $("#avatar").change(function(){
        $("#img").attr("src",URL.createObjectURL($(this)[0].files[0]));
    });
})