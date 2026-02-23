user = User.objects.get(username="default") this is because auth is excluded 





# TO-DO
## PRIORITY 1 FIXES
    - check the custom error messages in mixin
    - update the homepage

    - on fridge add i can assign 0 and negative 
    - on edit ingredietn it shows 2 labels for the duplicate names specifically 
    - on add and edit recipe i can assign negative ingredients 

## PRIORITY 2 FIXES
    - finish documentation and link it properly
    - remove all prints 
    - remember to set debug false 

## FEATURES
    - add search boxes
    - add more dummy data

    - add calorie tracker
    - add select boxes and select all with option to delete all ?

## TEST
    - duplicates, deleting to set null
    - add unique=true where applicable, make sure measure units are transformed dynamically
    - update the setup inscrutions and files, test on other PC and acc

    
## UI
    - make the house, cart, fork on the same row for mobile
    - no sticky header on mobile    
    - center the divs in header lol

## EXTRA FEATURES
    - check if i can make a guide
    - check if i can make day/night widget
    - later I plan to have a check that allows edit/delete only on fields created by a specific user (user cannot delete public ingredients made by other users)
    - created by will be added to models once i implement auth













