# SQL Injection Talk

## Outline

1. START with homepage of student website
1. What is a website?
    1. Show `/home/tchamber/repos/sql_injection_talk/sample_file.txt`
        * This isn't _really_ a website...
    1. Show https://www.gb.nrao.edu/~tchamber/a_website.html
        1. Show dev tools here; keep them open!
        1. This is a _very simple_ website. In the olden days...
    1. Show `basic_site.py`
        1. But what if we want:
            * persistent data
            * our users each to see something different when they go to our website?
        1. We need some way to send data _to_ a website/server
        1. Explain basics of GET/POST
    1. Show `basic_site_no_persistence.py`
        1. This is a simple website that stores any students you add to a list in memory
        1. This can be considered "an in-memory database"
    1. Show `basic_site_with_persistence.py`
        1. This is a slightly more complicated website that stores students in a CSV file on disk
        1. This can be considered "a very simple database"
        1. Show CSV file in Sublime
        1. Show CSV file in Excel
1. Why might you use a "proper, relational database"?
    1. Performance. What if there are 10 million rows?
    1. Reliability. What if one thousand people are trying to make changes simultaneously?
    1. Features. Relationships
1. How do we make a database do things?
    * In PSQL shell
        1. Basic queries
        2. Multiple queries
        3. Comments
1. Now we can make a website that uses a database!
    1. Show login
