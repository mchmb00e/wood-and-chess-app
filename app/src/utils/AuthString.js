export function isEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

export function isPassword(password) {
  return password.length >= 4;
}
// --- FUNCIONES AUXILIARES (Puedes ponerlas arriba o fuera del export) ---

/**
 * Valida que el RUT sea un "entero plano" (sin puntos ni guion) 
 * y que el dígito verificador coincida con el algoritmo de Módulo 11.
 */
function validarRutChileno(rut) {
  // 1. Convertimos a string por seguridad
  const rutStr = String(rut).trim();

  // 2. Verificar formato: "entero plano" de 8 o 9 dígitos.
  // Nota: Aunque dijiste "entero", en Chile existen RUTs que terminan en 'K'.
  // Esta Regex acepta 7 u 8 dígitos seguidos de un número o una 'K'.
  if (!/^\d{7,8}[\dkK]$/.test(rutStr)) {
    return false;
  }

  // 3. Separar cuerpo y dígito verificador
  const cuerpo = rutStr.slice(0, -1);
  const dv = rutStr.slice(-1).toUpperCase();

  // 4. Algoritmo de Módulo 11
  let suma = 0;
  let multiplo = 2;

  // Recorremos el cuerpo de derecha a izquierda
  for (let i = cuerpo.length - 1; i >= 0; i--) {
    suma += parseInt(cuerpo.charAt(i)) * multiplo;
    
    // El multiplicador varía: 2, 3, 4, 5, 6, 7, 2, 3...
    multiplo = multiplo < 7 ? multiplo + 1 : 2;
  }

  const dvEsperado = 11 - (suma % 11);
  
  // Convertimos el resultado numérico a '0', 'K' o el número como string
  let dvCalculado = '0';
  if (dvEsperado === 11) dvCalculado = '0';
  else if (dvEsperado === 10) dvCalculado = 'K';
  else dvCalculado = dvEsperado.toString();

  return dv === dvCalculado;
}

// --- FUNCIÓN PRINCIPAL ---

export function isDataRegister(data) {
  // Desestructuramos para facilitar la lectura
  const { 
    rut, 
    nombre, 
    apellido, 
    email, 
    telefono, 
    contrasena, 
    verificar_contrasena 
  } = data;

  // 1. VALIDACIÓN DE RUT
  // Verifica largo (8-9) y algoritmo chileno
  const rutValido = validarRutChileno(rut);

  // 2. VALIDACIÓN DE NOMBRE Y APELLIDO
  // Regex: Palabra, espacio opcional, Palabra opcional. 
  // Acepta tildes y ñ (Importante para contexto Chile)
  const nombreRegex = /^[a-zA-ZáéíóúÁÉÍÓÚñÑ]+( [a-zA-ZáéíóúÁÉÍÓÚñÑ]+)?$/;
  
  const nombreValido = nombreRegex.test(nombre);
  const apellidoValido = nombreRegex.test(apellido);

  // 3. VALIDACIÓN DE TELÉFONO
  // Formato: Parte con 9, seguido de 8 dígitos (Total 9)
  const telefonoValido = /^9\d{8}$/.test(telefono);

  // 4. VALIDACIÓN DE EMAIL (Usando tu función existente)
  const emailValido = isEmail(email);

  // 5. VALIDACIÓN DE CONTRASEÑA (Usando tu función existente)
  const passValido = isPassword(contrasena);

  // 6. VALIDACIÓN DE IGUALDAD DE CONTRASEÑAS
  const passIguales = contrasena === verificar_contrasena;

  // --- RESULTADO FINAL ---
  // Retorna true solo si TODAS las condiciones se cumplen
  return (
    rutValido &&
    nombreValido &&
    apellidoValido &&
    telefonoValido &&
    emailValido &&
    passValido &&
    passIguales
  );
}