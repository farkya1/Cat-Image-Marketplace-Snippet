
//for the number of attempts
var count     = 0;

//the actual attempt location in html
var numberElement = document.getElementById("login-attempts");

var emailNoGood = document.getElementById("email-error");





function checkCredentials(event) {
    // package data in a JSON object
    event.preventDefault();


    var data_d = {'email': 'owner@email.com', 'password': 'password'};

    
    //email from the form
    data_d["email"] = document.getElementsByName("email")[0].value;

    //password from the form
    data_d["password"] = document.getElementsByName("password")[0].value;
    
    // SEND DATA TO SERVER VIA jQuery.ajax({})
    jQuery.ajax({
        url: "/processlogin",
        data: data_d,
        type: "POST",
        success:function(returned_data){
              returned_data = JSON.parse(returned_data);

              //The user is not signed in
              if (returned_data['success'] === 0){
                count += 1;
                numberElement.innerHTML = count;
                document.getElementsByName("email")[0].value = document.getElementsByName("email")[0].ariaPlaceholder;
                document.getElementsByName("password")[0].value = document.getElementsByName("password")[0].ariaPlaceholder;
              }
              
              //The user is not signed in
              else{
                window.location.href = "/home";
                

              }

            }
    });


}

function signupUsers(event) {
  // package data in a JSON object
  event.preventDefault();


  var data_d = {'email': 'owner@email.com', 'password': 'password'};
  console.log("passed");
  
  //email from the form
  data_d["email"] = document.getElementsByName("email")[0].value;

  //password from the form
  data_d["password"] = document.getElementsByName("password")[0].value;
  
  // SEND DATA TO SERVER VIA jQuery.ajax({})
  jQuery.ajax({
      url: "/signupuser",
      data: data_d,
      type: "POST",
      success:function(returned_data){
            returned_data = JSON.parse(returned_data);

            //The user is not signed in
            if (returned_data['success'] === 0){
              document.getElementsByName("email")[0].value = document.getElementsByName("email")[0].ariaPlaceholder;
              document.getElementsByName("password")[0].value = document.getElementsByName("password")[0].ariaPlaceholder;
              emailNoGood.style.display = "block";
            }
            
            //The user is not signed in
            else{
              window.location.href = "/home";
              

            }

          }
  });


}