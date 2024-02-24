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
    var price = document.getElementById('price_hidden_' + productId).value;
    var prof_installation = document.getElementById('prof_installation_hidden_' + productId).value;


    prof_installation = (prof_installation === 'true');

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
        alert('Product updated');
        window.location.href = '/basket'
    })
    
}


function warn() {
    alert('This product is currently out of stock');
}