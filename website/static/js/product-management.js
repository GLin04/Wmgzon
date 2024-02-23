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
    var total = quantity * price;
    document.getElementById('total').innerHTML = 'TOTAL = £' + total.toFixed(2);
}

function warn() {
    alert('This product is currently out of stock');
}