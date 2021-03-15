function addedSuccess() {
  document.getElementById("demo").innerHTML = "Item added successfully in Cart";
  setTimeout(function() {
    $('#demo').html('');
  }, 3000);
}