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
3. Creamos el foso
    - En Columnas por altura: {"1":9,"2":8,"3":9}
        "1" = altura, 9 = posiciones, "2" = altura, 8 = posiciones...
4. Creamos las lineas que tengamos en el foso
5. Para crear las posiciones ejecutamos:
    - python manage.py crear_posiciones --todas (las que no están creadas, no repite)
    - python manage.py crear_posiciones --foso 1 ---> por Id de foso
    - python manage.py crear_posiciones --linea 4   ---> por Id

