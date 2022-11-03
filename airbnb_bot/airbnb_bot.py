import re
import sqlite3 as sql
import time
from os.path import isfile

# Wir haben in der Sitzung beide gemeinsam an einem Rechner an dem Projekt gearbeitet

location_regex = [
    # first entry in every tuple is a regex for matching user inputs
    # second entry in every tuple is a possible value
    #   for the key neighbourhood_group in our sql file
    (r'(charlottenburg)|(wilmersdorf)', 'Charlottenburg-Wilm.'),
    (r'(friedrichshain)|(kreuzberg)', 'Friedrichshain-Kreuzberg'),
    (r'lichtenberg', 'Lichtenberg'),
    (r'(marzahn)|(Hellersdorf)', 'Marzahn - Hellersdorf'),
    (r'mitte', 'Mitte'),
    (r'neukölln', 'Neukölln'),
    (r'pankow', 'Pankow'),
    (r'reinickendorf', 'Reinickendorf'),
    (r'spandau', 'Spandau'),
    (r'(steglitz)|(zehlendorf)', 'Steglitz - Zehlendorf'),
    (r'(tempelhof)|(schöneberg)', 'Tempelhof - Schöneberg'),
    (r'(treptow)|(köpenick)', 'Treptow - Köpenick')
]


def get_location_from_input(sentence, regex_list=location_regex):
    """
    get valid location names from user input using RegEx
    """
    # iterate through regular expressions and associated values in regex_list
    for regex, value in regex_list:
        match = re.search(regex, sentence)
        if match:
            # if a regex matches the input: return the corresponding value
            return value
    # return None if no regular expression matches the input
    return None


def query_sql(key, value, columns, sql_file):
    """
    Query a sqlite file for entries where "key" has the value "value".
    Return the values corresponding to columns as a list.
    """

    # set up sqlite connection
    conn = sql.connect(sql_file)
    c = conn.cursor()

    # prepare query string
    query_template = 'SELECT {columns} FROM listings WHERE {key} = "{value}"'
    columns_string = ', '.join(columns)  # e.g. [location, price] -> 'location, price'
    # replace the curly brackets in query_template with the corresponding info
    query = query_template.format(columns=columns_string, key=key, value=value)

    # execute query
    r = c.execute(query)
    # get results as list
    results = r.fetchall()

    # close connection
    conn.close()

    return results

# Leon Holuch & Jonas Hillen - begin #
def ask_for_neighbourhoods():
    # print available neighbourhoods
    neighbourhoods = [
        'Charlottenburg-Wilm.', 'Friedrichshain-Kreuzberg',
        'Lichtenberg', 'Marzahn - Hellersdorf', 'Mitte', 'Neukölln', 'Pankow',
        'Reinickendorf', 'Spandau', 'Steglitz - Zehlendorf',
        'Tempelhof - Schöneberg', 'Treptow - Köpenick']
    print('Wir haben Appartements in folgenden Stadtteilen:')
    print(', '.join(neighbourhoods))

    # get query from user
    sentence = input('\nWo möchtest du denn übernachten?\n')
    # normalize to lowercase
    return sentence.lower()


def ask_for_result_number():
    u_input = input('\nWie viele Ergebnisse möchtest du sehen?\n')

    try:
        u_int = int(u_input)
    except ValueError:
        print('Leider ist die Eingabe von "' + u_input + '" keine Zahl!\n')
        u_int = 10

    return u_int
# Leon Holuch & Jonas Hillen - end #

# Leon Holuch - begin #
def ask_for_price():
    u_input = input('\nWie teuer sollen die Wohnungen maximal sein?\n')

    try:
        u_int = int(u_input)
    except ValueError:
        print('Leider ist die Eingabe von "' + u_input + '"keine Zahl!\nWir zeigen dir alle Ergebnisse!\n')
        u_int = 999999

    return u_int
# Leon Holuch - end #

