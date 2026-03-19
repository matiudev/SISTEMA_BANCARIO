# ARCHIVO PARA ESCRIBIR:

Comandos 
- git add
- git commit -m "INFORMACION DEL CAMBIO"
- git push origin main
- git pull oirign main (Trae los cambios de los compañeros)

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
- Lo que hay que agregar
- Lo que hay que modificar
- Lo que hay que revisar

Aca vamos escribiendo lo que faltaria para cada uno saber sus tareas y lo que sigue


cambiar logica del sistema:
Generar 2 roles (Cliente y gerente)
3 clases persona, cliente y gerente
Cliente debe ser capaz de ver movimientos de sus cuentas (consulta primero que cuenta quiere ver), ver montos de sus cuentas (consulta que cuenta ver) y ser capaz de transferir a cuentas que esten en la bd
Tambien la tabla de clientes debe contener: id (pk), rut, nombres, apellido, contraseña, contacto, direccion,  

Gerente debe ser capaz: registrar empleados, ver clientes, editar clientes, asginar tipo de cuentas, eliminar clientes, ver cuentas
Tabla 

Validar rut

--MATIAS NO PUDE PROBAR NADA YA QUE LA BASE DE DATO HABIA QUE REINICAR Y NO SABIA XDDD PRUEBALO Y ME INDICAS LOS ERRORES PLOX

18 marzo 2:14
cree las siguientes def en el models cuenta:
registrar_movimiento ---- Funcion auxiliar 
cosultar_saldo ---- Sirve para que cliente y empleado consulten saldos por cuentas
transferir_a_terceros ---- transferencias entre cuentas Corriente/Vista. Valida: saldo suficiente, que la cuenta de origen esté ACTIVA y que el RUT destino exista en la BD
crear_cuenta ---- Permite al empleado asignar cuentas (Corriente, Ahorro, Vista) a clientes existentes
ver_historial_cliente ---- Ahora el cliente puede elegir que cuenta para ver su historial
formato_clp ---- esta def es un auxiliar para formateo del dato a moneda chilena

Cree la tabla transferencias:
LA TABLA DE TRANSFERENCIA TIENE UNA CASILLA DE TIPO_MOVIMIENTO SE DEBE AGREGAR MANUALMENTE LOS TIPOS GIROS Y INGRESOS YA QUE EL SISTEMA NO ESTA PREPARADO PARA ESO

Se modifico el listado de crear cliente con ver listar cliente estaban al reves, ademas cuando se listaban los cliente daba error porque en el menu aparece como c.id pero esta se llama c._id ##corregido 

Se agrego la sanitizacion de rut en una carpeta fuera de models, como utils.sanitizador se ocupo en menu.py cuando se logea y cuando se registra un cliente nuevo estandar chileno

se agrego obenter cuentas por el rut en cuentas 359

Se modifico la conexion de cliente y cuenta, abria 2 veces la conexion y daba error

Se creo en cliente buscar por rut en cliente.py y en cuenta.py 


