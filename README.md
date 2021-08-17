# Fantasy-Football-optimiser
Creates an optimised DraftKing's Line-up based on the provided projections

This is is code I have written a while back in order to automatically write the best (n) lineups for a fantasy-football team into a csv file, that can be uploaded directly to DraftKings. 
The projections used here are from https://fantasyfootballanalytics.net/. Other projections can of course be used but the Data-read in class has to be extended I assume. 
There is also a jupyter notebook explaining the logic and the most important steps of the MIP.
The code needs refactoring, but so far I have been too lazy to do so.

## How to use
Note: This whole process can automised if desired
1. Download the projections
2. Download the DrafKing Salaries (best to directly copy them)
3. Run main.py with the chosen parameters
4. Upload the projections to DraftKings
5. Happy gambling

Side Note: This is only the optimisation of the line-up so if the projections are bad, it's as always garbage in = garbage out. Also this does not really take the uncertainty that is associated to each prediction into account. This could be something fun for the future