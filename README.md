![brandlogo](static/images/moviefindericon.svg)

# Milestone Project 3 Data Centric - MovieFinder
<p align="center">
<img src="static/images/moviefindergif.gif" height=340>
</p>

## Problem Statement
The aim of this project is to demonstrate ones ability to utilize python web framework, Flask, to perform create, read, update and delete (CRUD) operation with a database. 
To fulfill this requirement in a practical approach, an application which allows user to share movie information such as casts, director, images or short clips,
 was built. This
application shall be able to perform the following:
- To add a new movie
- To edit a movie info
- To delete a movie
- To search for a movie by filtering
<br/>

## UX
Realization of this project depends on the availability of users and technologies. Users would be moviegoers or moive reviewers who wants to share 
different types of movie they have watched. This application should fulfill their following needs:

- "I want to have different ways to filter for a particular movie information."
- "I want to know what type of movie which I have just watched."
- "I want to share and add this old movie info to somewhere for others to know."
- "I want to edit and delete movie info which is wrong."
- "I want to know which movies this particular actor/director is casted in."

By using front-end and back-end technologies such as bootstrap, flask, the user's needs can be achieved.<br/>

The minimalist design approach on the styling of the appliation is to allow the content to stand out and be the focal point. Each buttons are designed and styled 
in a similar fashion to allow ease of recognizing interactive features on the application. 
As filtering by genre is a common queries ones will seek before 
reading further about a movie, this application would present a landing page showing different movies filtered by genre. For ease of access to filter movies by year
or genre or keywords and adding movie info, the top bar would be built with these features and available in every pages.

<p align="center">
<img src="static/images/moviefinder_landingpage.JPG" height=500>
<br/>Fig-1 Landing page of MovieFinder
</p>

