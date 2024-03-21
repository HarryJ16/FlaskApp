#importacion
from storeguitar import create_app

# devuelve la instacia de crate_app y la guarda en la variable App
# para ejecutar la apliacaion solo se puede atravez del nombre app.py
if __name__ == '__main__':
        app = create_app()
        app.run()
