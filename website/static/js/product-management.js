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



function warn() {
    alert('This product is currently out of stock');
}