A wireframe of this application can be found [here](https://xd.adobe.com/view/b9de51c0-dc0c-4f05-b796-5655a8f68da1-ec8d/).<br/>

## Features
### Existing Features

- ***Landing Page*** - The landing page displays movies filtered by different genre.
<p align="center">
<img src="static/images/moviefinder_landingpage.JPG" height=500>
</p>

- ***Movie Info Search Bar*** - This feature allow user to search for different number of movies in the movie database by keywords.
 <br/><p align="center">
<img src="static/images/searchbar.JPG">
</p>
<br/>



- ***Top Bar Buttons*** - (From left to right) The "i" movie recorder button directs the user back to the landing page. 
The genre dropdown menu displays a range of available genre and if selected, it directs the user to the movie info list of the selected genre.
The year dropdown menu displays a range of available year and if selected, it directs the user to the movie info list of the selected year. The add movie
button displays the add new movie popout.
 <br/><p align="center"><p align="center"><img src="static/images/moviefindertopbarbuttons.JPG"></p>
  <br/>

- ***Movie Genre View More Button*** - The view more button directs the user to a movie info list page filtered by genre .
<br/><p align="center"><img src="static/images/moviefinderviewmorebuttons.JPG"></p>
  <br/>  


- ***Movie Info Page Side Bar Button*** - (From top to bottom) The waste bin icon directs the user to the delete popout. The edit icon directs the user to the update popout.
<br/><p align="center"><img src="static/images/moviefindersidebuttons.JPG"></p>
  <br/>

 - ***Movie Info List*** - The movie info list displays a list of filtered movies.
<br/><p align="center"><img src="static/images/moviefinder_movieinfolist.JPG" height=400></p>
  <br/>

- ***Movie Info Page*** - The movie info page displays information of a selected movie.
<br/><p align="center">
<img src="static/images/moviefinder_movieinfo.JPG" height=500></p>
  <br/>

- ***Add New Movie Popout*** - The add new movie popout allows user to add a new movie information into the database. It includes a backend validation feature to prevent invalid
info to be uploaded into the database. Partial of the validation script is as shown below:
<br/><p align="center">
<img src="static/images/moviefinder_addmovie.JPG" height=500></p>
  <br/>

  ```
        # To check whether field is empty
            if len(imageurl.filename) == 0:
                errors['file_is_blank'] = "Poster field cannot be blank"
            elif '.' in imageurl.filename:
                file_ext = os.path.splitext(imageurl.filename)[1]
                # To validate file extension
                if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                    errors['poster_ext_is_wrong'] = "Poster file ext is invalid"
            # To validate file size
            elif poster_size > 1024 * 1024:
                errors['poster_size_above_limit'] = "Poster file size cannot be  more than 1MB"

            # To check whether field is empty
            if len(backdrop.filename) == 0:
                errors['backdrop_is_blank'] = "Backdrop field cannot be blank"
            elif '.' in backdrop.filename:
                file_ext = os.path.splitext(backdrop.filename)[1]
                # To validate file extension
                if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                    errors['bkdrp_ext_is_wrong'] = "Backdrop file ext is invalid"
            # To validate file size
            elif backdrop_size > 1024 * 1024:
                errors['backdrop_size_above_limit'] = "Backdrop file size cannot be more than 1MB"
  ```

- ***Update Movie Popout*** - The update movie popout allows user to edit a movie information and upload into the database. Same as the add new movie feature, it also includes a backend validation 
feature to prevent invalid
info to be uploaded into the database.
<br/><p align="center"> <img src="static/images/moviefinder_updatemovie.JPG" height=500></p>
  <br/>

- ***Delete Movie Popout*** - The delete movie popout allowes user to delete movie info from the database. 
<br/><p align="center"><img src="static/images/moviefinder_deletemovie.JPG" height=500></p>
  <br/>

- ***Custom 404 Error Page*** - The custom 404 error page directs the user to a customized 404 error page. The user can be redirected back to the landing page by 
clicking onto the 'i' movie recorder button on the top bar.
<br/><p align="center">
<img src="static/images/custom404page.JPG" height=400></p>
  <br/>


  
  
### Feature Left to Implement
- ***User Account Creation***<br/>
This feature will allow user to create an account and thus, also provide a database of user for this application.<br/><br/> 
- ***User Comments and Likes***<br/>
This feature will allow user to provide their comments for a particular movie and whether they like the movie.  <br/><br/>
- ***Movie rating***<br/>
This feature will allow user to rate a movie.
<br/><br/>
- ***New Added Genre***<br/>
This feature will allow user to have more genre to choose by retrieving newly added genre from the genre collection in the database.
<br/><br/>
- ***Image File Content Check***<br/>
This feature will check whether the content of the uploaded image is appropriate using artificial intelligence.
<br/><br/>
- ***Filtering Genre for Landing Page***<br/>
This feature will allow user to chose the order of the genre to be displayed on the landing page.
<br/><br/>

## Technologies Used

- [HTML/CSS](https://html.com/)<br/>
The project uses HTML/CSS for base template and styling of the landing page.
- [Python](https://www.python.org/)<br/>
The project uses Python as the primary programming language.
- [Bootstrap](https://getbootstrap.com/)<br/>
The project uses Bootstrap for the application responsiveness for different screen sizes.
- [Inkscape](https://inkscape.org/)<br/>
The project uses inkscape for creating svg files.
- [JQuery](https://jquery.com/)<br/>
The project uses JQuery to ease the manipulation of DOM. 
- [Heroku](https://www.heroku.com/)<br/>
The project uses Heroku to host the application. 
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)<br/>
The project uses Flask as the backend frame for server side scripting.<br/>
- [MongoDB](https://www.mongodb.com/)<br/>
The project uses Mongo DB to store movie information.<br/>
- [Cloudinary](https://cloudinary.com/)<br/>
The project uses Cloudinary to store image files and provides the image url links. 
<br/><br/>

## Testing

| <h3>**Features Testing**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Test Case 1: Landing page is displayed as per Fig 1 when page is loaded or refreshed**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| **Expected:** The landing page shall be displayed as per Fig 1.<br/>**Test:** Refresh the page.<br/>**Result:** The  Landing page is displayed as per Fig 1 when page is loaded or refreshed.<br/>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **Test Case 2: Movie info page is displayed after clicking onto one of the movie thumbnail on the landing page**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **Expected:** The corresponding movie info page shall be displayed after clicking onto one of the movie thumbnail on the landing page.<br/>**Test:** Click onto one of the movie thumbnail on the landing page.<br/>**Result:** The corresponding movie info page is displayed after clicking onto one of the movie thumbnail on the landing page.<br/>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **Test Case 3: Movie info list page filtered by genre is displayed after clicking onto one of the genre view more button**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Expected:** The corresponding movie info list page filtered by genre shall be displayed after clicking onto one of the genre view more button.<br/>**Test:** Click onto one of the genre view more button on the landing page.<br/>**Result:** The corresponding movie info list page filtered by genre is displayed after clicking onto one of the genre view more button.<br/>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **Test Case 4: Not more than 3 movie thumbnails for each genre is displayed on the landing page**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Expected:** Each genre shall displays not more than 3 movie thumbnails.<br/>**Test:** Refresh the landing page or click onto the 'i' movie recorder button.<br/>**Result:** Each genre displayed not more than 3 movie thumbnails on the landing page.<br/>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **Test Case 5: Movie info list displays a list of movies filtered by keywords in the movie info search bar**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Expected:** Movie info list shall displays a list of movies filtered by keywords in the movie info search bar.<br/>**Test:** Type in some queries in the movie info search bar.<br/>**Result:** Movie info list displayed a list of movies filtered by keywords in the movie info search bar.<br/>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **Test Case 6: "Sorry we found no result for xxx" error message is flashed when xxx in the movie info search bar does not exist**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Expected:** "Sorry we found no result for xxx" error message shall be flashed if xxx in the movie info search bar does not exist.<br/>**Test:** Type in some invalid queries in the movie info search bar.<br/>**Result:** "Sorry we found no result for xxx" error message is flashed when xxx in the movie info search bar does not exist.<br/>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **Test Case 7: Landing page is displayed when the 'i' class movie recorder button is triggered from other pages**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Expected:** Landing page shall be displayed when the 'i' class movie recorder button is triggered from other pages.<br/>**Test:** Clicked onto the 'i' class movie recorder button from movie info or movie info list page.<br/>**Result:** Landing page is displayed when the 'i' class movie recorder button is triggered from other pages.<br/>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **Test Case 8: Movie info list is filtered by genre when the genre dropdown menu is selected from any pages**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Expected:** Movie info list shall be filtered by genre when the genre dropdown menu is selected from any pages.<br/>**Test:** Select one of the genre from the genre dropdown menu from any page.<br/>**Result:** Movie info list is filtered by genre when the genre dropdown menu is selected from other pages.<br/>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **Test Case 9: Movie info list is filtered by year when the year dropdown menu is selected from any pages**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **Expected:** Movie info list shall be filtered by year when the year dropdown menu is selected from any pages.<br/>**Test:** Select one of the year from the year dropdown menu from any page.<br/>**Result:** Movie info list is filtered by year when the year dropdown menu is selected from any pages.<br/>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **Test Case 10: The release year of any newly added movies which does not exist in the database previously is added and sorted by year in the year dropdown menu**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **Expected:** The release year of any newly added movies which does not exist in the database previously shall be added and sorted by year in the year dropdown menu.<br/>**Test:** Add a new movie with its release year not available in the database.<br/>**Result:** The release year of any newly added movies which does not exist in the database previously is added and sorted by year in the year dropdown menu.<br/>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **Test Case 11: Add movie popout is shown when the add movie button is clicked from any pages**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **Expected:** Add movie popout shall be shown when the add movie button is clicked from any pages.<br/>**Test:** Click the add movie button from any pages.<br/>**Result:** Add movie popout is shown when the add movie button is clicked from any pages.<br/>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **Test Case 12: Movie info page is displayed after clicking onto one of the movie info card on the movie info list page**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **Expected:** The corresponding movie info page shall be displayed after clicking onto one of the movie info card on the movie info list page.<br/>**Test:** Click onto one of movie info card on the movie info list page.<br/>**Result:** Movie info page is displayed after clicking onto one of the movie info card on the movie info list page.<br/>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|  **Test Case 13: "xxx is deleted" message is flashed and redirected back to the landing page after xxx movie is deleted**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **Expected:** "xxx is deleted" message shall be flashed and redirected back to the landing page after xxx movie is deleted.<br/>**Test:** Click the waste bin button to delete the movie.<br/>**Result:** "xxx is deleted" message is flashed and redirected back to the landing page after xxx movie is deleted.<br/>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **Test Case 14:A Custom 404 error page is displayed for an invalid url**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **Expected:** A custom 404 error page shall be displayed for an invalid url.<br/>**Test:** Type in an invalid url after the '/'.<br/>**Result:** A Custom 404 error page is displayed for an invalid url.<br/>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **Test Case 15: Movie text info is loaded onto the text input fields of the update movie popout when the edit button is clicked from the movie info page**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **Expected:** Movie text info shall be loaded onto the text input fields of the update movie popout when the edit button is clicked from the movie info page.<br/>**Test:** Click onto the edit button from the movie info page.<br/>**Result:** Movie text info is loaded onto the text input fields of the update movie popout when the edit button is clicked from the movie info page.<br/>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **Test Case 16: "xxx field cannot be blank" error message is flashed when text input fields contain only a space in the update/add movie popouts**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **Expected:** "xxx field cannot be blank" error message shall be flashed when text input fields contain only a space in the update/add movie popouts.<br/>**Test:** Enter a space in any of the text input field.<br/>**Result:** "xxx field cannot be blank" error message is flashed when text input fields contain only a space in the update/add movie popouts.<br/>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **Test Case 17: "Please fill up this field" message is flashed from the text input field which is blank from the update/add movie popouts**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **Expected:** "Please fill up this field" message shall be flashed from the text input field which is blank from the update/add movie popouts.<br/>**Test:** Leave the text input field blank.<br/>**Result:** "Please fill up this field" message is flashed from the text input field which is blank from the update/add movie popouts.<br/>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **Test Case 18:"Year field cannot be words or characters" error message is flashed when the year input field is not a number from the update/add movie popouts**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **Expected:** "Year field cannot be words or characters" error message shall be flashed when the year input field is not a number from the update/add movie popouts.<br/>**Test:** Enter some words or characters in the year field.<br/>**Result:** "Year field cannot be words or characters" error message is flashed when the year input field is not a number from the update/add movie popouts.<br/>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **Test Case 19:"Year field cannot be less than or equal to zero" error message is flashed when the year input field is <= 0 from the update/add movie popouts**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **Expected:** "Year field cannot be less than or equal to zero" error message shall be flashed when the year input field <= 0 from the update/add movie popouts.<br/>**Test:** Enter 0 or less in the year field.<br/>**Result:** "Year field cannot be less than or equal to zero" error message is flashed when the year input field is <= 0 from the update/add movie popouts.<br/>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **Test Case 20: "Trailer (Youtube url) format is incorrect" error message is flashed when the trailer youtubeurl field is of invalid format from the update/add movie popouts**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **Expected:** "Trailer (Youtube url) format is incorrect" error message shall be flashed when the trailer youtubeurl field is of invalid format from the update/add movie popouts.<br/>**Test:** Enter invalid format in the trailer youtubeurl field.<br/>**Result:** "Trailer (Youtube url) format is incorrect" error message is flashed when the trailer youtubeurl field is of invalid format from the update/add movie popouts.<br/>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **Test Case 21: "Backdrop file size cannot be more than 1MB" error message is flashed when the file size of the selected backdrop is > 1 MB from the update/add movie popouts**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **Expected:** "Backdrop file size cannot be more than 1MB" error message shall be flashed when the file size of the selected backdrop is > 1 MB from the update/add movie popouts.<br/>**Test:** Upload a file of size > 1 MB in the backdrop file input field.<br/>**Result:** "Backdrop file size cannot be more than 1MB" error message is flashed when the file size of the selected backdrop is > 1 MB from the update/add movie popouts.<br/>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **Test Case 22: "Poster file size cannot be more than 1MB" error message is flashed when the file size of the selected poster is > 1 MB from the update/add movie popouts**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **Expected:** "Poster file size cannot be more than 1MB" error message shall be flashed when the file size of the selected poster is > 1 MB from the update/add movie popouts.<br/>**Test:** Upload a file of size > 1 MB in the poster file input field.<br/>**Result:** "Poster file size cannot be more than 1MB" error message is flashed when the file size of the selected poster is > 1 MB from the update/add movie popouts.<br/>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **Test Case 23: "Thumbnails files size cannot be more than 2MB" error message is flashed when the total file size of the selected thumbnails is > 2 MB from the update/add movie popouts**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **Expected:** "Thumbnails files size cannot be more than 2MB" error message shall be flashed when the total file size of the selected thumbnails is > 2 MB from the update/add movie popouts.<br/>**Test:** Upload a few files which each size > 1 MB in the thumbnails file input field.<br/>**Result:** "Thumbnails files size cannot be more than 2MB" error message is flashed when the total file size of the selected thumbnails is > 2 MB from the update/add movie popouts.<br/>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **Test Case 24: Invalid fie extension error message is flashed when the file field is uploaded with file that is not .jpg/.png/.gif extension from the update/add movie popouts**                                                                                                                                                                                                                                                                                                                                                                                                  |
| **Expected:** Invalid fie extension error message shall be flashed when the file field is uploaded with file that is not .jpg/.png/.gif extension from the update/add movie popouts.<br/>**Test:** Upload a file with extension that is not .jpg/.png/.gif extension.<br/>**Result:** Invalid fie extension error message is flashed when the file field is uploaded with file that is not .jpg/.png/.gif extension from the update/add movie popouts.<br/>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |




### Responsiveness
**360 x 640**<br><p align="center">
<img src="static/images/360by640_1.JPG" height=200>
<img src="static/images/360by640_2.JPG" height=200>
<img src="static/images/360by640_3.JPG" height=200>
<img src="static/images/360by640_4.JPG" height=200>
<img src="static/images/360by640_5.JPG" height=200></p>



<br>

**375 x 667**<br><p align="center">
<img src="static/images/375by667_1.JPG" height=200>
<img src="static/images/375by667_2.JPG" height=200>
<img src="static/images/375by667_3.JPG" height=200>
<img src="static/images/375by667_4.JPG" height=200>
<img src="static/images/375by667_5.JPG" height=200></p>

<br>


**768 x 1024**<br><p align="center">
<img src="static/images/768by1024_1.JPG" height=200>
<img src="static/images/768by1024_2.JPG" height=200>
<img src="static/images/768by1024_3.JPG" height=200>
<img src="static/images/768by1024_4.JPG" height=200>
<img src="static/images/768by1024_5.JPG" height=200></p>

<br>

### Bugs/Problems Encountered
There are a numbers of bugs or problems encountered during the development of the project. The main ones are as explained below:

- ***Retriving data after looping through a pymongo.cursor.Cursor object*** <br>
During looping of movie database on the html side using Jinja2 language, the looping can only be looped once. It was discovered that the return type of the movie database was a pymongo cursor which resulted only a single scan in the loop. 
This was solved by changing the type from pymongo cursor to list object on the server side before passing it to the html.

- ***Reading same file*** <br>
During uploading of the image file to the Cloudinary cloud database, the Cloudinary api responded with an error on empty file being uploaded.
It was discovered that after performing a read operation on the file in the form validation function, the pointer of the file was shifted to the end
of the file. Hence, this caused Cloudinary to detect an [empty image file](https://stackoverflow.com/questions/28320658/python-why-a-file-is-empty-after-reading-it-and-writing-to-another-one). This was solved by shifting the file pointer to the start of the file using 
[seek](https://www.codestudyblog.com/questions/sf/0421194141.html) and then read the file again.
    

## Deployment

The website is hosted using heroku and can be accessed via [here]( https://simplyedwin-tgc-proj3-movfdr.herokuapp.com/).


## Credits

### Acknowledgements

- Trent colleage staff and classmates for feedbacks on website design

- Design of logo are sourced from [Freepik](https://www.flaticon.com/authors/freepik).

- [Toast scripts](https://github.com/CodeSeven/toastr) used for flashing message.

- Bootstrap 4 floating label css from [floatinglabel](https://www.cssscript.com/pure-css-floating-label-pattern-bootstrap/).

- Readme template from [Code Institute](https://github.com/Code-Institute-Solutions/readme-template).

- For creating the [progress bar](https://www.youtube.com/watch?v=f-wXTpbNWoM) during update or add movie
