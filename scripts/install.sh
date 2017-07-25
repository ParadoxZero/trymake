#!/usr/bin/env bash

install() {
    if ! hash python; then
        echo "python is not installed"
        exit 1
    fi

    PYTHON_MAJOR=$(python -c 'import sys; print(sys.version_info[0])')
    PYTHON_MINOR=$(python -c 'import sys; print(sys.version_info[1])')
    if [ $PYTHON_MAJOR -lt 3 ] ; then
        echo "Python Version Not supported"
        exit 1
    fi

    if [ $PYTHON_MINOR -lt 6 ] ; then
        echo "Python Version Not supported"
        exit 1
    fi
    echo "***********************************************"
    echo "* Configuring python                          *"
    echo "***********************************************"
    python --version

    pip install --upgrade pip
    pip install -r requirements.txt

    echo "***********************************************"
    echo "* Configuring Project                         *"
    echo "***********************************************"
    python manage.py makemigrations
    python manage.py migrate
    python manage.py insert_country_data
}

test(){
coverage run --source='.' manage.py test
coverage report
}
remove_data(){
echo "***********************************************"
echo "* Removing Migrations if any                  *"
echo "***********************************************"
bash remove_migrations.sh y
}

if [ $# -lt 1 ]; then
    echo "Missing action"
    exit 1
fi

case $1 in

install)
install
test ;;
remove)
remove_data ;;
test)
test ;;
all)
remove_data
install
test;;

esac