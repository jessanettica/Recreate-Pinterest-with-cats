
![cats](https://cloud.githubusercontent.com/assets/8107962/23489845/96342ac0-fea9-11e6-89e0-a3fa0cbe239c.gif)

Sections:
* Stack
* Implementation Details
    * Django
    * Seeding the db from the provided JSON data
    * Displaying the Pins
    * Infinite Scroll
    * Adding new widgets/pins to the page
* How to run the project on your computer
* Possible Issues
* Further Improvements


Stack
SQLite database, Django for the web framework, Python, JavaScript and jQuery.


**Implementation Explanation**

*Django*

This project is built with Django. I chose Django because I wanted to showcase using
a framework I have most recently been working with. Additionally, Django comes with 
user authentication and for this project I implemented user registration, signin, 
and sign out.

SQlite is the default database for Django, and it is fast and efficient. However, to
deploy the project, it would be necessary to migrate to mySQl or Postgresql. 

*Seeding the DB*

The JSON version of the dataset provided is saved in the 
`pins_formatted.json` file in the seed_data directory. That file was then used 
in the `seed_db.py` script in the scripts directory. 

*Displaying the Pins*

The pins are loaded to the page on inital page load with AJAX. After assigning the 
column width and the margin between the columns, using the window width the 
number of columns that will fit on the page is calculated. An array is used to store
the height of each column, and the length of the array is how many columns are on
the page. When each pin is added, it is added to the shortest column, and the array
is updated with the new column height. The left and top of each of the 
absolutely-positioned pins is determined using these values (`getTopPosition()`, 
`getLeftPosition()` as well as the rest of the logic described above is in 
static/pins/pins.js).

*Infinite Scroll*

Infinite scroll was also implemeted with AJAX. When the user scrolls to the bottom
of the page, it triggers a post request. Using the model method `as_dict` (it's at
the bottom of `models.py`), which returns a dictionary representation of an object,
which is then jsonified, the response contains json data of the first 24 pins 
that have not been used since all of the pins were previously all used (this is
handled with the `is_used` field on the Pin model (in `models.py`). If all the 
pins have been displayed, then 20 are displayed and the is_used_field is updated 
so that they are not used again untill all the pins have been used once more.

*Adding new pins*

I made the assumption that "giving other widgets to arrange on 
the page" meant that the page had to handle the addition of user-created pins as
well. My take is a form on the page that opens in a modal when a user clicks on 
the blue "Create Pin" button. After the user fills out the form and submits it, 
the appropriate board is either created or fetched, and the Pin is created and
saved in the db. The  modal closes and the user received an alert that their 
pin is created. The new Pin is appended at the bottom of the page after the pins
currently loaded. If the user scrolls, the new pins fetched will be appended after
the new created pin. 

*User Registration*

Once you are running the program on your computer (see the section below on how to do that), you will have to register as a new user or login to see the homepage. You just 
have to enter a username and a password. You'll have to enter the password twice 
in the form to confirm it. You will then be redirected to the homepage (For reference it's at "http://localhost:8000/pins/").


**Installation/How to run the Project**

Step 1)Check that you are at the level that contains the pinenv/ directory (the same level that also has this README file) and activate the virtual env by running:
    `source pinenv/bin/activate`

    Possible issue: You do not have virtualenv. To install it run:
        `pip install virtualenv`
        Then try `source pinenv/bin/activate` again. 


Step 2) Go into the pinsite/ directory and install the dependencies by running:
    ```
    cd pinsite/
    pip install -r requirements.txt
    ```

    Possible issue: You do not have pip and so you cannot do any of the above.
        Highly unlikely because pip is already installed if you're using Python 2 >=2.7.9 or Python 3 >=3.4
        You can check by running:
        `pip --version`

        If you have pip but it is not working as it should (installing the dependencies) try updating it by running:
        `pip install -U pip`

    If you ran `pip install -r requirements.txt` it should have installed Django 1.8 and  django-extensions. 
    Check if you have the right Django version by running: 
        `python -c "import django; print(django.get_version())`

    Possible issue: The dependencies are not installing.
        The above should definitely work, but just in case, you can make your own
        virtual environment and install the two dependencies this project uses. You
        can do this by running:
            ```
            pip install virtualenv
            virtualenv name_you_want_for_your_virtual_env
            source name_you_want_for_your_virtual_env/bin/activate
            pip install django==1.8
            pip install django-extensions
            ```


Step 3) You should still be in the directory pinsite/ which contains the manage.py file.
    Check with 'ls' and then you are ready to start the server.
    To run the server:
        `python manage.py runserver`

    In your browser open up: `http://localhost:8000/`
    If that's not the right port, when you start the server the terminal will tell you which port the development server is on. 

Step 4) Register as a new user and checkout the cat-themed pins!


**Other possible issues**

1) You are getting an error that says `'ImportError: No module named django.core.management`':
    That means you don't have django installed. Check by running `python -c "import django; print(django.get_version())`
2) If you are getting that error but you do have django installed, it might be that django is installed on your computer
in a directory path that is unaccessible to the project. Try pip installing Django 1.8:

    `pip install django==1.8`

3) If you are still having issues and the server is not starting check that you have the dependencies installed (django 1.8 and requirements). 
If `pip install -r requirements.txt` did not work and you don't have django or requirements you can pip install the 2 dependencies.
Note: this project uses django 1.8, so you must install that version. If you just run pip install django it will intall 1.10. To install the 2 dependencies run: 
```
    pip install django==1.8
    pip install requirements
```
Those 2 dependencies are all you need. 

4) `Six` issue when installing packages
  * go here: github.com/pypa/pip/issues/3165



**Further Improvements**

    * add a style sheet. In-line style is not best practice, so the very first
    improvement I would make would be to make a css file and put all of the styling there. 
    * speaking of style, the overflow on the pin discriptions is hidden, but it does not show the ellipsis. When I add the ellipsis to the text-overflow property it only works
    if I also use nowrap on thw white-space property. Making the ellipsis work on multiple lines like on the Pinterest feed would be an awesome and aesthetically pleasing improvement. 

    * making registration more robust so that the same user data is available for all users. For example, right now the users added from the dataset have a full name and image, but users that register on my project site for teh first time do not. The users created from the data, were never registered, so they don't ahve passwords and can't be authenticated

    * an alternative improvement to making registration more robust would be to implement sign-in with a third party, like Facebook sign-in or Google sign-in.
    * add ability for users to create shoppable pins. For now, I set the shoppable field as
    False for all user-created pins. 

