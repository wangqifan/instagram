$(document).ready(function(){
    $("#login").click(function(){
         $.ajax({    
            type:'post',        
            url:'/login/',    
            data:$("#loginform").serialize(),    
            cache:false,    
            dataType:'json'
        });
        return false;
    });
    $("#signup").click(function(){
        alert("123")
        $.ajax({    
           type:'post',        
           url:'/reg/',    
           data:$("#loginform").serialize(),    
           cache:false,    
           dataType:'json'
       });
       return false;
   });
});