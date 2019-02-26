## ScootyWorld
## By Ravisastry

This Web Application is a Project for the Udacity [FullstackNanoDegreeCourse](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

## About Project:
This application displays the latest scooters along with scooter categories,authenticated users can perform the CRUD operations on scooters and categories also.

## Skills Required:
	* Python
	* Html
	* CSS
	* Flask Framework
	* SQLAlchemy
	* OAuth

## How to Install:
	
1. Install [Python](https://www.python.org/downloads).
2. Install [Vagrant](https://www.vagrantup.com/downloads.html).
3. Install [VirtualBox](https://www.virtualbox.org/wiki/downloads).
4. Install [Git](https://git-scm.com/download/win).
5. Vagrant setup file to this Clone or Download[fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm).
6. Launch the vagrant virtual machine inside vagrant sub-directory then open Git Bash:`$vagrant up`.

7. Login to vagrant virtual machine:`$vagrant ssh`.

8. Change directory to /vagrant :`$cd /vagrant/`.

9. Change directory to ScootyWorld project folder inside vagrant folder:`$cd ScootyWorld`.

10. Install the required project modules are:
	* `sudo pip install flask`.
	* `sudo pip install sqlalchemy`.
	* `sudo pip install requests`.
	* `sudo pip install oauth2client`.

11. Create application database:`$python migrations.py`.

12. Inserting application data in database:`$python pushing_data.py`.

13. Run the main project file:`python application.py`.

14. Access the application any local browser[http://localhost:5000](http://localhost:5000).

## JSON EndPoints:

1. Display the all categories:`http://localhost:5000/categories/JSON`.
2. Display the all scooters:`http://localhost:5000/scooters/JSON`.
3. Display the scooters of given category:`http://localhost:5000/scooters/category/1/JSON`.
4. Display the scooters of given category in scooter:`http://localhost:5000/scooters/category/1/1/JSON`.