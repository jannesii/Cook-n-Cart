import sqlite3
from typing import List
import os


def main():
    db_path = "cook_and_cart.db"
    db_path = os.path.join(os.getcwd(), "utils", db_path)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    
    query ="""
    INSERT INTO products (name, unit, price_per_unit, category) VALUES
    ('Maito', 'litra', 1.20, 'Maitotuotteet'),
    ('Leipä', 'kpl', 2.50, 'Leivonnaiset'),
    ('Kananmunat', 'kpl', 3.00, 'Maatuotteet'),
    ('Suola', 'kg', 0.80, 'Mausteet'),
    ('Vesi', 'litra', 0.50, 'Juomat'),
    ('Omena', 'kg', 3.00, 'Hedelmät ja vihannekset'),
    ('Kana', 'kg', 5.00, 'Liha ja kala'),
    ('Juusto', 'kg', 8.00, 'Maitotuotteet'),
    ('Tomaatit', 'kg', 2.50, 'Hedelmät ja vihannekset'),
    ('Perunat', 'kg', 1.00, 'Hedelmät ja vihannekset'),
    ('Sokeri', 'kg', 1.50, 'Ruoka-aineet'),
    ('Kylmävesi', 'litra', 0.30, 'Juomat'),
    ('Pasta', 'kg', 1.80, 'Ruoka-aineet'),
    ('Oliiviöljy', 'litra', 4.00, 'Ruoka-aineet'),
    ('Kerma', 'litra', 1.50, 'Maitotuotteet'),
    ('Salaatti', 'kpl', 1.20, 'Hedelmät ja vihannekset'),
    ('Juustolevite', 'litra', 3.50, 'Maitotuotteet'),
    ('Kahvi', 'kg', 12.00, 'Juomat'),
    ('Teetä', 'paketti', 2.50, 'Juomat'),
    ('Riisi', 'kg', 2.00, 'Ruoka-aineet'),
    ('Munakoiso', 'kg', 2.20, 'Hedelmät ja vihannekset'),
    ('Lihamakkara', 'kg', 6.50, 'Liha ja kala'),
    ('Jogurtti', 'kpl', 0.60, 'Maitotuotteet'),
    ('Kookosmaito', 'litra', 2.50, 'Juomat'),
    ('Sitrushedelmät', 'kg', 4.00, 'Hedelmät ja vihannekset'),
    ('Valkosipuli', 'kg', 3.00, 'Mausteet'),
    ('Parsa', 'kpl', 1.80, 'Hedelmät ja vihannekset'),
    ('Hedelmäsmoothie', 'litra', 3.50, 'Juomat'),
    ('Täysjyväleipä', 'kpl', 2.80, 'Leivonnaiset'),
    ('Vegaaninen juusto', 'kg', 9.00, 'Maitotuotteet'),
    ('Luonnonjogurtti', 'kpl', 0.70, 'Maitotuotteet'),
    ('Mangolasi', 'litra', 2.00, 'Juomat'),
    ('Juustokumina', 'paketti', 2.20, 'Mausteet'),
    ('Banaanit', 'kg', 2.80, 'Hedelmät ja vihannekset'),
    ('Sipulit', 'kg', 1.50, 'Hedelmät ja vihannekset'),
    ('Kookosöljy', 'litra', 5.00, 'Ruoka-aineet'),
    ('Sieni', 'kg', 3.50, 'Hedelmät ja vihannekset'),
    ('Tomaattikastike', 'litra', 2.70, 'Ruoka-aineet'),
    ('Maapähkinävoi', 'tölkki', 3.00, 'Leivonnaiset'),
    ('Täysjyväpasta', 'paketti', 1.90, 'Ruoka-aineet'),
    ('Savukala', 'paketti', 4.50, 'Liha ja kala'),
    ('Parsakaali', 'kpl', 2.30, 'Hedelmät ja vihannekset'),
    ('Kaurahiutaleet', 'kg', 1.80, 'Ruoka-aineet'),
    ('Valkoinen sokeri', 'kg', 1.40, 'Ruoka-aineet'),
    ('Kahvipapu', 'kg', 10.00, 'Juomat'),
    ('Appelsiinit', 'kg', 3.20, 'Hedelmät ja vihannekset'),
    ('Täysrasvainen kerma', 'litra', 1.60, 'Maitotuotteet'),
    ('Kinkku', 'kg', 5.50, 'Liha ja kala'),
    ('Bataatit', 'kg', 2.50, 'Hedelmät ja vihannekset'),
    ('Porkkanat', 'kg', 1.30, 'Hedelmät ja vihannekset'),
    ('Hedelmämehu', 'litra', 2.80, 'Juomat'),
    ('Täytetyt tortillat', 'paketti', 3.20, 'Leivonnaiset'),
    ('Soijamaito', 'litra', 2.20, 'Juomat'),
    ('Kikherneet', 'paketti', 1.90, 'Ruoka-aineet'),
    ('Mustikka', 'paketti', 3.00, 'Hedelmät ja vihannekset'),
    ('Valkosuklaa', 'kg', 12.50, 'Leivonnaiset'),
    ('Inkivääri', 'kg', 4.00, 'Mausteet'),
    ('Marjajogurtti', 'kpl', 0.80, 'Maitotuotteet'),
    ('Ruisleipä', 'kpl', 2.60, 'Leivonnaiset'),
    ('Kikatusse', 'litra', 1.50, 'Ruoka-aineet'),
    ('Maissi', 'kpl', 0.90, 'Hedelmät ja vihannekset'),
    ('Vadelmat', 'paketti', 3.50, 'Hedelmät ja vihannekset'),
    ('Sitrusöljy', 'pullo', 6.00, 'Mausteet'),
    ('Pinaatti', 'kpl', 2.10, 'Hedelmät ja vihannekset'),
    ('Vegaaninen maito', 'litra', 2.50, 'Juomat'),
    ('Karamellit', 'paketti', 1.20, 'Makeiset'),
    ('Tattari', 'kg', 2.30, 'Ruoka-aineet'),
    ('Mansikkahillo', 'purkki', 2.80, 'Leivonnaiset'),
    ('Parsakaali', 'kg', 2.50, 'Hedelmät ja vihannekset'),
    ('Vesimeloni', 'kpl', 4.00, 'Hedelmät ja vihannekset'),
    ('Sitruuna', 'kg', 3.00, 'Hedelmät ja vihannekset'),
    ('Hunaja', 'paketti', 3.50, 'Ruoka-aineet'),
    ('Piparit', 'paketti', 1.80, 'Leivonnaiset'),
    ('Basilika', 'kpl', 1.50, 'Mausteet'),
    ('Valkoinen riisi', 'kg', 1.70, 'Ruoka-aineet'),
    ('Kurkku', 'kpl', 1.20, 'Hedelmät ja vihannekset'),
    ('Kastikkeet', 'pullo', 2.60, 'Ruoka-aineet'),
    ('Täysjyvävehnäjauhot', 'kg', 2.10, 'Ruoka-aineet'),
    ('Lämpimät leivokset', 'kpl', 3.00, 'Leivonnaiset'),
    ('Tomusokeri', 'paketti', 1.40, 'Ruoka-aineet'),
    ('Mustapippuri', 'purkki', 1.00, 'Mausteet'),
    ('Tuuntilohi', 'kg', 15.00, 'Liha ja kala'),
    ('Vadelmamehu', 'litra', 3.00, 'Juomat'),
    ('Täysrasvainen maito', 'litra', 1.50, 'Maitotuotteet'),
    ('Lehtikaali', 'kpl', 2.20, 'Hedelmät ja vihannekset'),
    ('Sianliha', 'kg', 6.00, 'Liha ja kala'),
    ('Kikaria', 'kg', 2.40, 'Ruoka-aineet'),
    ('Hapanmaitotuotteet', 'paketti', 2.50, 'Maitotuotteet'),
    ('Metsäsienet', 'kg', 4.50, 'Hedelmät ja vihannekset'),
    ('Vegaaninen jogurtti', 'kpl', 0.90, 'Maitotuotteet'),
    ('Kirsikat', 'paketti', 3.20, 'Hedelmät ja vihannekset'),
    ('Pinaattilevitäytteet', 'paketti', 2.80, 'Ruoka-aineet'),
    ('Munakoisoviipaleet', 'paketti', 2.50, 'Hedelmät ja vihannekset'),
    ('Punajuuri', 'kg', 1.80, 'Hedelmät ja vihannekset'),
    ('Kookos-sokeri', 'kg', 2.00, 'Ruoka-aineet'),
    ('Ruisjauhot', 'kg', 1.90, 'Ruoka-aineet'),
    ('Tomaatit purkki', 'pullo', 1.70, 'Ruoka-aineet'),
    ('Porkkanasalaatti', 'kpl', 2.20, 'Hedelmät ja vihannekset'),
    ('Feta-juusto', 'kg', 7.50, 'Maitotuotteet'),
    ('Kasvisliemi', 'litra', 1.60, 'Ruoka-aineet'),
    ('Pellavansiemenet', 'kg', 3.20, 'Ruoka-aineet'),
    ('Maissijauhot', 'kg', 2.10, 'Ruoka-aineet'),
    ('Kevätsalaatti', 'kpl', 1.50, 'Hedelmät ja vihannekset'),
    ('Mustamauste', 'pullo', 2.80, 'Mausteet'),
    ('Suklaamousse', 'paketti', 3.60, 'Leivonnaiset'),
    ('Sienikastike', 'litra', 2.90, 'Ruoka-aineet'),
    ('Chia-siemenet', 'paketti', 4.00, 'Ruoka-aineet'),
    ('Hedelmäkakku', 'kpl', 3.50, 'Leivonnaiset'),
    ('Kookosjogurtti', 'kpl', 1.20, 'Maitotuotteet'),
    ('Chilikastike', 'pullo', 2.50, 'Mausteet'),
    ('Vihreä tee', 'paketti', 2.00, 'Juomat'),
    ('Kauramaito', 'litra', 1.80, 'Juomat'),
    ('Pellavansiemenleipä', 'kpl', 2.90, 'Leivonnaiset'),
    ('Kasvissosekeitto', 'litra', 2.40, 'Ruoka-aineet'),
    ('Quinoa', 'kg', 4.50, 'Ruoka-aineet'),
    ('Ruisleipä viipale', 'kpl', 2.70, 'Leivonnaiset'),
    ('Tofu', 'paketti', 3.00, 'Liha ja kala'),
    ('Edamame', 'paketti', 2.20, 'Hedelmät ja vihannekset'),
    ('Greippi', 'kg', 3.80, 'Hedelmät ja vihannekset'),
    ('Kurkkuviipaleet', 'paketti', 1.50, 'Hedelmät ja vihannekset'),
    ('Pähkinäsekoitus', 'paketti', 4.00, 'Välipalat'),
    ('Seesaminsiemenet', 'kg', 3.00, 'Ruoka-aineet'),
    ('Valkoviinietikka', 'pullo', 1.80, 'Ruoka-aineet'),
    ('Tuuntilaatikko', 'paketti', 5.50, 'Liha ja kala'),
    ('Bataattiranskalaiset', 'paketti', 2.80, 'Välipalat'),
    ('Hedelmäkirsikka', 'kg', 4.20, 'Hedelmät ja vihannekset'),
    ('Vegaaninen margariini', 'paketti', 2.50, 'Maitotuotteet'),
    ('Herkkusieni', 'kg', 3.60, 'Hedelmät ja vihannekset'),
    ('Paprikajauhe', 'paketti', 1.50, 'Mausteet'),
    ('Hampunsiemenet', 'paketti', 3.00, 'Ruoka-aineet'),
    ('Valkosipulijauhe', 'paketti', 1.20, 'Mausteet'),
    ('Kaalilaatikko', 'kpl', 3.00, 'Hedelmät ja vihannekset'),
    ('Pesto', 'pullo', 2.90, 'Ruoka-aineet'),
    ('Suklaarouhe', 'paketti', 2.50, 'Leivonnaiset'),
    ('Kookoslastut', 'paketti', 3.00, 'Leivonnaiset'),
    ('Vihreät pavut', 'paketti', 2.30, 'Hedelmät ja vihannekset'),
    ('Kikhernepyörykät', 'paketti', 3.50, 'Liha ja kala'),
    ('Täysjyväriisi', 'kg', 2.00, 'Ruoka-aineet'),
    ('Kaurajauhot', 'kg', 1.80, 'Ruoka-aineet'),
    ('Marjaisa myslit', 'paketti', 4.20, 'Välipalat'),
    ('Pinaattipiirakka', 'kpl', 3.80, 'Leivonnaiset'),
    ('Vegaaninen maissileipä', 'kpl', 2.60, 'Leivonnaiset'),
    ('Vadelma-avokado', 'kg', 5.00, 'Hedelmät ja vihannekset'),
    ('Täysjyvätoast', 'kpl', 2.40, 'Leivonnaiset'),
    ('Kookos-suklaa', 'paketti', 3.20, 'Makeiset'),
    ('Kikatusse', 'kg', 1.60, 'Ruoka-aineet'),
    ('Hummus', 'purkki', 2.50, 'Leivonnaiset'),
    ('Valkoinen punajuuri', 'kg', 1.70, 'Hedelmät ja vihannekset'),
    ('Pinaattipiirake', 'kpl', 3.60, 'Leivonnaiset'),
    ('Sitruunajuusto', 'kg', 4.50, 'Maitotuotteet'),
    ('Maitohappokäyneleet', 'paketti', 2.80, 'Maitotuotteet'),
    ('Valkoinen ohra', 'kg', 2.20, 'Ruoka-aineet'),
    ('Vaaleat pavut', 'paketti', 2.00, 'Hedelmät ja vihannekset'),
    ('Vegaaninen maustettu tofu', 'paketti', 3.50, 'Liha ja kala'),
    ('Kookosvähärasvainen', 'paketti', 2.30, 'Maitotuotteet'),
    ('Vihreä salaatti', 'kpl', 1.70, 'Hedelmät ja vihannekset'),
    ('Hedelmäinen granola', 'paketti', 3.80, 'Välipalat'),
    ('Valkoinen suola', 'paketti', 1.00, 'Ruoka-aineet'),
    ('Quinoasalaatti', 'paketti', 4.00, 'Välipalat'),
    ('Maapähkinävoimakset', 'pullo', 2.60, 'Välipalat'),
    ('Kaurainen leipä', 'kpl', 2.50, 'Leivonnaiset'),
    ('Sitrushedelmäsalaatti', 'kpl', 3.00, 'Hedelmät ja vihannekset'),
    ('Vegaaninen proteiinijauhe', 'paketti', 15.00, 'Välipalat'),
    ('Mustaherukkamehu', 'litra', 3.20, 'Juomat'),
    ('Kookosvesi', 'pullo', 1.50, 'Juomat'),
    ('Mansikkajogurtti', 'kpl', 1.10, 'Maitotuotteet'),
    ('Kookoskakku', 'kpl', 3.70, 'Leivonnaiset'),
    ('Valkosuklaamousse', 'paketti', 2.80, 'Leivonnaiset'),
    ('Porkkanamuffinit', 'paketti', 3.50, 'Leivonnaiset'),
    ('Vegaaniset keksit', 'paketti', 2.40, 'Makeiset'),
    ('Valkosipulileipä', 'kpl', 2.90, 'Leivonnaiset'),
    ('Hedelmäsekoitus', 'paketti', 3.00, 'Välipalat'),
    ('Vegaaninen pizza', 'kpl', 5.00, 'Leivonnaiset'),
    ('Sitrusleivos', 'kpl', 3.20, 'Leivonnaiset'),
    ('Kookosjäätelö', 'kpl', 2.50, 'Makeiset'),
    ('Vadelmakiisseli', 'pullo', 2.70, 'Juomat'),
    ('Valkosuklaapatukat', 'paketti', 2.00, 'Makeiset'),
    ('Täysjyväwrapit', 'paketti', 2.80, 'Leivonnaiset'),
    ('Kaurainen tortillaletut', 'paketti', 2.60, 'Leivonnaiset'),
    ('Hedelmäviili', 'kpl', 1.30, 'Maitotuotteet'),
    ('Vegaaniset nakkikastikkeet', 'pullo', 3.00, 'Ruoka-aineet'),
    ('Kookos-sipulikeitto', 'litra', 2.50, 'Ruoka-aineet'),
    ('Hedelmäsalaatti', 'kpl', 2.80, 'Hedelmät ja vihannekset'),
    ('Vegaaninen burgeri', 'paketti', 4.50, 'Liha ja kala'),
    ('Kookoshillo', 'purkki', 3.20, 'Leivonnaiset'),
    ('Hedelmäpirtelö', 'paketti', 2.60, 'Juomat'),
    ('Vegaaninen juustokakku', 'kpl', 4.00, 'Leivonnaiset'),
    ('Valkosipulivoi', 'paketti', 2.20, 'Ruoka-aineet'),
    ('Hedelmäsmoothie-purkki', 'paketti', 2.90, 'Juomat'),
    ('Kaurapuuro', 'paketti', 1.50, 'Ruoka-aineet'),
    ('Mantelimaito', 'litra', 2.80, 'Juomat'),
    ('Soijarouhe', 'paketti', 3.50, 'Proteiinit'),
    ('Seesaminsiemenlevy', 'paketti', 2.20, 'Välipalat'),
    ('Pistasuola', 'kg', 15.00, 'Pähkinät ja siemenet'),
    ('Lakritsi', 'paketti', 1.80, 'Makeiset'),
    ('Vihreä paprika', 'kpl', 1.60, 'Hedelmät ja vihannekset'),
    ('Punainen paprika', 'kpl', 1.60, 'Hedelmät ja vihannekset'),
    ('Keltasipuli', 'kg', 1.40, 'Hedelmät ja vihannekset'),
    ('Valkoinen viinirypäle', 'kg', 3.50, 'Hedelmät ja vihannekset'),
    ('Mansikka', 'paketti', 4.00, 'Hedelmät ja vihannekset'),
    ('Kirsikka', 'paketti', 3.20, 'Hedelmät ja vihannekset'),
    ('Mustikka', 'paketti', 3.50, 'Hedelmät ja vihannekset'),
    ('Karpalomehu', 'litra', 2.90, 'Juomat'),
    ('Appelsiinimehu', 'litra', 2.70, 'Juomat'),
    ('Ananasmehu', 'litra', 3.00, 'Juomat'),
    ('Vesimeloniviipaleet', 'paketti', 2.50, 'Hedelmät ja vihannekset'),
    ('Persikka', 'kg', 3.20, 'Hedelmät ja vihannekset'),
    ('Luomuomena', 'kg', 3.80, 'Hedelmät ja vihannekset'),
    ('Luomukurkku', 'kpl', 1.50, 'Hedelmät ja vihannekset'),
    ('Luomutomaatti', 'kg', 2.70, 'Hedelmät ja vihannekset'),
    ('Luomukaalilaatikko', 'kpl', 3.20, 'Hedelmät ja vihannekset'),
    ('Luomutarjotin', 'paketti', 4.50, 'Hedelmät ja vihannekset'),
    ('Luomukasvikset', 'kg', 4.00, 'Hedelmät ja vihannekset'),
    ('Luomuraejuusto', 'kg', 9.50, 'Maitotuotteet'),
    ('Luomunaamiot', 'paketti', 2.80, 'Välipalat'),
    ('Luomuvoi', 'paketti', 2.50, 'Maitotuotteet'),
    ('Luomumaitoa', 'litra', 1.90, 'Maitotuotteet'),
    ('Luomujogurtti', 'kpl', 0.80, 'Maitotuotteet'),
    ('Luomukauramaito', 'litra', 1.70, 'Juomat'),
    ('Luomukikherneet', 'paketti', 2.00, 'Proteiinit'),
    ('Luomulinsse', 'paketti', 3.00, 'Proteiinit'),
    ('Luomukasvissyö', 'paketti', 3.50, 'Välipalat'),
    ('Luomubataatti', 'kg', 2.40, 'Hedelmät ja vihannekset'),
    ('Luomuporkkanat', 'kg', 1.30, 'Hedelmät ja vihannekset'),
    ('Luomupiparit', 'paketti', 1.80, 'Leivonnaiset'),
    ('Luomusitruuna', 'kg', 3.10, 'Hedelmät ja vihannekset'),
    ('Luomuhunaja', 'paketti', 3.60, 'Ruoka-aineet'),
    ('Luomukaura', 'kg', 1.90, 'Ruoka-aineet'),
    ('Luomuyrttituotteet', 'paketti', 2.50, 'Mausteet'),
    ('Luomusmoothie', 'paketti', 3.00, 'Juomat'),
    ('Luomumarmeladi', 'purkki', 2.80, 'Leivonnaiset'),
    ('Luomuhummus', 'purkki', 2.50, 'Välipalat'),
    ('Luomumargariini', 'paketti', 2.30, 'Maitotuotteet'),
    ('Luomutofu', 'paketti', 3.20, 'Proteiinit'),
    ('Luomukikatusse', 'litra', 1.60, 'Ruoka-aineet'),
    ('Luomuvihreä tee', 'paketti', 2.10, 'Juomat'),
    ('Luomukasvispizza', 'kpl', 5.50, 'Leivonnaiset'),
    ('Luomukasviskeitto', 'litra', 2.50, 'Ruoka-aineet'),
    ('Luomukasvislasagne', 'paketti', 4.00, 'Leivonnaiset'),
    ('Luomukasvistiili', 'paketti', 3.00, 'Ruoka-aineet'),
    ('Luomukasviksalsa', 'purkki', 2.70, 'Mausteet'),
    ('Luomukasvipähkinät', 'paketti', 4.50, 'Pähkinät ja siemenet'),
    ('Luomukasvijogurtti', 'kpl', 1.00, 'Maitotuotteet'),
    ('Luomukasviproteiini', 'paketti', 5.00, 'Proteiinit'),
    ('Luomukasvijauhot', 'kg', 2.20, 'Ruoka-aineet'),
    ('Luomukasvisleipä', 'kpl', 2.80, 'Leivonnaiset'),
    ('Luomukasvisleivät', 'paketti', 3.00, 'Leivonnaiset'),
    ('Luomukasvisgraniitti', 'paketti', 3.20, 'Juomat'),
    ('Luomukasvismakeiset', 'paketti', 2.50, 'Makeiset'),
    ('Luomukasvismuffinit', 'paketti', 3.40, 'Leivonnaiset'),
    ('Luomukasvisgranola', 'paketti', 3.80, 'Välipalat'),
    ('Luomukasviskakku', 'kpl', 4.50, 'Leivonnaiset'),
    ('Luomukasvispasta', 'paketti', 2.70, 'Ruoka-aineet'),
    ('Luomukasvispihvit', 'paketti', 3.60, 'Proteiinit'),
    ('Luomukasvisperunat', 'kg', 1.80, 'Hedelmät ja vihannekset'),
    ('Luomukasvissaali', 'kpl', 1.90, 'Hedelmät ja vihannekset'),
    ('Luomukasvistomaatti', 'kg', 2.70, 'Hedelmät ja vihannekset'),
    ('Luomukasvikeitto', 'litra', 2.60, 'Ruoka-aineet'),
    ('Luomukasvikeittojuusto', 'kg', 7.80, 'Maitotuotteet'),
    ('Luomukasvikastike', 'pullo', 2.40, 'Mausteet'),
    ('Luomukasvikastikkeet', 'paketti', 3.00, 'Mausteet'),
    ('Luomukasvikastikepurkki', 'paketti', 2.50, 'Mausteet'),
    ('Luomukasviskastikkeet', 'paketti', 3.10, 'Mausteet'),
    ('Luomukasvilevitteet', 'paketti', 2.90, 'Mausteet'),
    ('Luomukasvilevitepurkki', 'paketti', 3.00, 'Mausteet'),
    ('Luomukasvileviteseos', 'paketti', 2.80, 'Mausteet'),
    ('Luomukasvissose', 'paketti', 3.20, 'Ruoka-aineet'),
    ('Luomukasvissosekeitto', 'litra', 2.90, 'Ruoka-aineet'),
    ('Luomukasvissosepurkki', 'paketti', 3.50, 'Ruoka-aineet'),
    ('Luomukasvissosepaketti', 'paketti', 4.00, 'Ruoka-aineet'),
    ('Luomukasvissosemix', 'paketti', 3.80, 'Ruoka-aineet'),
    ('Luomukasvissosemixpaketti', 'paketti', 4.20, 'Ruoka-aineet'),
    ('Luomukasvissosemixpurkki', 'paketti', 4.50, 'Ruoka-aineet'),
    ('Luomukasvissosemixpaketti', 'paketti', 4.80, 'Ruoka-aineet'),
    ('Luomukasvissosemixlitra', 'litra', 5.00, 'Ruoka-aineet'),
    ('Luomukasvissosemixkg', 'kg', 5.50, 'Ruoka-aineet'),
    ('Luomukasvissosemixkpl', 'kpl', 6.00, 'Ruoka-aineet'),
    ('Luomukasvissosemixpullo', 'pullo', 5.20, 'Ruoka-aineet'),
    ('Luomukasvissosemixpaketti', 'paketti', 4.70, 'Ruoka-aineet'),
    ('Vegaaninen korvikejuusto', 'paketti', 3.80, 'Maitotuotteet');
    """
    
    cursor.execute(query)
    connection.commit()

if __name__ == "__main__":
    main()