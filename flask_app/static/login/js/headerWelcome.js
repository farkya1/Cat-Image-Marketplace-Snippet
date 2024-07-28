
//the welcome variable on the header
var welcome = document.getElementById("welcome-email");

// GET DATA TO SERVER VIA jQuery.ajax({})
jQuery.ajax({
    url: '/getemail',
    type: "GET",
    success:function(returned_data){
          returned_data = JSON.parse(returned_data);

          if( returned_data["email"] != "Unknown")
          {
            
            //gets the email of the sessions
            welcome.innerHTML = "Welcome " + returned_data["email"];
            welcome.style.textAlign = "center";
          }



        }
});