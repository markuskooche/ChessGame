# ChessGame
Current Version: 0.4.1

## How to install the game
First you have to install all requirements.

requirements.txt
```
numpy==1.19.4
pygame==2.0.1
```

The easiest way to install the requirements is by executing the install.sh file.

install.sh
```
#!/usr/bin/env sh

python3 -m venv packages/
source packages/bin/activate

python3 -m pip install -r requirements.txt
```

Now you have to start the virtual environment end start the game.<br>
You can do this with the run.sh file.

run.sh
```
#!/usr/bin/env sh

python -m venv packages/
source packages/bin/activate

python3 main.py
```


## How to move a piece
* Click on a field to select a figure.
* Click on another field to execute the move.


## How to control the game
* To reset a move, press the key 'r'.
* To delete a selection, press the key 'd'.
* To start a new game, press the key 'n'.

**WHEN A PAWN REACHES THE END OF THE BOARD, YOU CAN CURRENTLY ONLY PERFORM A PAWN PROMOTION WITHIN THE TERMINAL.**


## Version history
| Version | Changelog                             |
|---------|---------------------------------------|
| 0.1     | gui and moves created                 |
| 0.2     | figure classes and player class added |
| 0.2.1   | basic figure moves added              |
| 0.2.2   | stupid random player added            |
| 0.2.3   | pawn attack moves added               |
| 0.3     | check and checkmate added             |
| 0.3.1   | small optimizations for legal_moves   |
| 0.3.2   | faster algorithm for legal_moves      |
| 0.3.3   | 'king checking king'-moves deleted    |
| 0.3.4   | pawn promotion added                  |
| 0.3.5   | en passant added                      |
| 0.3.6   | castling added                        |
| 0.4     | code was revised and ui stuff added   |
| 0.4.1   | game class was revised for player     |
| 0.4.2   | install and run files added           |