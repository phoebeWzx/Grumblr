# README

### DNS for homework#6

http://ec2-100-26-190-77.compute-1.amazonaws.com:8000/

#### LoginPage

- The ``Sign Up`` on the Navbar links to the registration page
- If you input nonexistent username or password, it will display error messgae
- If username and password is correct, it will turn to Global Stream Page
- The ``Forget Password`` links to reset the password by registered email address

#### Reset Page & ResetPassword Page

- After if checking the input email is a registered email, the reset link will send to the console
- Input the new password and confirm it in the reset link.
- The page will go back to login in page and the user can use the new password login account.

#### Registration Page

- The ``Login`` on the Navbar links back to the login page
- If any information is missing, it will display errors
- If user successfully register, it will send a verify email to console
- The verify link will turn to global page

#### Global Stream Page

- Only logged users can reach this page
- The right side displays the fistname and lastname of the logged user
- Each post links to its user's profile page
- ``My Profile `` link to the current user profile page
- ``Sign out`` links back to the login page
- ``Follower stream `` links to Follower stream page which will display all posts of followers

#### Profile Page

- User information (first name and last name) ,username, short bio and age are on the right sidebar
- Brand of navbar and ``Global`` link to the global page
- The logged user profile will have link to edit profile
- Vistor profile page has link to choose 'follow' or 'unfollow'.(If you click 'follow' or 'unfollow' button then return to the last page, please reload the page and the follow statement will be correct)
- ``Sign out`` links to the login page

#### Follower Stream

- This page will display all posts of followers

#### Edit Profile

- User can change firstname, lastname, age and short bio in this page
- User can upload the picture as the avatar
- ``Change password`` on the nav bar will link to change password page

### Notes

- I used amazon web service with Nginx and uWSGI
- First, I cloned and set up my Grumblr App on AWS instance. Then I installed uWSGI with editing config .ini file and set system unit file to automatically reboot uWSGI. Then I installed Ngix and configured config file to set port and static path. Finally, I modified the email backend to use the andrew SMTP server.

#### Ref

- https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-uwsgi-and-nginx-on-ubuntu-16-04
- https://medium.com/@srijan.pydev_21998/complete-guide-to-deploy-django-applications-on-aws-ubuntu-16-04-instance-with-uwsgi-and-nginx-b9929da7b716