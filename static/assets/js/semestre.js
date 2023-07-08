
function checkValue() {
    let checkEstado = document.getElementById("checkEstado")
    let estado = document.getElementById("estado")
    if (checkEstado.value == "V") {
        estado.value = "N"
        checkEstado.value = "N"
    } else {
        estado.value = "V"
        checkEstado.value = "V"
    }

}

