# Procedimietnos del Foso
1. Crear App /foso
2. Crear datos en el backend, admin
    - Materiales
    - Proveedores
    - Destrezas
        I. edicion
        II. mover
        III. retirar
        IV. añadir
3. Creamos las lineas del foso
    - En el admin Foso / Líneas
        Línea 1, Línea 2, Línea 3....
4. Para crear las posiciones ejecutamos:
    - python manage.py crear_posiciones --todas
    - python manage.py crear_posiciones --"Línea 4" ---> por nombre
    - python manage.py crear_posiciones --linea 4   ---> por Id

