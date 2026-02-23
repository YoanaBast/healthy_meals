## What I’ve Learned

- 404 pages don’t render with `DEBUG=False`; WhiteNoise helps serve static files.  
- CSS `@import` works in development but breaks after `collectstatic` + `DEBUG=False` because WhiteNoise doesn’t bundle imports.  
- Planning is never perfect; multiple reworks are normal.  
- Git: switching branches, resolving conflicts, and understanding that `git pull` vs `git pull origin main` behave differently is crucial.  
- Branch naming matters—misnamed branches (e.g., `pages-something` vs `paginator`) can create confusion.  
- PR workflow: merging too early can leave unfinished tasks; always double-check before closing a branch.  
- JS is essential for dynamic UX (e.g., pop-ups) to avoid losing user input during CRUD operations on related entities like categories, units, or tags.


## What I’ve Learned (Short)

- 404 + `DEBUG=False` needs WhiteNoise.  
- CSS `@import` breaks after `collectstatic` + WhiteNoise.  
- Plans always need rework.  
- Git: know `git pull` vs `git pull origin main` and handle conflicts.  
- Branch names matter—misnaming causes confusion.  
- Don’t merge PRs too early.  
- JS needed for dynamic UX to keep user input during related CRUD.
