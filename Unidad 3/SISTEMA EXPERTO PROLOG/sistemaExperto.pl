% SISTEMA EXPERTO PARA DIAGNOSTICO DE FALLAS DE ENCENDIDO
% Aguilar Recio Jesús Octavio
% Flores Fernandez Emily Karely

:- dynamic sintoma/1.
:- dynamic verificacion/2.
:- use_module(library(readutil)).

% PREDICADO PARA VALIDADCIONES DE ENTRADA

leer_entrada_numero(Mensaje, Min, Max, Opcion) :-
    repeat,
    format('~w (~w-~w): ', [Mensaje, Min, Max]),
    read_line_to_string(user_input, Linea),
    (atom_number(Linea, Opcion), 
     integer(Opcion), 
     Opcion >= Min, 
     Opcion =< Max -> 
        true
    ;
        format('Opcion invalida. Por favor ingrese un numero entre ~w y ~w.~n', [Min, Max]),
        fail
    ).

leer_entrada_sn(Pregunta, Respuesta) :-
    repeat,
    format('~w (s/n): ', [Pregunta]),
    read_line_to_string(user_input, Linea),
    string_lower(Linea, Lower),
    (sub_string(Lower, 0, 1, _, "s") -> Respuesta = si;
     sub_string(Lower, 0, 1, _, "n") -> Respuesta = no;
     (writeln('Respuesta no valida, por favor responda "s" o "n"'), fail)).

% PREDICADO PARA LIMPIAR LA BASE DE CONOCIMIENTOS

limpiar_base_conocimiento :-
    retractall(sintoma(_)),
    retractall(verificacion(_,_)).

% PREDICADO PRINCIPAL INTERFAZ DEL SISTEMA

iniciar_programa :-
    limpiar_base_conocimiento,
    writeln('=== SISTEMA EXPERTO PARA DIAGNOSTICO DE FALLAS DE ENCENDIDO ==='),
    writeln('\nSeleccione el sintoma principal:'),
    writeln('1. No hay sonido al girar la llave'),
    writeln('2. Hay sonido de clic al girar la llave'),
    writeln('3. Motor gira pero no enciende'),
    writeln('4. Hay sonido pero motor no gira'),
    leer_entrada_numero('Ingrese el numero de su opcion', 1, 4, Opcion),
    (Opcion =:= 1 -> assertz(sintoma(no_hay_sonido)), preguntas_no_hay_sonido;
     Opcion =:= 2 -> assertz(sintoma(hay_sonido_clic)), preguntas_hay_sonido_clic;
     Opcion =:= 3 -> assertz(sintoma(motor_gira_pero_no_enciende)), preguntas_motor_gira;
     Opcion =:= 4 -> assertz(sintoma(hay_sonido_motor_no_gira)), preguntas_hay_sonido_motor_no_gira),
    realizar_diagnostico.

preguntar(Pregunta, Hecho) :-
    leer_entrada_sn(Pregunta, Respuesta),
    assertz(verificacion(Hecho, Respuesta)).

% RUTAS DE PREGUNTAS PARA CADA SINTOMA

preguntas_no_hay_sonido :-
    preguntar('¿Las luces del tablero encienden?', luces_tablero_encienden),
    (verificacion(luces_tablero_encienden, si) -> 
        (preguntar('¿El fusible principal esta intacto?', fusible_principal_intacto),
         (verificacion(fusible_principal_intacto, si) -> 
             preguntar('¿El rele de encendido funciona?', rele_encendido_funciona);
             true));
        preguntar('¿Los bornes de la batería estan corroidos/sueltos?', bornes_corroidos)).

preguntas_hay_sonido_clic :-
    preguntar('¿La bateria tiene mas de 3 años?', bateria_mas_de_3_anios),
    (verificacion(bateria_mas_de_3_anios, no) ->
        preguntar('¿El solenoide recibe voltaje?', solenoide_recibe_voltaje);
        true).

preguntas_motor_gira :-
    preguntar('¿Hay olor a gasolina?', olor_a_gasolina),
    (verificacion(olor_a_gasolina, si) -> 
        (preguntar('¿El motor ahoga al arrancar?', motor_ahoga), !)
    ;
        (preguntar('¿Las bujias estan en buen estado?', bujias_buen_estado),
         (verificacion(bujias_buen_estado, si) -> 
             preguntar('¿Hay presion en el riel de combustible?', presion_riel_combustible)
         ;
             true)
        )).

