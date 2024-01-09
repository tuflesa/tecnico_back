SELECT *
FROM estructura_empresa
JOIN estructura_zona ON estructura_empresa.id = estructura_zona.empresa_id
JOIN estructura_seccion ON estructura_zona.id = estructura_seccion.zona_id
JOIN estructura_equipo ON estructura_seccion.id = estructura_equipo.seccion_id;
