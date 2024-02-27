function checkPassEqual() {
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("passwordConfirm").value;

    if (password !== confirmPassword) {
        alert("Passwords do not match");
        return false;
    }
    return true;
}

function checkFormFilled() {
    alert("checkFormFilled");
    console.log(user_name + email + password + passwordConfirm);
    if (user_name && email && password && passwordConfirm) {
        document.getElementById("register").disabled = true;
    } else {
        document.getElementById("register").disabled = false;
    }
}

function check_fields_filled() {
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const passwordConfirm = document.getElementById('passwordConfirm').value;
    
  
    const register = document.getElementById('register');
  
    // Enable or disable the submit button based on the check
    if (name && email && password && passwordConfirm) {
        register.disabled = false;
    } else {
        register.disabled = true;
    }

    return allFieldsFilled;
}
