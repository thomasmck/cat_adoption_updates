# cat_adoption_updates
Script for automatically checking when new cats are availabe for adoption from the Blue Cross and sending out email notifications.

Notes:
* Create a file called "settings.py" with the following details:
  * "email" = email address you wish to use to send the notifications email, for current settings this needs to be a gmail account which has enabled access from less secured devices
  * "password" = password for the email above
  * "recipients" = list of emails to send notification emails to
* "cat_list.csv" currently contains the list of cats available when I ran the scripts myself, please remove these before running the script yourself
* If you have a different set of filters you wish to apply then just copy in your link with correct filters to the variables "cat_page" in "main.py"
* Be sensible about how often you call the script
