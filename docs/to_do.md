- CSS @import works fine in development but breaks with collectstatic + DEBUG=False because WhiteNoise serves each file independently — it doesn't process or bundle @import statements, so the imported files never load.
- No amount of planning seems to be enough, I and up reworking things multiple times 
- worked on multiple git branches, switched back and forth, forgot to pull, made and resolved conflicts, learned that the local main does not update on its own and a git pull instead of a git pull origin main gave me a heart attack 
- creating a branch called pages-something and then learning it is called paginator left me with some weird looking branches 


# TO-DO

## PRIORITY 1 FIXES

## PRIORITY 2 FIXES
    - clean up css and move to different files(?) - the project breaks when I try to import css and I'm not sure why yet
    - remove attrs={'class':
    - fix DRY for the form in edit_ingredient_popup (? no idea what i meant here, check if calling form twice is optimal)
    - use exclude in the form (?)
    - move nutrients and stuff outside of models
    
## FEATURES
    - add view option to grocery list
    - add calorie tracker
    - add search boxes
    - add more dummy data
    
    
## TEST
    - duplicates, deleting to set null
    - add unique=true where applicable, make sure measure units are transformed dynamically
    - update the setup inscrutions and files, test on other PC and acc

    
## UI
    - make the house, cart, fork on the same row for mobile

## EXTRA FEATURES
    - check if i can make a guide
    - check if i can make day/night widget
    - later I plan to have a check that allows edit/delete only on fields created by a specific user (user cannot delete public ingredients made by other users)
    - add weight to ingredients and recipes (total weight to be split to portions?)
    - add select boxes and select all with option to delete all ?














