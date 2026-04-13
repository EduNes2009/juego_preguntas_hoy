import sqlite3
import os

# Buscamos la ruta absoluta para no fallar
base_dir = os.path.dirname(os.path.abspath(__file__))
ruta_db = os.path.join(base_dir, "logic", "data", "preguntas_game.db")

# Si el archivo ya existe, lo borramos para forzar la nueva estructura
if os.path.exists(ruta_db):
    os.remove(ruta_db)
    print("Archivo viejo borrado.")

conn = sqlite3.connect(ruta_db)
cursor = conn.cursor()

print("Creando tabla con columna 'usada'...")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS preguntas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        categoria TEXT NOT NULL,
        pregunta TEXT NOT NULL,
        opcion_a TEXT NOT NULL,
        opcion_b TEXT NOT NULL,
        opcion_c TEXT NOT NULL,
        opcion_d TEXT NOT NULL,
        correcta TEXT NOT NULL,
        imagen TEXT,
        audio TEXT,       
        tipo TEXT,
        puntos INTEGER,
        usada INTEGER DEFAULT 0
    )
''')

# Datos de prueba
datos = [
        # --- CATEGORÍA 1: MUNDO HARRY POTTER ---
        ('HARRY POTTER', '¿Cuál es el verdadero nombre de Lord Voldemort?', 'Tom Riddle', 'Sirius Black', 'Severus Snape', 'Albus Dumbledore', 'Tom Riddle', None, 'texto', 100),
        ('HARRY POTTER', '¿Qué criatura vive en la Cámara de los Secretos?', 'Un dragón', 'Un basilisco', 'Un hipogrifo', 'Un elfo doméstico', 'Un basilisco', None, 'texto', 200),
        ('HARRY POTTER', '¿Cómo se llama el elfo doméstico de los Malfoy?', 'Kreacher', 'Winky', 'Dobby', 'Hokey', 'Dobby', None, 'texto', 300),
        ('HARRY POTTER', '¿Cuál es el patronus de Hermione Granger?', 'Una nutria', 'Un ciervo', 'Un gato', 'Un cisne', 'Una nutria', None, 'texto', 400),
        ('HARRY POTTER', '¿En qué posición juega Harry en Quidditch?', 'Buscador', 'Guardián', 'Golpeador', 'Cazador', 'Buscador', None, 'texto', 500),
        ('HARRY POTTER', '¿Qué objeto es un Horrocrux?', 'La espada de Gryffindor', 'El diario de Riddle', 'La escoba de Harry', 'El mapa del merodeador', 'El diario de Riddle', None, 'texto', 600),
        ('HARRY POTTER', '¿Quién mató a Albus Dumbledore?', 'Voldemort', 'Bellatrix Lestrange', 'Severus Snape', 'Draco Malfoy', 'Severus Snape', None, 'texto', 700),
        ('HARRY POTTER', '¿Cómo se llama el sauce que golpea en Hogwarts?', 'Sauce Boxeador', 'Sauce Llorón', 'Sauce Gritón', 'Sauce Rambla', 'Sauce Boxeador', None, 'texto', 100),
        ('HARRY POTTER', '¿Qué forma tiene el Patronus de Luna Lovegood?', 'Liebre', 'Gato', 'Caballo', 'Zorro', 'Liebre', None, 'texto', 200),
        ('HARRY POTTER', '¿Qué poción otorga suerte líquida?', 'Felix Felicis', 'Multijugos', 'Amortentia', 'Veritaserum', 'Felix Felicis', None, 'texto', 300),
        ('HARRY POTTER', '¿Cuál es el nombre del gato de Hermione?', 'Crookshanks', 'Mrs. Norris', 'Fang', 'Hedwig', 'Crookshanks', None, 'texto', 400),
        ('HARRY POTTER', '¿Qué hechizo abre puertas y ventanas?', 'Alohomora', 'Revelio', 'Lumos', 'Nox', 'Alohomora', None, 'texto', 500),
        ('HARRY POTTER', '¿Quién es el autor de "Animales Fantásticos y dónde encontrarlos"?', 'Newt Scamander', 'Gilderoy Lockhart', 'Beedle el Bardo', 'Bathilda Bagshot', 'Newt Scamander', None, 'texto', 600),
        ('HARRY POTTER', '¿Cuál es la madera de la varita de Harry?', 'Acebo', 'Sauce', 'Roble', 'Tejo', 'Acebo', None, 'texto', 700),
        ('HARRY POTTER', '¿Cómo se llama el hermano de Albus Dumbledore?', 'Aberforth', 'Ariana', 'Percival', 'Gellert', 'Aberforth', None, 'texto', 100),
        ('HARRY POTTER', '¿En qué calle viven los Dursley?', 'Privet Drive', 'Grimmauld Place', 'Spinner’s End', 'Godric’s Hollow', 'Privet Drive', None, 'texto', 200),
        ('HARRY POTTER', '¿Quién es el Príncipe Mestizo?', 'Severus Snape', 'Tom Riddle', 'Harry Potter', 'Draco Malfoy', 'Severus Snape', None, 'texto', 300),
        ('HARRY POTTER', '¿Qué animal es el emblema de la casa Hufflepuff?', 'Tejón', 'Águila', 'Serpiente', 'León', 'Tejón', None, 'texto', 400),
        ('HARRY POTTER', '¿Cómo se llama la prisión de magos custodiada por Dementores?', 'Azkaban', 'Nurmengard', 'Gringotts', 'Hogwarts', 'Azkaban', None, 'texto', 500),
        ('HARRY POTTER', '¿Quién es el padrino de Harry Potter?', 'Sirius Black', 'Remus Lupin', 'Severus Snape', 'Albus Dumbledore', 'Sirius Black', None, 'texto', 600),
        ('HARRY POTTER', '¿Cuál es el núcleo de la varita de Saúco?', 'Pelo de cola de Thestral', 'Pluma de Fénix', 'Fibra de corazón de Dragón', 'Pelo de Unicornio', 'Pelo de cola de Thestral', None, 'texto', 700),
        
        # --- CATEGORÍA 6: MÚSICA ---
        ('MÚSICA','Escucha el fragmento: ¿Quién es el artista de esta canción?','Prince','Elvis Presley','Michael Jackson','David Bowie','Michael Jackson', None, 'billy_jean.mp3', 'musica', 100),
        ('MÚSICA','¿A qué famosa banda británica pertenece esta melodía?','The Rolling Stones','The Beatles','The Who','The Kinks','The Beatles', None, 'yesterday.mp3', 'musica', 200),
        ('MÚSICA','Escucha el solo: ¿Qué instrumento está sonando?','Bajo','Saxofón','Guitarra Eléctrica','Violín','Guitarra Eléctrica', None, 'hendrix_solo.mp3', 'musica', 300),
        ('MÚSICA','Por su sonido, ¿cuántas cuerdas tiene este instrumento estándar?','3','4','5','6','4', None, 'violin_solo.mp3', 'musica', 400),
        ('MÚSICA','¿Qué banda interpreta esta famosa ópera rock?','Queen','The Who','Led Zeppelin','Pink Floyd','Queen', None, 'bohemian_rhapsody.mp3', 'musica', 500),
        ('MÚSICA','¿En qué década nació el género que escuchas?','1950','1940','1960','1970','1950', None, 'rock_and_roll_50s.mp3', 'musica', 600),
        ('MÚSICA','¿Cómo se llama el vocalista que escuchas a continuación?','Bono','The Edge','Sting','Phil Collins','Bono', None, 'u2_vocal.mp3', 'musica', 700),
        ('MÚSICA','¿Qué género musical representa este ritmo?','Reggae','Ska','Rock','Jazz','Reggae', None, 'marley_reggae.mp3', 'musica', 100),
        ('MÚSICA','Escucha la obra: ¿Quién compuso esta sinfonía?','Mozart','Beethoven','Bach','Chopin','Beethoven', None, 'novena_sinfonia.mp3', 'musica', 200),
        ('MÚSICA','¿Qué banda grabó este clásico de los años 70?','The Eagles','The Doors','Pink Floyd','Queen','The Eagles', None, 'hotel_california.mp3', 'musica', 300),
        ('MÚSICA','Escucha la voz: ¿Quién es conocida como la Reina del Soul?','Aretha Franklin','Whitney Houston','Diana Ross','Tina Turner','Aretha Franklin', None, 'respect_aretha.mp3', 'musica', 400),
        ('MÚSICA','¿Qué grupo lideró el movimiento grunge con este tema?','Nirvana','Pearl Jam','Soundgarden','Alice in Chains','Nirvana', None, 'smells_like_spirit.mp3', 'musica', 500),
        ('MÚSICA','¿Quién es el autor y cantante de esta utópica canción?','John Lennon','Paul McCartney','George Harrison','Ringo Starr','John Lennon', None, 'imagine_lennon.mp3', 'musica', 600),
        ('MÚSICA','Escucha el instrumento principal: ¿Cuál es?','Trompeta','Saxofón','Piano','Guitarra','Trompeta', None, 'armstrong_trumpet.mp3', 'musica', 700),
        ('MÚSICA','Este ritmo revolucionó el pop, ¿quién lo interpreta?','Michael Jackson','Prince','Madonna','Stevie Wonder','Michael Jackson', None, 'thriller.mp3', 'musica', 100),
        ('MÚSICA','¿Qué grupo británico interpreta este riff icónico?','The Rolling Stones','The Beatles','The Who','Led Zeppelin','The Rolling Stones', None, 'satisfaction.mp3', 'musica', 200),
        ('MÚSICA','Escucha la voz ¿Quién es?','Elvis Presley','Chuck Berry','Buddy Holly','Little Richard','Elvis Presley', None, 'elvis_rock.mp3', 'musica', 300),
        ('MÚSICA','¿Qué cantante pop interpreta este éxito de los 80?','Madonna','Cher','Cyndi Lauper','Whitney Houston','Madonna', None, 'like_a_virgin.mp3', 'musica', 400),
        ('MÚSICA','¿Qué banda de rock progresivo creó esta atmósfera sonora?','Pink Floyd','Queen','Genesis','Yes','Pink Floyd', None, 'another_brick.mp3', 'musica', 500),
        ('MÚSICA',' ¿Quién compuso este concierto?','Vivaldi','Mozart','Bach','Haydn','Vivaldi', None, 'vivaldi_seasons.mp3', 'musica', 600),
        ('MÚSICA','¿Qué cantante contemporánea interpreta esta balada?','Adele','Amy Winehouse','Lady Gaga','Beyoncé','Adele', None, 'rolling_in_the_deep.mp3', 'musica', 700),

        # --- CATEGORÍA 2: CINE ---
        ('CINE', '¿Quién dirigió la película "Interstellar"?', 'Christopher Nolan', 'Steven Spielberg', 'James Cameron', 'Ridley Scott', 'Christopher Nolan', None, 'texto', 100),
        ('CINE', '¿Qué actor interpreta a Iron Man?', 'Chris Evans', 'Robert Downey Jr.', 'Mark Ruffalo', 'Tom Holland', 'Robert Downey Jr.', None, 'texto', 200),
        ('CINE', '¿Cuál es la primera película de Pixar?', 'Bichos', 'Cars', 'Toy Story', 'Monsters Inc.', 'Toy Story', None, 'texto', 300),
        ('CINE', '¿Cómo se llama el reino de Black Panther?', 'Asgard', 'Genosha', 'Wakanda', 'Themyscira', 'Wakanda', None, 'texto', 400),
        ('CINE', '¿Qué película ganó el Oscar a mejor película en 2020?', '1917', 'Joker', 'Parasite', 'The Irishman', 'Parasite', None, 'texto', 500),
        ('CINE', '¿Quién es el villano en "The Lion King"?', 'Mufasa', 'Scar', 'Zazu', 'Rafiki', 'Scar', None, 'texto', 600),
        ('CINE', '¿En qué año se estrenó Star Wars: A New Hope?', '1975', '1980', '1977', '1982', '1977', None, 'texto', 700),
        ('CINE', '¿Qué actor interpretó a Jack en "Titanic"?', 'Brad Pitt', 'Leonardo DiCaprio', 'Tom Cruise', 'Johnny Depp', 'Leonardo DiCaprio', None, 'texto', 100),
        ('CINE', '¿Cómo se llama el reino congelado en "Frozen"?', 'Arendelle', 'DunBroch', 'Corona', 'Motunui', 'Arendelle', None, 'texto', 200),
        ('CINE', '¿Quién es el director de "Pulp Fiction"?', 'Quentin Tarantino', 'Martin Scorsese', 'Steven Spielberg', 'Francis Ford Coppola', 'Quentin Tarantino', None, 'texto', 300),
        ('CINE', '¿Qué película de terror presenta a una niña llamada Regan?', 'El Exorcista', 'Poltergeist', 'IT', 'Carrie', 'El Exorcista', None, 'texto', 400),
        ('CINE', '¿Cuál es el nombre del protagonista de "Die Hard" (Duro de Matar)?', 'John McClane', 'Ethan Hunt', 'Jason Bourne', 'James Bond', 'John McClane', None, 'texto', 500),
        ('CINE', '¿En qué ciudad transcurre "Batman" (DC Comics)?', 'Metrópolis', 'Gotham City', 'Central City', 'Star City', 'Gotham City', None, 'texto', 600),
        ('CINE', '¿Cómo se llama el sistema de IA en "Iron Man"?', 'JARVIS', 'HAL 9000', 'SIRI', 'ALEXA', 'JARVIS', None, 'texto', 700),
        ('CINE', '¿Qué película animada trata sobre un ogro verde?', 'Shrek', 'Toy Story', 'Madagascar', 'Kung Fu Panda', 'Shrek', None, 'texto', 100),
        ('CINE', '¿Quién es el villano de la película "Halloween"?', 'Michael Myers', 'Jason Voorhees', 'Freddy Krueger', 'Chucky', 'Michael Myers', None, 'texto', 200),
        ('CINE', '¿Cuál es el nombre del droide astromecánico azul y blanco?', 'C-3PO', 'R2-D2', 'BB-8', 'K-2SO', 'R2-D2', None, 'texto', 300),
        ('CINE', '¿Cuál es el nombre del león protagonista en "El Rey León"?', 'Simba', 'Mufasa', 'Scar', 'Kovu', 'Simba', None, 'texto', 400),
        ('CINE', '¿Qué actor interpreta a Jack Sparrow?', 'Johnny Depp', 'Orlando Bloom', 'Brad Pitt', 'Tom Cruise', 'Johnny Depp', None, 'texto', 500),
        ('CINE', '¿Cómo se llama la computadora de "2001: Odisea del Espacio"?', 'HAL 9000', 'R2-D2', 'Jarvis', 'Skynet', 'HAL 9000', None, 'texto', 600),
        ('CINE', '¿Quién dirigió "La Lista de Schindler"?', 'Steven Spielberg', 'Martin Scorsese', 'James Cameron', 'Ridley Scott', 'Steven Spielberg', None, 'texto', 700),
     
        # --- CATEGORÍA 3: GEOGRAFÍA ---
        ('GEOGRAFÍA', '¿Cuál es el río más largo del mundo?', 'Nilo', 'Amazonas', 'Misisipi', 'Yangtsé', 'Amazonas', None, 'texto', 100),
        ('GEOGRAFÍA', '¿En qué continente está Egipto?', 'Asia', 'Europa', 'África', 'Oceanía', 'África', None, 'texto', 200),
        ('GEOGRAFÍA', '¿Cuál es la capital de Italia?', 'Milán', 'Venecia', 'Nápoles', 'Roma', 'Roma', None, 'texto', 300),
        ('GEOGRAFÍA', '¿Qué país tiene forma de bota?', 'Grecia', 'Italia', 'España', 'Portugal', 'Italia', None, 'texto', 400),
        ('GEOGRAFÍA', '¿Dónde se encuentra la Torre Eiffel?', 'Londres', 'Berlín', 'París', 'Madrid', 'París', None, 'texto', 500),
        ('GEOGRAFÍA', '¿Cuál es el océano más grande?', 'Atlántico', 'Índico', 'Ártico', 'Pacífico', 'Pacífico', None, 'texto', 600),
        ('GEOGRAFÍA', '¿Cuál es el monte más alto del mundo?', 'K2', 'Everest', 'Aconcagua', 'Kilimanjaro', 'Everest', None, 'texto', 700),
        ('GEOGRAFÍA', '¿Qué país tiene más población en el mundo?', 'India', 'China', 'EE.UU.', 'Rusia', 'India', None, 'texto', 100),
        ('GEOGRAFÍA', '¿Cuál es la capital de Japón?', 'Kioto', 'Osaka', 'Tokio', 'Hiroshima', 'Tokio', None, 'texto', 200),
        ('GEOGRAFÍA', '¿En qué país se encuentran las Pirámides de Giza?', 'Marruecos', 'Egipto', 'Jordania', 'Turquía', 'Egipto', None, 'texto', 300),
        ('GEOGRAFÍA', '¿Cuál es el desierto más caluroso del mundo?', 'Sahara', 'Atacama', 'Gobi', 'Kalahari', 'Sahara', None, 'texto', 400),
        ('GEOGRAFÍA', '¿Qué cordillera separa Europa de Asia?', 'Urales', 'Alpes', 'Andes', 'Himalaya', 'Urales', None, 'texto', 500),
        ('GEOGRAFÍA', '¿Cuál es la capital de Australia?', 'Sídney', 'Melbourne', 'Canberra', 'Perth', 'Canberra', None, 'texto', 600),
        ('GEOGRAFÍA', '¿Qué país es el más grande del mundo por territorio?', 'Canadá', 'China', 'Rusia', 'Brasil', 'Rusia', None, 'texto', 700),
        ('GEOGRAFÍA', '¿A qué país pertenecen las Islas Galápagos?', 'Ecuador', 'Chile', 'Perú', 'Colombia', 'Ecuador', None, 'texto', 100),
        ('GEOGRAFÍA', '¿Cuál es el país más pequeño del mundo?', 'Mónaco', 'Vaticano', 'San Marino', 'Malta', 'Vaticano', None, 'texto', 200),
        ('GEOGRAFÍA', '¿Qué río pasa por la ciudad de Londres?', 'Támesis', 'Sena', 'Danubio', 'Rin', 'Támesis', None, 'texto', 300),
        ('GEOGRAFÍA', '¿Qué país tiene la mayor cantidad de islas en el mundo?', 'Suecia', 'Noruega', 'Filipinas', 'Indonesia', 'Suecia', None, 'texto', 400),
        ('GEOGRAFÍA', '¿Cuál es la capital de Canadá?', 'Ottawa', 'Toronto', 'Montreal', 'Vancouver', 'Ottawa', None, 'texto', 500),
        ('GEOGRAFÍA', '¿En qué país se encuentra la ciudad de Petra?', 'Jordania', 'Egipto', 'Israel', 'Irak', 'Jordania', None, 'texto', 600),
        ('GEOGRAFÍA', '¿Cuál es el nombre del estrecho que separa España de Marruecos?', 'Gibraltar', 'Magallanes', 'Bósforo', 'Bering', 'Gibraltar', None, 'texto', 700),

        # --- CATEGORÍA 4: CIENCIA ---
        ('CIENCIA', '¿Cuál es el símbolo químico del oro?', 'Ag', 'Fe', 'Au', 'Pb', 'Au', None, 'texto', 100),
        ('CIENCIA', '¿Cuál es el planeta más cercano al Sol?', 'Venus', 'Marte', 'Mercurio', 'Júpiter', 'Mercurio', None, 'texto', 200),
        ('CIENCIA', '¿Qué gas necesitamos para respirar?', 'Nitrógeno', 'Oxígeno', 'Hidrógeno', 'Helio', 'Oxígeno', None, 'texto', 300),
        ('CIENCIA', '¿Quién propuso la teoría de la relatividad?', 'Newton', 'Galileo', 'Einstein', 'Tesla', 'Einstein', None, 'texto', 400),
        ('CIENCIA', '¿Cuál es la velocidad de la luz (aprox)?', '300.000 km/s', '150.000 km/s', '500.000 km/s', '1.000.000 km/s', '300.000 km/s', None, 'texto', 500),
        ('CIENCIA', '¿Cuántos planetas tiene el sistema solar?', '7', '8', '9', '10', '8', None, 'texto', 600),
        ('CIENCIA', '¿Cuál es el órgano más grande del cuerpo?', 'Corazón', 'Hígado', 'Piel', 'Pulmones', 'Piel', None, 'texto', 700),
        ('CIENCIA', '¿Qué planeta es conocido como el Planeta Rojo?', 'Venus', 'Marte', 'Júpiter', 'Saturno', 'Marte', None, 'texto', 100),
        ('CIENCIA', '¿Qué animal es el mamífero más grande?', 'Elefante', 'Ballena Azul', 'Tiburón Blanco', 'Jirafa', 'Ballena Azul', None, 'texto', 200),
        ('CIENCIA', '¿Cuál es el componente principal del sol?', 'Oxígeno', 'Helio', 'Hidrógeno', 'Carbono', 'Hidrógeno', None, 'texto', 300),
        ('CIENCIA', '¿Qué tipo de sangre se considera donante universal?', 'O negativo', 'A positivo', 'AB positivo', 'B negativo', 'O negativo', None, 'texto', 400),
        ('CIENCIA', '¿Quién inventó la bombilla eléctrica?', 'Nikola Tesla', 'Thomas Edison', 'Alexander Bell', 'Benjamin Franklin', 'Thomas Edison', None, 'texto', 500),
        ('CIENCIA', '¿Cuál es la fórmula química del agua?', 'H2O', 'CO2', 'O2', 'NaCl', 'H2O', None, 'texto', 600),
        ('CIENCIA', '¿Cuántos huesos tiene un adulto humano?', '186', '206', '256', '306', '206', None, 'texto', 700),
        ('CIENCIA', '¿Qué planeta tiene anillos visibles más grandes?', 'Neptuno', 'Urano', 'Saturno', 'Júpiter', 'Saturno', None, 'texto', 100),
        ('CIENCIA', '¿Cómo se llama el proceso por el cual las plantas fabrican su alimento?', 'Respiración', 'Digestión', 'Fotosíntesis', 'Osmosis', 'Fotosíntesis', None, 'texto', 200),
        ('CIENCIA', '¿Cuál es el metal líquido a temperatura ambiente?', 'Hierro', 'Plomo', 'Mercurio', 'Cobre', 'Mercurio', None, 'texto', 300),
        ('CIENCIA', '¿Qué planeta tiene la mancha roja gigante?', 'Júpiter', 'Saturno', 'Marte', 'Neptuno', 'Júpiter', None, 'texto', 400),
        ('CIENCIA', '¿Cuál es la principal fuente de energía de la Tierra?', 'El Sol', 'El Viento', 'El Petróleo', 'El Carbón', 'El Sol', None, 'texto', 500),
        ('CIENCIA', '¿Qué gas expulsan los humanos al respirar?', 'Dióxido de Carbono', 'Oxígeno', 'Nitrógeno', 'Metano', 'Dióxido de Carbono', None, 'texto', 600),
        ('CIENCIA', '¿Cómo se llama el centro de un átomo?', 'Núcleo', 'Protón', 'Electrón', 'Neutrón', 'Núcleo', None, 'texto', 700),
        
        # --- CATEGORÍA 5: DEPORTES ---
        ('DEPORTES', '¿Cuántos jugadores tiene un equipo de fútbol?', '10', '12', '11', '9', '11', None, 'texto', 100),
        ('DEPORTES', '¿Cada cuántos años se juega un Mundial?', '2', '3', '4', '5', '4', None, 'texto', 200),
        ('DEPORTES', '¿En qué deporte destaca Roger Federer?', 'Fútbol', 'Tenis', 'Golf', 'Rugby', 'Tenis', None, 'texto', 300),
        ('DEPORTES', '¿Cuál es la distancia de una maratón?', '21 km', '42.195 m', '10 km', '50 km', '42.195 m', None, 'texto', 400),
        ('DEPORTES', '¿Quién es el máximo ganador de Balones de Oro?', 'Cristiano', 'Pelé', 'Maradona', 'Messi', 'Messi', None, 'texto', 500),
        ('DEPORTES', '¿Dónde se originaron los Juegos Olímpicos?', 'Roma', 'Grecia', 'Egipto', 'Francia', 'Grecia', None, 'texto', 600),
        ('DEPORTES', '¿Cuánto dura un partido de básquet (NBA)?', '40 min', '48 min', '60 min', '90 min', '48 min', None, 'texto', 700),
        ('DEPORTES', '¿En qué ciudad se celebraron los JJ.OO. de 2024?', 'Tokio', 'París', 'Los Ángeles', 'Londres', 'París', None, 'texto', 100),
        ('DEPORTES', '¿Cuántos sets debe ganar un hombre en un Grand Slam?', '2', '3', '4', '5', '3', None, 'texto', 200),
        ('DEPORTES', '¿A qué equipo pertenece LeBron James actualmente?', 'Lakers', 'Warriors', 'Celtics', 'Bulls', 'Lakers', None, 'texto', 300),
        ('DEPORTES', '¿Cómo se llama el estadio del Real Madrid?', 'Camp Nou', 'Wanda Metropolitano', 'Santiago Bernabéu', 'Mestalla', 'Santiago Bernabéu', None, 'texto', 400),
        ('DEPORTES', '¿Quién es el ciclista con más Tours de Francia (oficiales)?', 'Eddy Merckx', 'Miguel Induráin', 'Lance Armstrong', 'Chris Froome', 'Miguel Induráin', None, 'texto', 500),
        ('DEPORTES', '¿Qué selección ganó el Mundial de Qatar 2022?', 'Francia', 'Brasil', 'Argentina', 'Alemania', 'Argentina', None, 'texto', 600),
        ('DEPORTES', '¿Cuál es la puntuación máxima en un juego de Bowling?', '100', '200', '300', '400', '300', None, 'texto', 700),
        ('DEPORTES', '¿Cómo se llama el golpe inicial en Golf?', 'Putt', 'Swing', 'Tee off', 'Drive', 'Tee off', None, 'texto', 100),
        ('DEPORTES', '¿Cuántos anillos tiene el logo olímpico?', '4', '5', '6', '7', '5', None, 'texto', 200),
        ('DEPORTES', '¿En qué país nació el fútbol?', 'Brasil', 'Inglaterra', 'Argentina', 'Italia', 'Inglaterra', None, 'texto', 300),
        ('DEPORTES', '¿En qué país se inventó el baloncesto?', 'Estados Unidos', 'Canadá', 'Inglaterra', 'Francia', 'Estados Unidos', None, 'texto', 400),
        ('DEPORTES', '¿Cuántos tiempos tiene un partido de fútbol?', '2', '3', '4', '1', '2', None, 'texto', 500),
        ('DEPORTES', '¿Qué color de jersey usa el líder del Tour de Francia?', 'Amarillo', 'Rosa', 'Verde', 'Blanco', 'Amarillo', None, 'texto', 600),
        ('DEPORTES', '¿Cuál es el estilo de natación más lento?', 'Pecho', 'Crol', 'Espalda', 'Mariposa', 'Pecho', None, 'texto', 700),
       
]


datos_corregidos = []
for fila in datos:
    # Si la fila ya tiene los 11 campos (como las de música)
    if len(fila) == 11:
        datos_corregidos.append(fila)
    # Si tiene 10 (las de texto normal), le agregamos el campo faltante
    elif len(fila) == 10:
        # Convertimos a lista para insertar el campo 'usada' o corregir audio
        f = list(fila)
        # La estructura que espera el INSERT es:
        # (cat, preg, opA, opB, opC, opD, corr, imagen, audio, tipo, puntos)
        
        # Insertamos None en la posición del audio (índice 8) si es texto
        # Tu fila original de texto es: (..., imagen, tipo, puntos)
        # Queremos: (..., imagen, audio, tipo, puntos)
        nueva = (f[0], f[1], f[2], f[3], f[4], f[5], f[6], f[7], None, f[8], f[9])
        datos_corregidos.append(nueva)

# EL TRY DEBE ESTAR AL MISMO NIVEL QUE EL FOR
print("Insertando preguntas...")
try:
    cursor.executemany('''
        INSERT INTO preguntas (
            categoria, pregunta, opcion_a, opcion_b, opcion_c, opcion_d,
            correcta, imagen, audio, tipo, puntos
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', datos_corregidos)

    conn.commit()
    
    # Resetear el estado de 'usada' a 0 para todas
    cursor.execute("UPDATE preguntas SET usada = 0")
    conn.commit()
    
    print(f"✅ ¡Éxito! Se insertaron {len(datos_corregidos)} preguntas.")

except Exception as e:
    print(f"💥 ERROR AL INSERTAR: {e}")

finally:
    conn.close()
    print("Proceso finalizado.")