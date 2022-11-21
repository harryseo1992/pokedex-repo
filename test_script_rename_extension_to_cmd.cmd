ECHO write to screen
python driver.py --inputfile input_ability.txt ability
python driver.py --inputdata 2 move
python driver.py --inputdata 2 pokemon
python driver.py --inputfile input_move.txt move

ECHO write to file
python driver.py --inputfile input_move.txt --output output_move.txt move
python driver.py --inputfile input_ability.txt --output output_ability.txt ability
python driver.py --inputfile input_pokemon.txt --output output.txt pokemon

ECHO write to file expanded
python driver.py --inputfile input_pokemon.txt --output output_pokemon_expand.txt pokemon --expanded

ECHO error
python driver.py --inputfile input_error.txt --output output_error.txt move