# Jonas Hillen - begin #
def ask_for_nights():
    u_input = input('\nWie viele Nächte möchtest du bleiben?\n')

    try:
        u_int = int(u_input)
    except ValueError:
        print('Leider ist die Eingabe von "' + u_input + '" keine Zahl!\nWir zeigen alle Ergebnisse!\n')
        u_int = 1

    return u_int
# Jonas Hillen - end #

def airbnb_bot(sql_file, top_n):
    """
    find flats in a given location.

    main steps:
    1) get input sentence from the user; normalize upper/lowercase
    2) extract the location name from the user input
    3) query sql_file for flats in the given location
    4) print the top_n results
    """

    # (Step 0: make sure sql_file exists)
    if not isfile(sql_file):
        # raise an error if the file is not found
        raise FileNotFoundError(
            'Die Datei {} konnte nicht gefunden werden!'.format(sql_file)
        )

# Leon Holuch & Jonas Hillen - begin #
    # ask for neighbourhood till we get a location
    while True:
        # ask for neighbourhoods
        sentence = ask_for_neighbourhoods()

        # extract location from user input
        location = get_location_from_input(sentence)

        if location is None:
            # if the user input doesn't contain valid location information:
            # apologize & quit
            print('\nEntschuldigung, das habe ich leider nicht verstanden...\nVersuchen wir es nochmal!\n')
        else:
            break
# Leon Holuch - begin #
    # ask for maximum price #
    price_m = ask_for_price()
# Leon Holuch - end #
    # ask how many results should be displayed
    top_n = ask_for_result_number()
# Leon Holuch & Jonas Hillen - end #

    # ask how many nights the guest want to stay
    nights_n = ask_for_nights()

    #####################################################################
    # STEP 3: query sqlite file for flats in the area given by the user #
    #####################################################################

    # get matches from csv file
    columns = ['name', 'neighbourhood', 'price', 'minimum_nights']
    results = query_sql(
        key='neighbourhood_group', value=location,
        columns=columns, sql_file=sql_file
    )

    # if there are no results: apologize & quit
    if len(results) == 0:
        print('Tut mir Leid, ich konnte leider nichts finden!')
        return

    #############################################################################
    # STEP 4: print information about the first top_n flats in the results list #
    #############################################################################
# Leon Holuch - begin #
    # filter results #
    results = [p for p in results if p[2] <= price_m]
    print('Ich habe {} Wohnungen mit dem Preis{} oder niedriger in {} gefunden.\n'.format(
        len(results), price_m ,location))

# Jonas Hillen - begin #
    # sort results
    results = [r for r in results if r[3] <= nights_n]
# Jonas Hillen - end #

    # return results
    print('Ich habe {} passende Wohnungen in {} gefunden.\n'.format(
        len(results), location))
    # check input ≤ num of results
    print('Hier sind die {} besten Ergebnisse:\n'.format(min(top_n, len(results))))

    # print the first top_n entries from the results list
    for r in results[:top_n]:
        answer = '"{}", {}. Das Apartment kostet {}€. Du musst mindestens {} Nächte bleiben.'.format(
            # look at the columns list to see what r[0], r[1], r[2] are referring to!
            r[0], r[1], r[2], r[3]
        )
        print(answer)


if __name__ == '__main__':
    #  the airbnb_bot() function is called if the script is executed!
# Leon Holuch & Jonas Hillen - begin #
    # greet user
    print('Hallöchen!\n')
    while True:
        airbnb_bot(sql_file='listings.db', top_n=10)

        u_end = input('\nMöchtest du nochmal suchen? [Ja/Nein]\n')

        if u_end.lower() == 'ja':
            continue
        if u_end.lower() == 'nein':
            break
        print('\n"' + u_end + '" war keine Option... Selbstzerstörung in...')
        print('\n...3...')
        time.sleep(1)
        print('...2...')
        time.sleep(1)
        print('...1...')
        break
# Leon Holuch & Jonas Hillen - end #
