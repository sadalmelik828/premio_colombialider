$(document).ready(function(){
	// validacion para envio de formulario
	$("#inscripcion").submit(function(){
		if(valida() == false || confirm("La informaci\xf3n ingresada es correcta!\nEsta seguro que desea postularse para el premio de alcaldes y gobernadores incluyentes ?") == false) {
			return false;
		}
	});
	$("#id_tipo_gobernante").change(function(){
		var valor = $(this).val();
		if(valor == 1 || valor == '') {
			$("tr:eq(2)").slideUp();
		} else {
			$("tr:eq(2)").slideDown();
		}
		$("#id_departamento option:eq(0)").attr('selected', true);
		$("#id_municipio :not(option:eq(0))").remove();
	});
	// removiendo todos los municipios
	$("#id_municipio :not(option:eq(0))").remove();
	// funcion que muestra los municipios según el departamento
	$("#id_departamento").change(function(){
		var administracion = $("#id_tipo_gobernante").val()
		var depto_id = $(this).val();
		if(depto_id != "") {
			$.post('/municipios/', { depto_id: depto_id }, function(respuesta) {				
				if(respuesta.length > 0) {
					document.inscripcion.municipio.length = respuesta.length
					for(var i = 0; i < respuesta.length; i++) {
						document.inscripcion.municipio.options[i].value = respuesta[i].id
						document.inscripcion.municipio.options[i].id = respuesta[i].codigo
			            document.inscripcion.municipio.options[i].text = respuesta[i].nombre
					}
				}
			}, 'json');
		} else {
			$("#id_municipio :not(option:eq(0))").remove();
		}
		if(administracion == 1) {
			setTimeout("$('#1').attr('selected', true);", 3000);
		}
	});
	// Habilitar campo "Cúal medio?" si se ha seleccionado la opcion Otro en los medios por los que se enteró de la convocatoria
	$("#id_medio_convocatoria_4").click(function(){
		if($(this).is(":checked")) {
			$("#id_cual_medio").removeAttr("disabled").focus();
		} else {
			$("#id_cual_medio").attr("disabled", true);
		}
	});
});
//*************************
//FUNCIONES
//*************************

// validador de campos vacios
function vacio(q) {
    for ( i = 0; i < q.length; i++ ) {
        if ( q.charAt(i) != " " ) {
            return true;
        }
    }
    return false;
}
// validacion de campos de formulario
function valida() {
	// recoleccion de los valores de cada campo
	var administracion = $("#id_tipo_gobernante").val();
	var departamento = $("#id_departamento").val();
	var municipio = $("#id_municipio").val();
	var nombre = $("#id_nombre").val();
	var telefono = $("#id_tel_fijo").val();
	var cel = $("#id_celular").val();
	var email = $("#id_correo").val();
	var contacto = $("#id_nombre_contacto").val();
	var cargo_contacto = $("#id_cargo_contacto").val();
	var tel_fijo = $("#id_tel_fijo_contacto").val();
	var celular = $("#id_celular_contacto").val();
	var correo = $("#id_correo_contacto").val();
	var carta = $("#id_carta_postulacion").val();
	var medio = $("input[name='medio_convocatoria']").is(":checked");
	var otro = $("#id_medio_convocatoria_4").is(":checked");
	var cual_medio = $("#id_cual_medio").val();
	// validaciones
	if(administracion == "") {
		alert("Es obligatorio seleccionar el tipo de administraci\xf3n para postularse.");
		$("#id_tipo_gobernante").focus();
		return false;	
	}
	if(departamento == "") {
		alert("Es obligatorio seleccionar el departamento.");
		$("#id_departamento").focus();
		return false;	
	}
	if(municipio == "") {
		alert("Es obligatorio seleccionar el municipio.");
		$("#id_municipio").focus();
		return false;	
	}
	if(vacio(nombre) == false) {
		alert("Es obligatorio ingresar el nombre del alcalde o gobernador.");
		$("#id_nombre").css('border-color', 'red').focus();
		return false;
	}
	if(vacio(telefono) == false) {
		alert("Es obligatorio ingresar el n\xfamero de tel\xe9fono fijo del alcalde o gobernador.");
		$("#id_tel_fijo").css('border-color', 'red').focus();
		return false;	
	}
	if(vacio(cel) == false) {
		alert("Es obligatorio ingresar el n\xfamero de tel\xe9fono celular del alcalde o gobernador.");
		$("#id_celular").css('border-color', 'red').focus();
		return false;
	}
	if(vacio(email) == false) {
		alert("Es obligatorio ingresar la direcci\xf3n de correo electr\xf3nico del alcalde o gobernador\nRecuerde que debe terminar en .gov.co.");
		$("#id_correo").css('border-color', 'red').focus();
		return false;	
	} else {
		if(!email.match(/[\w-\.]{3,}@([\w-]{2,}\.)*gov\.co/)){
	        alert('El correo electr\xf3nico que introdujo no es valido.\nPor favor verifique.');
	        $("#id_correo").css('border-color', 'red').focus();
	        return false;
	    }
	}
	if(vacio(contacto) == false) {
		alert("Es obligatorio ingresar el nombre de la persona de contacto.");
		$("#id_nombre_contacto").css('border-color', 'red').focus();
		return false;	
	}
	if(vacio(cargo_contacto) == false) {
		alert("Es obligatorio ingresar el cargo de la persona de contacto.");
		$("#id_cargo_contacto").css('border-color', 'red').focus();
		return false;	
	}
	if(vacio(tel_fijo) == false) {
		alert("Es obligatorio ingresar el n\xfamero de tel\xe9fono fijo de la persona de contacto.");
		$("#id_tel_fijo_contacto").css('border-color', 'red').focus();
		return false;	
	}
	if(vacio(celular) == false) {
		alert("Es obligatorio ingresar el n\xfamero de tel\xe9fono celular de la persona de contacto.");
		$("#id_celular_contacto").css('border-color', 'red').focus();
		return false;	
	}
	if(vacio(correo) == false) {
		alert("Es obligatorio ingresar la direcci\xf3n de correo electr\xf3nico de la persona de contacto.");
		$("#id_correo_contacto").css('border-color', 'red').focus();
		return false;	
	} else {
		// match(/[\w-\.]{3,}@([\w-]{2,}\.)*([\w-]{2,}\.)[\w-]{2,4}/)
		if(!correo.match(/[\w-\.]{3,}@([\w-]{2,}\.)*([\w-]{2,}\.)[\w-]{2,4}/)){
	        alert('El correo electr\xf3nico que introdujo no es valido.\nPor favor verifique.');
	        $("#id_correo_contacto").css('border-color', 'red').focus();
	        return false;
	    }
	}
	if(vacio(carta) == false) {
		alert("Es obligatorio adjuntar la carta de postulaci\xf3n firmada por el gobernador o alcalde.");
		$("#id_carta_postulacion").focus();
		return false;	
	}
	if(medio == false) {
		alert("Es obligatorio seleccionar al menos un medio por el c\xf9al se enter\xf3 de la convocatoria.");
		$("#id_medio_convocatoria_0").focus();
		return false;	
	}
	if(otro == true && vacio(cual_medio) == false) {
		alert("Es obligatorio especificar por c\xfaal otro medio se enter\xf3 de la convocatoria.");
		$("#id_cual_medio").css('border-color', 'red').focus();
		return false;	
	}
}