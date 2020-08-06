# DataNest
A modular command line program for capturing and analyzing data from the popular MMORPG, Dragon Nest. Written in Python and uses SQL.

### Overall status:  
- In progress  
    
## Module 1 - Conversion Tracker:
#### Background:
- In Dragon Nest, players get to open 3 conversion boxes every day - 1 armor box, 1 wtd box (wings/tail/decal), and 1 acc box (accessory)  
- When opened, players will receive a random number (from 10 - 100) of fragments corresponding to the box type (armor boxes give armor fragments, etc.)  
- This module aims to help players keep track of the number of fragments received and estimate how lucky or unlucky a player is according to probability data
#### Features:  
- Import, export data from csv  
- Add, remove, view characters  
- Add, update, delete data for specific dates  
- View data (overall, or for specific dates)  
- Data stored in a single db file, managed with sql  
