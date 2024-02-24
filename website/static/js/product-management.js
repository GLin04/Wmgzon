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
    document.getElementById('total').innerHTML = 'TOTAL = £' + total.toFixed(2);

    document.getElementById('total_hidden').value = total.toFixed(2);

}

function updateQuantity(productId) {
    var quantity = document.getElementById('quantity_' + productId).value;
    var original_quantity = document.getElementById('original_quantity_' + productId).textContent;
    var price = document.getElementById('price_hidden_' + productId).value;
    var prof_installation = document.getElementById('prof_installation_hidden_' + productId).value;
    var update_button = document.getElementById('update_button_' + productId);
    
    prof_installation = (prof_installation === 'true');

    if (quantity != original_quantity) {
        update_button.style.display = 'inline';
    } else {
        update_button.style.display = 'none';
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

function resizeAndPreview(input) {
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
        
        // Set the value of the input file to the data URL of the canvas
        input.value = canvas.toDataURL('image/jpeg');
        
        // Set the value of the hidden input field to the URL
        document.getElementById('image_url').value = input.value;
        alert(input.value);
      };
  
      reader.readAsDataURL(input.files[0]);
      
    }
  }
  
function warn() {
    alert('This product is currently out of stock');
}