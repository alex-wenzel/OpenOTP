if [[ "$VIRTUAL_ENV" != "" ]]
then
  :
else
  echo "venv must be active"
  exit 1
fi

python3 -m pip install $@
python3 -m pip list --format=freeze > requirements.txt