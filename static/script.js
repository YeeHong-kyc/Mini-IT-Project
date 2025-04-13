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
    
    
    
    if(passwordField == "" || confirmPasswordField == ""){
        alert("Both password are required");
        message.textContent="Both password are required";
        return;
    }
    
    if(passwordField != confirmPasswordField){
        alert("Both passwords must be identical.");
        message.textContent="Both passwords must be identical.";
        return;
    }

    if(passwordField === confirmPasswordField){
         message.textContent = "Password Match";
         message.style.backgroundcolor = "#1dcd59"
    }
    else{
        message.textContent="Password Don't Match!";
        message.style.backgroundcolor ="#ff4d4d"
    }

}
function checkText(){
    console.log(passwordField);
    console.log(confirmPasswordField);
    console.log(submitButton);

    if (passwordField.value && confirmPasswordField.value){
        submitButton.disabled = false
    }else{
        submitButton.disabled = true
    }
}
