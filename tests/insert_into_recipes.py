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
    INSERT INTO recipes (name, instructions, tags) VALUES
    ('Lihapullat', 
     '1. Sekoita jauheliha, sipuli, munat, korppujauhot, mausteet ja suola keskenään.\n\
     2. Muotoile taikinasta lihapullia.\n\
     3. Paista lihapullat pannulla kullanruskeiksi.\n\
     4. Lisää joukkoon tomaattikastiketta ja hauduta hetki.\n\
     5. Tarjoile perunoiden ja puolukkahillon kanssa.',
     NULL),

    ('Kalakeitto', 
     '1. Kiehauta vesi kattilassa ja lisää perunat, porkkanat ja sipulit.\n\
     2. Anna kiehua noin 15 minuuttia.\n\
     3. Lisää kalafileet ja keitä, kunnes kala on kypsää.\n\
     4. Mausta suolalla, pippurilla ja tillillä.\n\
     5. Tarjoile tuoreen leivän kanssa.',
     NULL),

    ('Karjalanpiirakat', 
     '1. Valmista ruisjauhoista taikina lisäämällä vettä ja suolaa.\n\
     2. Kauli taikinasta ohuet levyiksi.\n\
     3. Valmista täyte keittämällä riisiä maidossa ja mausta suolalla.\n\
     4. Levitä riisitä taikinakuorien päälle ja rullaa reunat sisään.\n\
     5. Paista uunissa 220°C:ssa noin 15 minuuttia.\n\
     6. Voitele voilla tarjoilun yhteydessä.',
     NULL),

    ('Paistettu lohi', 
     '1. Mausta lohifileet suolalla ja pippurilla.\n\
     2. Kuumenna pannulla öljyä keskilämmöllä.\n\
     3. Paista lohi molemmin puolin kullanruskeaksi ja kypsäksi, noin 4-5 minuuttia per puoli.\n\
     4. Tarjoile sitruunaviipaleiden ja salaatin kanssa.',
     NULL),

    ('Kasvislasagne', 
     '1. Kuullota sipuli, valkosipuli ja vihannekset (esim. kesäkurpitsa, munakoiso, paprika) pannulla.\n\
     2. Lisää tomaattikastiketta ja mausteita, anna hautua noin 20 minuuttia.\n\
     3. Valmista valkokastike: sulata voi kattilassa, lisää jauhot ja maito vähitellen sekoittaen, kunnes kastike paksuuntuu.\n\
     4. Kokoa lasagne kerroksittain: aluksi kastiketta, sitten lasagnelevyjä, vihannestä ja valkokastiketta.\n\
     5. Ripottele juustoraastetta pinnalle.\n\
     6. Paista uunissa 180°C:ssa noin 30 minuuttia, kunnes pinta on kullanruskea.',
     NULL),

    ('Pinaattipyörykät', 
     '1. Sekoita silputtu pinaatti, fetajuusto, kananmunat, korppujauhot, mausteet ja suola keskenään.\n\
     2. Muotoile taikinasta pieniä pyöryköitä.\n\
     3. Paista pyörykät pannulla öljyssä, kunnes ne ovat kullanruskeita.\n\
     4. Tarjoile jogurttikastikkeen kanssa.',
     NULL),

    ('Marjainen smoothiekulho', 
     '1. Sekoita tehosekoittimessa pakastetut marjat, banaani, jogurtti ja mantelimaito tasaiseksi.\n\
     2. Kaada smoothiet kulhoon.\n\
     3. Koristele esimerkiksi granolalla, tuoreilla marjoilla ja siemenillä.',
     NULL),

    ('Vegaaninen curry', 
     '1. Kuullota sipuli, valkosipuli ja inkivääri pannulla.\n\
     2. Lisää curryjauhe ja paista hetki.\n\
     3. Lisää kikherneet, pinaatti ja kookosmaito.\n\
     4. Anna curryn kiehua, kunnes pinaatti on pehmeää ja maut ovat sekoittuneet.\n\
     5. Tarjoile basmatiriisin kanssa.',
     NULL),

    ('Täysjyvätoast avokadolla', 
     '1. Paahda täysjyväleipäviipaleet kullanruskeiksi.\n\
     2. Muotoile avokadolehti ja levitä se paahdetun leivän päälle.\n\
     3. Mausta suolalla, pippurilla ja sitruunamehulla.\n\
     4. Lisää halutessasi chili-hiutaleita tai punasipulia.',
     NULL),

    ('Hedelmäinen granola', 
     '1. Sekoita kaurahiutaleet, pähkinät, siemenet ja hunaja kulhossa.\n\
     2. Levitä seos uunipellille ja paahda 175°C:ssa noin 20 minuuttia, sekoittaen puolivälissä.\n\
     3. Anna jäähtyä ja sekoita kuivatut hedelmät joukkoon.\n\
     4. Säilytä tiiviissä purkissa ja nauti jogurtin tai maidon kanssa.',
     NULL);

    """
    
    cursor.execute(query)
    connection.commit()

if __name__ == "__main__":
    main()