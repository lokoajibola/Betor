@echo off
call C:\ProgramData\anaconda3\Scripts\activate.bat base
cd "C:\Users\MY PC\bets"  // Navigate to the script directory
python sel_bet9ja2.py      // Execute the script
python sel_sportybet2.py      // Execute the script
python sel_1x1.py      // Execute the script
python bet_arb1.py      // Execute the script
pause
