@ECHO OFF

echo ---------------------------------------------------------------------
echo Build virtual enviroment started...
python --version

echo ---------------------------------------------------------------------
echo Install virtualenv...
python -m pip install --user --disable-pip-version-check virtualenv==20.0.31

echo Creating venv...
python -m venv venv

echo Activating venv...
call venv\Scripts\activate.bat

echo ---------------------------------------------------------------------
echo Upgrading pip version in venv...
python -m pip install --upgrade pip==20.3.3

echo ---------------------------------------------------------------------
echo Installing packages from requirements.txt into venv...
pip install -r requirements.txt

echo ---------------------------------------------------------------------
echo VENV INFO:
python --version
pip --version --disable-pip-version-check
pip list --disable-pip-version-check

echo ---------------------------------------------------------------------
pause