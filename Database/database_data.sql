insert into countries (country_id, country_name, r, g, b)
values
	(1, 'French Empire', 60, 150, 247),
	(2, 'Russian Empire', 64, 190, 64),
	(3, 'Great Britain', 255, 60, 60);

insert into infantry (infantry_id, infantry_name, country_id, count, distance, way, error, guard)
values
	(1, 'line_infantry', 1, 90, 160, 100, 9, false),
	(2, 'line_infantry', 2, 90, 160, 110, 10, false),
	(3, 'line_infantry', 3, 90, 170, 100, 10, false),
	(4, 'light_infantry', 1, 60, 210, 100, 6, false),
	(5, 'light_infantry', 2, 60, 210, 110, 7, false),
	(6, 'light_infantry', 3, 60, 220, 100, 7, false),
	(7, 'live_guard', 1, 90, 160, 100, 6, true),
	(8, 'live_guard', 2, 90, 160, 110, 7, true),
	(9, 'live_guard', 3, 90, 170, 100, 7, true);

insert into artillery (artillery_id, artillery_name, country_id, core_distance, core_error, grapeshot_count, grapeshot_error, grapeshot_distance)
values
	(1, '12_pd', 1, 800, 5, 60, 8, 250),
	(2, '12_pd', 2, 800, 4, 50, 8, 250),
	(3, '12_pd', 3, 800, 5, 40, 8, 280);