//alert("Conectado")

function checkValue() {
    let checkEstado = document.getElementById("checkEstado")
    let estado = document.getElementById("estado")
    if (checkEstado.value == "A") {
        estado.value = "N"
        checkEstado.value = "N"
    } else {
        estado.value = "A"
        checkEstado.value = "A"
    }

}



// function estadop() {
//     var filas = document.getElementsByTagName("tr");
//     var tabla = document.getElementById("tabla");
//     var numeroFilas = tabla.rows.length;
//     for (var i = 0; i < numeroFilas; i++) {
//       var fila = tabla.rows[i + 1]; // El índice comienza en 0, por lo que la segunda fila tiene el índice 1
//       var celda = fila.cells[6];
//       var celda2 = fila.cells[3];
//       var input = celda.querySelector("input");
//       var valor = input.value;
//       var formulario = document.createElement('form');
//       var input = document.createElement('input');
//       input.setAttribute('type', 'hidden');
//       input.value=valor;
//       input.name = "id";
  
//       var boton = document.createElement("button");
//       formulario.appendChild(input);
//       formulario.appendChild(boton);
//       if (celda2.textContent.includes('No vigente')) {
//         boton.innerText = "Dar Alta";
//         formulario.method = "POST";
//       formulario.action = "/daralta_semestre";
//         celda.appendChild(formulario);
  
//       } else {
//         boton.innerText = "Dar Baja";
//         formulario.method = "POST";
//       formulario.action = "/darbaja_semestre";
//         celda.appendChild(formulario);
  
//       }
//     }
//     alert(numeroFilas);
//   }
//   window.onload = estadop;


// var comboBox = document.getElementById("mostrar");
// comboBox.addEventListener("change", function () {
//     alert("si")
//     var offset = 0
//     var limit = comboBox.value;
//     var pElement = document.getElementById("contador");
//     if (pElement.textContent.includes('1')) {
//         $.ajax({
//             url: "/semestres/b",
//             type: "POST",
//             data: { limit: limit, offset: offset },
//             dataType: "html",
//             success: function (response) {
//                 $("#contenido-dinamico").html(response);
//             }
//         });
//         setTimeout(estadop, 30);
//     } else {
//         contador = 1;
//         pElement.textContent = contador;
//         $.ajax({
//             url: "/semestres/b",
//             type: "POST",
//             data: { limit: limit, offset: 0 },
//             dataType: "html",
//             success: function (response) {
//                 $("#contenido-dinamico").html(response);
//             }
//         });
//         setTimeout(estadop, 30);
//     }
// });