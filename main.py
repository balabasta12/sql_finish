from sqlalchemy import create_engine

engine = create_engine(
    'postgresql://my_46:010203040506@localhost:5432/music_catalog')
connection = engine.connect()

# количество исполнителей в каждом жанре;
count_performers = connection.execute('''
    SELECT genres.title_genres, count(genres_performers.performers_id)
    FROM genres_performers
    JOIN genres ON genres.id = genres_performers.genres_id
    GROUP BY genres.title_genres
    ''').fetchall()

# print(f'Количество исполнителей в каждом жанре: {count_performers}')

# количество треков, вошедших в альбомы 2019-2020 годов;
count_track_06_20 = connection.execute('''
    SELECT albums.name_album, albums.year_of_issue, count(tracks.id)
    FROM Albums
    JOIN tracks ON albums.id = tracks.albums_id
    WHERE albums.year_of_issue >= 2006 AND albums.year_of_issue <= 2020
    GROUP BY albums.name_album, albums.year_of_issue
    ''').fetchall()

# print(f'Количество треков, вошедших в альбомы 2019-2020 годов: {count_track_06_20}')

# средняя продолжительность треков по каждому альбому;
duration_track_average = connection.execute('''
    SELECT  a.name_album, round(AVG(t.track_duration)) 
    FROM Albums a
    JOIN tracks t ON a.id = t.albums_id
    GROUP BY a.name_album
    ''').fetchall()
#round(AVG(t.track_duration)) - стоит тип dp

# print(f'Cредняя продолжительность треков по каждому альбому: {duration_track_average}')

# все исполнители, которые не выпустили альбомы в 2020 году;
performers_album_not_in_20 = connection.execute('''
    SELECT p.name_performers, a.year_of_issue
    FROM performers p
    JOIN albums_performers ap ON p.id = ap.performers_id
    JOIN albums a ON ap.albums_id = a.id
    WHERE a.year_of_issue != 2020
    ''').fetchall()

# print(f'Все исполнители, которые не выпустили альбомы в 2020 году: {performers_album_not_in_20}')

# названия сборников, в которых присутствует конкретный исполнитель (выберите сами);
name_in_collection = connection.execute('''
    SELECT DISTINCT c.name_collectioan
    FROM collection c
    JOIN collection_tracks ct ON c.id = ct.collection_id
    JOIN tracks t ON ct.tracks_id = t.id
    JOIN albums a ON t.albums_id = a.id
    JOIN albums_performers ap ON a.id = ap.albums_id
    JOIN performers p ON ap.performers_id = p.id
    WHERE p.name_performers LIKE 'artist_9'
    ''').fetchall()

# print(f'Названия сборников, в которых присутствует конкретный исполнитель ("artist_9"): {name_in_collection}')

# название альбомов, в которых присутствуют исполнители более 1 жанра;
album_styles = connection.execute('''
     SELECT a.name_album
     FROM albums a
     JOIN albums_performers ap ON a.id = ap.albums_id
     JOIN performers p ON ap.performers_id = p.id
     JOIN genres_performers gp ON p.id = gp.performers_id
     GROUP BY p.name_performers, a.name_album
     HAVING count(gp.genres_id) > 1
    ''').fetchall()

# print(f'Название альбомов, в которых присутствуют исполнители более 1 жанра: {album_styles}')


# наименование треков, которые не входят в сборники;
lonely_track = connection.execute('''
    SELECT t.name_track
    FROM tracks t
    LEFT JOIN collection_tracks ct ON t.id = ct.tracks_id
    where ct.tracks_id IS NULL
    ''').fetchall()

# print(f'Наименование треков, которые не входят в сборники: {lonely_track}')

# исполнителя(-ей), написавшего самый короткий по продолжительности трек
# (теоретически таких треков может быть несколько);
the_shortest_track = connection.execute('''
    SELECT p.name_performers, t.track_duration
    FROM performers p
    JOIN albums_performers ap ON p.id = ap.performers_id
    JOIN albums a ON ap.albums_id = a.id
    JOIN tracks t ON a.id = t.albums_id
    WHERE t.track_duration IN (SELECT MIN(track_duration) FROM tracks)
    ''').fetchall()

# print(f'Исполнителя(-ей), написавшего самый короткий по продолжительности трек : {the_shortest_track}')

# название альбомов, содержащих наименьшее количество треков.
the_shortest_album = connection.execute('''
    SELECT a.name_album, count(t.id)
    FROM albums a
    JOIN tracks t  ON a.id = t.albums_id
    GROUP BY a.name_album 
    HAVING count(t.id) in (
        SELECT count(t.id)
        FROM albums a
        JOIN tracks t  ON a.id = t.albums_id
        GROUP BY a.name_album
        ORDER BY count(t.id)\
        LIMIT 1)
    ''').fetchall()

# print(f'Название альбомов, содержащих наименьшее количество треков : {the_shortest_album}')