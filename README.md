# Item Catalog Project
##### By: Sarah Thomens

## How to Install and Run Project
1. This project should be run using a virtual box, we'll use VirtualBox and Vagrant.
	* To download VirtualBox click [here](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) and install the platform package for your operating system.
	* To download Vagrant, which configures the VM, click [here](https://www.vagrantup.com/downloads.html) and install the version for your operating system.
2. Next configure the Virtual Machine by downloading [this](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip) and moving to your preferred directory.
	* Open your terminal and cd into this directory
	* cd into the vagrant directory
	* Start the virtual machine: `vagrant up`
	* Log into your virtual machine: `vagrant ssh`
3. To set up the database, run in the vagrant the command: `python starterBooks.py`. If it works, the program should have spit out "Books Added!"
4. To start the server, run in the vagrant the command: `python application.py`
5. To see the website, open up your browser of choice and navigate to: 'localhost:8000'. This will bring you to the main page of the website. From there, you can navigate the site using the links and buttons.
6. To shut down, return to your terminal and press CTRL + C to exit the server.
7. To shut down vagrant:
	* First, close out the ssh by typing CTRL + D
	* Next, type vagrant halt to completely shut down vagrant.


## Project Description
This program creates an item catalog for books. It uses a database to store books and users. Each book has a title, author, description, and genre. Each user has a name, email, and picture.

### CRUD
The project allows the user to do several tasks following the CRUD outline.
1. Create - The user can add new books if they are logged in.
2. Read - The user can view books in several ways. The books are pulled from the database. The site can list recent books, all books, the books the user created themselves, and books organized by genre. Individual books can also be accessed where the user can see the title, author, genre, and description of a specific book.
3. Update - The user can edit only the books they have added to the system. The title, author, description, and genre can all be edited and updated in the database.
4. Delete - The user can delete only the books they have added to the catalog.

### OAuth
The project also uses OAuth to help secure the web app and only allow users to edit and delete books and only add books when they are logged in.
* This application uses the Google OAuth system to allow users to sign in.
* The authentication in this project was greatly influenced by Udacity's course on Google Authentication. They have a course [here](https://www.udacity.com/course/authentication-authorization-oauth--ud330) if you want to learn more.

### JSON
This project has three JSON endpoints which the user can use to see just the information in the database easily.
* localhost:8000/catalog/JSON - this endpoint shows every book in the database and their corresponding information.
* localhost:8000/book/<book_id>/JSON - this endpoint shows a specific book in the database and its corresponding information.
* localhost:8000/user/<user_id>/JSON - this endpoint shows the users in the database and their corresponding information.


## Back End Web Development Elements Used
* `vagrant` - virtual machine
* `sqlalchemy` - python database library
* `flask` - server-side framework
* `jinja2` - python template engine
* `oauth2` - authentication (specifically Google)
* `JSON API` - to access database information
