$(document).ready(function(){
	
	$("#id_postulacion").submit(function(){
		// variable que verifica si esta cerrando la postulacion
		var cerrada = $("#id_cerrada").is(":checked");
		// Verificacion de las respuestas obligatorias si cierra la postulacion
		if(cerrada) {
			// declaracion de variables
			var vacios = Array();
			var t = 0;
			var af = Array();
			var f = 0;
			// Bucle que revisa cada area de texto
			$("textarea").each(function(){
				if(vacio($(this).val()) == false) {
					$(this).prev("b").remove();
					vacios[t++] = $(this).closest("div").attr("id");
					$(this).before("<b style='color: red;'>* Campo obligatorio.</b>");
				}
			});
			// matriz que guarda los id del div por categoria cuando un area de texto esta vacia
			vacios = $.unique(vacios);
			// Confirmacion de guardado aun con los campos vacios
			if(vacios.length > 0){
				if(confirm("Esta cerrando la postulaci\xf3n, pero existen respuestas que no ha diligenciado en las secciones de:\n"+vacios.join(", ").toUpperCase()+"\nEsta seguro de querer cerrar la postulaci\xf3n sin responder estos campos ?") == false){
					return false;
				}
			}
			// matriz que contiene los id de los input file obligatorios
			var archivos = Array("id_postulacioncriteriorequisito_set-0-anexo", "id_postulacioncriteriorequisito_set-1-anexo", "id_educacion-0-anexo", "id_educacion-6-anexo", "id_mercado-4-anexo", "id_accesibilidad-4-anexo", "id_cultura-1-anexo", "id_cultura-2-anexo", "id_sectores-2-anexo", "id_gestion-0-anexo");			
			// bucle que revisa cada input file obligatorio
			$.each(archivos, function(i, v){
				if($("#"+v).closest("p").children("a").length != 1){
					if($("#"+v).val() == ""){
						$("#"+v).next("b").remove();
						af[f++] = $("#"+v).closest("p").closest("div").attr("id");
						$("#"+v).after("<b style='color: red;'>* Campo obligatorio.</b>");
					}
				}
			});
			// matriz que guarda los id del div por categoria cuando no tiene un soporte obligatorio anexo
			af = $.unique(af);
			// Confirmacion de guardado aun sin los soportes obligatorios
			if(af.length > 0){
				if(confirm("Esta cerrando la postulaci\xf3n, pero no ha anexado algunos soportes obligatorios en las secciones de:\n"+af.join(", ").toUpperCase()+"\nEsta seguro de querer cerrar la postulaci\xf3n sin anexar estos soportes ?") == false){
					return false;
				}
			}
		}
	});
	// mensaje informativo al marcar como cerrada la postulación
	$("#id_cerrada").click(function(){
		if($(this).is(":checked")) {
			$(this).closest("p").next("p").css("display", "inline");
		} else {
			$(this).closest("p").next("p").css("display", "none");
		}
	});
	// Deshabilitacion de todos los campos del formulario si la postulacion se ha guardado como cerrada
	if($("#id_cerrada").is(":checked")){
		$("input, textarea").attr("disabled", true);
		$("input[type='submit']").hide();
	}
});
// **********************
// Funciones
// **********************
// validador de campos vacios
function vacio(q) {
    for ( i = 0; i < q.length; i++ ) {
        if ( q.charAt(i) != " " ) {
            return true;
        }
    }
    return false;
}