$( document ).ready(function() {
    mostrar =document.getElementById("mostrarModal").value
    if (mostrar == "mostrar") {
        $('#menajeModal').modal('toggle')
    }
});