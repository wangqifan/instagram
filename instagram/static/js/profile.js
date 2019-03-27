
$(document).ready(function(){
    $("#follow").click(function(){
        $.ajax({
            "type":"POST",
            "url":"/follow/",
            "dataType":"json",
            "data":{
                "followID": window.uid
               },
            "success":function(msg)
            {
                window.location.reload()
            }
        })
    })

  $("#unfollow").click(function(){
    $.ajax({
        "type":"POST",
        "url":"/unfollow/",
        "dataType":"json",
        "data":{
            "followID": window.uid
           },
        "success":function(msg)
        {
            window.location.reload()
        }
    })
})
})