preguntas_hay_sonido_motor_no_gira :-
    preguntar('¿Hay un simbolo de llave/candado en el tablero?', simbolo_llave_tablero),
    (verificacion(simbolo_llave_tablero, no) ->
        preguntar('¿La ECU muestra codigos de error?', ecu_muestra_codigos);
        true).

realizar_diagnostico :-
    writeln('\n=== RESULTADO DEL DIAGNOSTICO ==='),
    (diagnostico(Falla) -> 
        format('Falla detectada: ~w~n~n', [Falla]),
        explicacion(Falla), nl,
        writeln('¿Desea realizar otro diagnostico? (s/n)'),
        leer_entrada_sn('', Respuesta),
        (Respuesta = si -> iniciar_programa; 
         Respuesta = no -> writeln('Gracias por usar el sistema experto.'))
    ;
        writeln('No se pudo determinar la falla con los datos proporcionados.'),
        writeln('¿Desea intentar con otros sintomas? (s/n)'),
        leer_entrada_sn('', Respuesta),
        (Respuesta = si -> iniciar_programa;
         Respuesta = no -> writeln('Gracias por usar el sistema experto.'))
    ).

finalizar_consulta :-
    writeln('\n¿Desea realizar otro diagnostico? (s/n)'),
    leer_entrada_sn('', Respuesta),
    (Respuesta = si -> iniciar_programa; true).

% REGLAS

% Fallas electricas (no hay sonido)
diagnostico('Conexiones de bateria sueltas o corroidas') :-
    sintoma(no_hay_sonido),
    verificacion(luces_tablero_encienden, no),
    verificacion(bornes_corroidos, no).

diagnostico('Bateria descargada o falla interna') :-
    sintoma(no_hay_sonido),
    verificacion(luces_tablero_encienden, no), 
    verificacion(bornes_corroidos, si).

diagnostico('Fusible principal quemado') :-
    sintoma(no_hay_sonido),
    verificacion(luces_tablero_encienden, si),
    verificacion(fusible_principal_intacto, no).

diagnostico('Rele de encendido defectuoso') :-
    sintoma(no_hay_sonido),
    verificacion(luces_tablero_encienden, si),
    verificacion(fusible_principal_intacto, si),
    verificacion(rele_encendido_funciona, no).

diagnostico('Interruptor de encendido o cableado defectuoso') :-
    sintoma(no_hay_sonido),
    verificacion(luces_tablero_encienden, si),
    verificacion(fusible_principal_intacto, si),
    verificacion(rele_encendido_funciona, si).

% Fallas mecanicas / electricas (hay sonido clic)
diagnostico('Bateria debil') :-
    sintoma(hay_sonido_clic),
    verificacion(bateria_mas_de_3_anios, si).

diagnostico('Cableado o rele de arranque defectuoso') :-
    sintoma(hay_sonido_clic),
    verificacion(bateria_mas_de_3_anios, no),
    verificacion(solenoide_recibe_voltaje, no).

diagnostico('Motor de arranque defectuoso') :-
    sintoma(hay_sonido_clic),
    verificacion(bateria_mas_de_3_anios, no),
    verificacion(solenoide_recibe_voltaje, si).

% Fallas combustible / chispa (motor gira pero no enciende)
diagnostico('Exceso de combustible (inyectores o sensor MAF)') :-
    sintoma(motor_gira_pero_no_enciende),
    verificacion(olor_a_gasolina, si),
    verificacion(motor_ahoga, si).

diagnostico('Sensor de cigueñal/arbol de levas defectuoso') :-
    sintoma(motor_gira_pero_no_enciende),
    verificacion(olor_a_gasolina, si),
    verificacion(motor_ahoga, no).

diagnostico('Bujias o bobinas defectuosas') :-
    sintoma(motor_gira_pero_no_enciende),
    verificacion(olor_a_gasolina, no),
    verificacion(bujias_buen_estado, no).

