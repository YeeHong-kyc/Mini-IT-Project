var passwordField = document.getElementById("0001").value.trim();
var confirmPasswordField = document.getElementById("0002").value.trim();
var message = document.getElementById("message");
var submitButton = document.getElementById("Submit");


function checkPassword(){
   

    //const password = passwordField.ariaValueMax.trim();
    //const confirmPassword = confirmPasswordField.ariaValueMax.trim();

    console.log(passwordField);
    console.log(confirmPasswordField);
    console.log(passwordField == "");
    console.log(confirmPasswordField == "");
}
    
    
function checkPassword() {
    var pass1 = document.getElementById("0001").value;
    var pass2 = document.getElementById("0002").value;

    if (!pass1 || !pass2) {
        alert("Either Password box or Confirm Password box cannot be null");
        return false; // prevent form submission
    }

    if (pass1 !== pass2) {
        alert("Passwords do not match");
        return false;
    }

    return true; // allow form submission
}

//}
//function checkText(){
//    console.log(passwordField);
//    console.log(confirmPasswordField);
//    console.log(submitButton);
//
//    if (passwordField.value && confirmPasswordField.value){
//        submitButton.disabled = false
//    }else{
//        submitButton.disabled = true
//    }
//}
