# DataNest
A modular command line program for capturing and analyzing data from the popular MMORPG, Dragon Nest. Written in Python and uses SQL.

### Overall status:  
- On hold  

## Conversion Tracker Module:  
#### Background:  
- In Dragon Nest, players get to open 3 conversion boxes every day - 1 armor box, 1 wtd box (wings/tail/decal), and 1 acc box (accessory)  
- When opened, players will receive a random number (from 10 - 1000) of fragments corresponding to the box type (armor boxes give armor fragments, etc.)  
- This module aims to help players keep track of the number of fragments received and estimate how lucky or unlucky a player is according to probability data  
#### Features:  
- Add, remove, view characters  
- Set active character to manage data for  
- Startup notification to inform user if data has been entered for the day  
- Import, export data from/to csv  
- Add, update (modify), delete data for specific dates  
- View data  
  - i) values for specific dates  
  - ii) overall values for armor, wtd, acc, combined (average, count, total)  
#### Technical Information:  
- Uses sql to manage data in a single db file  
- Stores each character's data in a separate table with the following naming convention - "(character name)" + "_conv", to allow for the addition of data from other modules into the db later  
- Each table has 4 columns: date, armor, wtd, acc  
- Users are allowed to store one record for each date (records can be updated/ modified)  
- When adding a record, users are required to key in values for armor, wtd, acc all at once, but can choose to enter blank values first and update them again later  
- Null values will not affect the average, count, total when viewing overall values  