diagnostico('Bomba de combustible o filtro tapado') :-
    sintoma(motor_gira_pero_no_enciende),
    verificacion(olor_a_gasolina, no),
    verificacion(bujias_buen_estado, si),
    verificacion(presion_riel_combustible, no).

diagnostico('Problema de sincronizacion/compresion') :-
    sintoma(motor_gira_pero_no_enciende),
    verificacion(olor_a_gasolina, no),
    verificacion(bujias_buen_estado, si),
    verificacion(presion_riel_combustible, si).

% Fallas electronicas (sonido pero motor no gira)
diagnostico('Inmovilizador activado') :-
    sintoma(hay_sonido_motor_no_gira),
    verificacion(simbolo_llave_tablero, si).

diagnostico('Problema en ECU') :-
    sintoma(hay_sonido_motor_no_gira),
    verificacion(simbolo_llave_tablero, no),
    verificacion(ecu_muestra_codigos, si).

diagnostico('Falla intermitente (cableado)') :-
    sintoma(hay_sonido_motor_no_gira),
    verificacion(simbolo_llave_tablero, no),
    verificacion(ecu_muestra_codigos, no).

% EXPLICACIONES PARA CADA FALLA

explicacion('Conexiones de bateria sueltas o corroidas') :-
    writeln('\nAccion recomendada:'),
    writeln('1. Limpiar bornes de la bateria con agua caliente y bicarbonato'),
    writeln('2. Apretar bien las conexiones'),
    writeln('3. Verificar voltaje de la bateria (debe ser >12.6V)'),
    writeln('4. Aplicar grasa antioxidante en los bornes').

explicacion('Bateria descargada o falla interna') :-
    writeln('\nAccion recomendada:'),
    writeln('1. Cargar la bateria con un cargador adecuado'),
    writeln('2. Si no mantiene carga, reemplazar bateria'),
    writeln('3. Verificar sistema de carga (alternador)'),
    writeln('4. Revisar posibles consumos parasitos').

explicacion('Fusible principal quemado') :-
    writeln('\nAccion recomendada:'),
    writeln('1. Localizar la caja de fusibles (consultar manual del vehiculo)'),
    writeln('2. Identificar y extraer el fusible principal'),
    writeln('3. Verificar visualmente el filamento (quemado = reemplazar)'),
    writeln('4. Investigar causa del sobreconsumo (cortocircuito posible)'),
    writeln('5. Reemplazar con fusible de la misma capacidad').

explicacion('Rele de encendido defectuoso') :-
    writeln('\nAccion recomendada:'),
    writeln('1. Localizar el rele de encendido (consultar diagrama electrico)'),
    writeln('2. Probar con un rele conocido bueno del mismo tipo'),
    writeln('3. Verificar voltaje en los terminales con multimetro'),
    writeln('4. Revisar conexiones y soldaduras en la base del rele'),
    writeln('5. Reemplazar si no hace "clic" al energizarse').

explicacion('Interruptor de encendido o cableado defectuoso') :-
    writeln('\nAccion recomendada:'),
    writeln('1. Verificar voltaje de salida del interruptor en posicion START'),
    writeln('2. Inspeccionar cableado por cortes o daños visibles'),
    writeln('3. Realizar prueba de continuidad en los cables relevantes'),
    writeln('4. Revisar conectores por corrosion o falsos contactos'),
    writeln('5. Probar con llave de repuesto (si aplica)').

explicacion('Bateria debil') :-
    writeln('\nAccion recomendada:'),
    writeln('1. Medir voltaje en reposo (debe ser >12.4V)'),
    writeln('2. Realizar prueba de carga con equipo especializado'),
    writeln('3. Verificar liquido en celdas (si es bateria convencional)'),
    writeln('4. Cargar completamente y volver a probar'),
    writeln('5. Reemplazar si no mantiene carga o tiene mas de 3 años').

explicacion('Cableado o rele de arranque defectuoso') :-
    writeln('\nAcción recomendada:'),
    writeln('1. Verificar continuidad en cables de control del solenoide'),
    writeln('2. Probar voltaje en terminal de control durante arranque'),
    writeln('3. Revisar rele de arranque (intercambiar con otro similar)'),
    writeln('4. Inspeccionar conexiones a tierra del motor de arranque'),
    writeln('5. Reparar o reemplazar cables dañados o relé defectuoso').

