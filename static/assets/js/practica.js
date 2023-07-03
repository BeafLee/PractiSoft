var empresaSelect = document.getElementById('empresa');
var ruc = document.getElementById('ruc');
var jefe = document.getElementById('jefe');
empresaSelect.addEventListener('change', function() {
  var empresaSeleccionado = empresaSelect.value;

  var xhr = new XMLHttpRequest();
  xhr.open('GET', '/buscar_empresa_datos?empresa=' + empresaSeleccionado, true);
  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {

    var datos = JSON.parse(xhr.responseText);

    ruc.innerHTML = '';
    ruc.value = datos[0];
    ruc.textContent = datos[0];

    jefe.innerHTML = '';
    jefe.value = datos[1];
    jefe.textContent = datos[1];
    }
  };
  xhr.send();
});