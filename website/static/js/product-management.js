function deleteProduct(productId) {
    fetch(`/delete_product/${productId}`, {
        method: 'DELETE',
    })
    .then(response => {
        window.location.href = '/electronics'
    })
}

document.getElementById('deleteProductButton').addEventListener('click', function() {
    deleteProduct(productId);
});