explicacion('Motor de arranque defectuoso') :-
    writeln('\nAccion recomendada:'),
    writeln('1. Dar golpes suaves al motor de arranque mientras se intenta arrancar'),
    writeln('2. Verificar consumo de corriente durante arranque (debe ser <200A)'),
    writeln('3. Desmontar y revisar escobillas y conmutador'),
    writeln('4. Probar el motor de arranque en banco'),
    writeln('5. Reemplazar si no gira o hace ruidos anormales').

explicacion('Exceso de combustible (inyectores o sensor MAF)') :-
    writeln('\nAccion recomendada:'),
    writeln('1. Esperar 10 minutos e intentar nuevamente'),
    writeln('2. Verificar lectura del sensor MAF con escaner'),
    writeln('3. Inspeccionar inyectores por goteo'),
    writeln('4. Revisar sensor de temperatura del refrigerante'),
    writeln('5. Limpiar cuerpo de aceleracion y sensor MAF').

explicacion('Sensor de cigueñal/arbol de levas defectuoso') :-
    writeln('\nAccion recomendada:'),
    writeln('1. Leer codigos de falla con escaner OBD2'),
    writeln('2. Verificar señal del sensor con osciloscopio'),
    writeln('3. Inspeccionar conexiones y cableado del sensor'),
    writeln('4. Revisar distancia entre sensor y rueda fonica'),
    writeln('5. Reemplazar sensor si no genera señal adecuada').

explicacion('Bujias o bobinas defectuosas') :-
    writeln('\nAccion recomendada:'),
    writeln('1. Extraer bujias y revisar estado (humedas, quemadas, erosionadas)'),
    writeln('2. Verificar gap de bujias con calibrador'),
    writeln('3. Probar bobinas con multimetro (resistencia primaria/secundaria)'),
    writeln('4. Realizar prueba de chispa en banco'),
    writeln('5. Reemplazar juego completo si es necesario').

explicacion('Bomba de combustible o filtro tapado') :-
    writeln('\nAccion recomendada:'),
    writeln('1. Verificar presion de combustible con manometro'),
    writeln('2. Escuchar bomba al encender contacto (debe zumbar 2-3 segundos)'),
    writeln('3. Reemplazar filtro de combustible si tiene mas de 30,000 km'),
    writeln('4. Inspeccionar conexiones electricas a la bomba'),
    writeln('5. Probar voltaje en terminales de la bomba').

explicacion('Problema de sincronizacion/compresion') :-
    writeln('\nAccion recomendada:'),
    writeln('1. Verificar sincronizacion de distribucion (marcas de tiempo)'),
    writeln('2. Realizar prueba de compresion en todos los cilindros'),
    writeln('3. Inspeccionar cadena/banda de distribucion por saltos'),
    writeln('4. Revisar tensor y guias de la distribucion'),
    writeln('5. Verificar valvulas por fugas o ajuste incorrecto').

explicacion('Inmovilizador activado') :-
    writeln('\nAccion recomendada:'),
    writeln('1. Usar llave original (no copias)'),
    writeln('2. Verificar pila del llavero (si es keyless)'),
    writeln('3. Esperar 10 minutos y reintentar (puede ser protección anti-robos)'),
    writeln('4. Consultar manual para procedimiento de resincronizacion'),
    writeln('5. Llevar a taller autorizado para reprogramacion si persiste').

explicacion('Problema en ECU') :-
    writeln('\nAccion recomendada:'),
    writeln('1. Leer codigos de falla con escaner profesional'),
    writeln('2. Verificar fusibles relacionados con la ECU'),
    writeln('3. Revisar conexiones y terminales del conector ECU'),
    writeln('4. Probar alimentación y tierra de la ECU'),
    writeln('5. Reparar o reprogramar ECU en taller especializado').

explicacion('Falla intermitente (cableado)') :-
    writeln('\nAccion recomendada:'),
    writeln('1. Inspeccionar visualmente cableados principales'),
    writeln('2. Mover cables mientras se intenta arrancar para reproducir falla'),
    writeln('3. Verificar puntos de tierra del sistema electrico'),
    writeln('4. Revisar conectores por corrosión o humedad'),
    writeln('5. Realizar prueba de vibracion para localizar falsos contactos').