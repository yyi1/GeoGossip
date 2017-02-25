while true
do
	python manage.py delete_stale
	sleep 3600
done

