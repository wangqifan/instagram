$(document).ready(function(){

      $(".click-like").click(function(){
             var imageid =  $(this).attr("data")
             $.ajax({
                 "type":"POST",
                 "url":"/like/",
                 "dataType":"json",
                 "data":{
                     "image_id": imageid
                    },
                 "success":function(msg)
                 {
                      $('.like-count-'+imageid).text(msg.message)
                 }
             })
       });

       $(".click-dislike").click(function(){
        var imageid =  $(this).attr("data")
        $.ajax({
            "type":"POST",
            "url":"/dislike/",
            "dataType":"json",
            "data":{
                "image_id": $(this).attr("data")
               },
            "success":function(msg)
            {
                 $('.like-count-'+imageid).text(msg.message)
            }
        })
    });
});