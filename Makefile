database_clean: ## Clean images, cache, static and database
	# Remove media
	-rm -rf media/images
	-rm -rf media/cache
	-rm -rf static
	-rm -f db.sqlite3
	# Create database
	./manage.py migrate

load_test_data: ## Import fixtures and collect static
	# Import some fixtures. Order is important as JSON fixtures include primary keys
	./manage.py loaddata apps/fixtures/auth.json
	./manage.py loaddata apps/fixtures/child_products.json
	./manage.py oscar_import_catalogue apps/fixtures/*.csv
	./manage.py oscar_import_catalogue_images apps/fixtures/images.tar.gz
	./manage.py oscar_populate_countries --initial-only
	./manage.py loaddata apps/fixtures/pages.json apps/fixtures/ranges.json apps/fixtures/offers.json
	./manage.py loaddata apps/fixtures/orders.json
	./manage.py clear_index --noinput
	./manage.py update_index catalogue
	./manage.py thumbnail_cleanup
	./manage.py collectstatic --noinput
