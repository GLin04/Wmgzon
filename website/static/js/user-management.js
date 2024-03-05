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
}
