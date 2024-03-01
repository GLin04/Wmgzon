 function deleteProduct(productId) {
    fetch(`/delete_product/${productId}`, {
        method: 'DELETE',
    })
    .then(response => {
        window.location.href = '/electronics'
    })
}

function redirectElectronics() {
    window.location.href = '/electronics';
}



function updateQuantity(productId) {
    var quantity = document.getElementById('quantity_' + productId).value;
    var original_quantity = document.getElementById('original_quantity_' + productId).textContent;
    var price = document.getElementById('price_hidden_' + productId).value;
    var prof_installation = document.getElementById('prof_installation_hidden_' + productId).value;
    var update_button = document.getElementById('update_button_' + productId);
    
    prof_installation = (prof_installation === 'true');

    if (quantity != original_quantity) {
        update_button.disabled = false;
    } else {
        update_button.disabled = true;
    }

    if (prof_installation) {
        prof_installation = 40;
    } else {
        prof_installation = 0; 
    }

    var total = ((parseInt(prof_installation) + parseFloat(price)) * parseInt(quantity)).toFixed(2);

    document.getElementById('current_total_' + productId).innerHTML = total;
    document.getElementById('current_quantity_' + productId).innerHTML = quantity;
}

function updateBasket(productId) {
    var quantity = document.getElementById('quantity_' + productId).value;
    var prof_installation = document.getElementById('prof_installation_hidden_' + productId).value;
    var total = document.getElementById('current_total_' + productId).innerHTML;
    

    fetch(`/update_basket?productId=${productId}&quantity=${quantity}&total=${total}`, {
        method: 'PUT',
    })
    .then(response => {
        window.location.href = '/basket'
    })
    
}

function deleteBasket(productId) {
    fetch(`/delete_basket?productId=${productId}`, {
        method: 'DELETE',
    })
    .then(response => {
        window.location.href = '/basket'
    })
}



function preview_image(input) {
    if (input.files && input.files[0]) {
      const reader = new FileReader();
      const img = new Image();
      
      reader.onload = function (e) {
        img.src = e.target.result;
      };
      
      img.onload = function() {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        // Set the width and height to your desired values
        canvas.width = 250;
        canvas.height = 250;
        
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      
        // Set the preview image src to the data URL of the canvas
        document.getElementById('preview').src = canvas.toDataURL('image/jpeg');

        
      };
  
      reader.readAsDataURL(input.files[0]);
      
    }
  }

function check_image_exists(product_image_array) {

    var image = document.getElementById('inputFile').files[0].name;
    for (i in product_image_array) {
        if (image === product_image_array[i]){
            alert(image +' image name already exists, please choose another image');
            submit.disabled = true;
            document.getElementById('inputFile').value = ''; // remove the input file
            break;
        }
        else {
            submit.disabled = false;
        }
    }
}




function check_fields_filled() {
    const name = document.getElementById('name').value;
    const productType = document.getElementById('productType').value;
    const price = document.getElementById('price').value;
    const deliveryTime = document.getElementById('deliveryTime').value;
    const brand = document.getElementById('brand').value;
    const specifications = document.getElementById('specifications').value;
    const description = document.getElementById('description').value;

    const inputFile = document.getElementById('inputFile').value;

    // Check if all fields are filled
    const allFieldsFilled = (
      name && productType && price &&
      deliveryTime && brand && specifications &&
      description
    );
  
    // Get the submit button
    const submitButton = document.getElementById('submit');
  
    // Enable or disable the submit button based on the check
    if (allFieldsFilled && (inputFile || product_image)) {
      submitButton.disabled = false;
    } else {
      submitButton.disabled = true;
    }
}




function check_stock(productId) {
    var quantity = parseInt(document.getElementById('quantity_' + productId).value);
    var stock = parseInt(document.getElementById('stock_hidden_' + productId).value);

    if ((stock < quantity) || !quantity){
        document.getElementById('update_button_' + productId).disabled = true;
        document.getElementById('error_' + productId).removeAttribute('hidden');

        if (stock < quantity) {
            document.getElementById('error_' + productId).innerText = 'Insufficient stock';
        } else {
            document.getElementById('error_' + productId).innerText = 'Please enter a quantity';
        }
    } else {
        document.getElementById('update_button_' + productId).disabled = false;
        document.getElementById('error_' + productId).setAttribute('hidden', true);
    }
}

function calculateTotal() {
    var quantity = document.getElementById('quantity').value;
    var profInstallationHidden = document.getElementById('prof_installation_hidden');
    var profInstallationCheckbox = document.getElementById('prof_installation');
    var total;

    if (profInstallationCheckbox.checked) {
        profInstallationHidden.value = true;
    }else {
        profInstallationHidden.value = false;
    }

    if (document.getElementById('prof_installation').checked) {
        var total = quantity * price + 40 * quantity;
    } else {
        var total = quantity * price;
    }
    document.getElementById('total').innerHTML = 'Total price: £' + total.toFixed(2);

    document.getElementById('total_hidden').value = total.toFixed(2);

}