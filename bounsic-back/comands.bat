# Activar ambiente
venv\Scripts\activate

# Correr
python -m app.main

# Guardar
pip freeze > .\requirements.txt

# Desactivar
deactivate

# Desinstalar
pip freeze > requirements.txt
pip uninstall -y -r requirements.txt