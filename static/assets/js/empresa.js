var depSelect = document.getElementById('departamento');
var provSelect = document.getElementById('provincia');
var disSelect = document.getElementById('distrito');

depSelect.addEventListener('change', function() {
  var depSeleccionado = depSelect.value;

  var xhr = new XMLHttpRequest();
  xhr.open('GET', '/buscar_prov_dep?departamento=' + depSeleccionado, true);
  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {

      var provincias = JSON.parse(xhr.responseText);

      provSelect.innerHTML = '<option value="value1" selected>Elija una provincia</option>';
      disSelect.innerHTML = '<option value="value1" selected>Elija un distrito</option>';

      for (var i = 0; i < provincias.length; i++) {
        var option = document.createElement('option');
        option.value = provincias[i];
        option.textContent = provincias[i];
        provSelect.appendChild(option);
      }
    }
  };
  xhr.send();
});

provSelect.addEventListener('change', function() {
  var provSeleccionado = provSelect.value;

  var xhr = new XMLHttpRequest();
  xhr.open('GET', '/buscar_dis_prov?provincia=' + provSeleccionado, true);
  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {

      var distritos = JSON.parse(xhr.responseText);

      disSelect.innerHTML = '<option value="value1" selected>Elija un distrito</option>';

      for (var i = 0; i < distritos.length; i++) {
        var option = document.createElement('option');
        option.value = distritos[i][0];
        option.textContent = distritos[i][1];
        disSelect.appendChild(option);
      }
    }
  };
  xhr.send();
});

function habilitarCombos(select) {
  var combo1 = document.getElementById('departamento');
  var combo2 = document.getElementById('provincia');
  var combo3 = document.getElementById('distrito');

  if (select.value == 1) {
    combo1.disabled = false;
    combo2.disabled = false;
    combo3.disabled = false;
    combo1.required = true;
    combo2.required = true;
    combo3.required = true;
  } else {
    combo1.disabled = true;
    combo2.disabled = true;
    combo3.disabled = true;
    combo1.required = false;
    combo2.required = false;
    combo3.required = false;
    combo1.selectedIndex = 0;
    combo2.selectedIndex = 0;
    combo3.selectedIndex = 0;
    combo2.innerHTML = '<option value="">Elija una provincia</option>';
    combo2.selectedIndex = 0;

    combo3.innerHTML = '<option value="">Elija un distrito</option>';
    combo3.selectedIndex = 0;
  }
}

function validarRuc(input) {
  input.value = input.value.replace(/\D/g, '');

  if (input.value.length !== 11) {
    input.setCustomValidity('El número debe tener 11 dígitos');
  } else {
    input.setCustomValidity('');
  }
}

function validarNumero(input) {
  const valor = input.value;
  const numeros = valor.replace(/[^\d()+]/g, '');
  const parentesisBalanceados = validarParentesis(numeros);
  const signoValido = validarSigno(numeros);

  input.value = numeros;

  if (!parentesisBalanceados) {
    input.setCustomValidity('Los paréntesis deben estar balanceados');
  } else if (!signoValido) {
    input.setCustomValidity('El signo "+" solo puede estar al principio');
  } else {
    input.setCustomValidity('');
  }
}

function validarParentesis(numero) {
  const stack = [];

  for (let i = 0; i < numero.length; i++) {
    if (numero[i] === '(') {
      stack.push('(');
    } else if (numero[i] === ')') {
      if (stack.length === 0) {
        return false; 
      }
      stack.pop();
    }
  }
  return stack.length === 0;
}

function validarSigno(numero) {
  if (numero.length > 0 && numero[0] === '+') {
    const resto = numero.slice(1);
    return resto.indexOf('+') === -1;
  }

  return true;
}

function validarCorreo(input) {
  const valor = input.value;

  const correoRegex = /^[^\s@]+@[^\s@]+\.[^\s@]{1,3}(\.[^\s@]{1,2})?$/;

  if (correoRegex.test(valor)) {
    input.setCustomValidity('');
  } else {
    input.setCustomValidity('El correo electrónico no cumple con el formato requerido');
  }
}