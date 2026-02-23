user = User.objects.get(username="default") this is because auth is excluded 





# TO-DO
-r remember to set debug false 
## PRIORITY 1 FIXES
    - show only fav needs to filter all not just page and stay checked until i uncheck it
    - remove all prints 
    - check the custom error messages in mixin
## PRIORITY 2 FIXES

## FEATURES
    - add view option to grocery list
    - add search boxes
    - add more dummy data

    - add calorie tracker
    - add select boxes and select all with option to delete all ?
    - finish documentation and link it properly

## TEST
    - duplicates, deleting to set null
    - add unique=true where applicable, make sure measure units are transformed dynamically
    - update the setup inscrutions and files, test on other PC and acc

    
## UI
    - make the house, cart, fork on the same row for mobile
    - no sticky header on mobile 

## EXTRA FEATURES
    - check if i can make a guide
    - check if i can make day/night widget
    - later I plan to have a check that allows edit/delete only on fields created by a specific user (user cannot delete public ingredients made by other users)
    - created by will be added to models once i implement auth













