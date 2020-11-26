# Gmail Email Compiler
+ A personal use script that compiles a user's daily emails which conform to desired filters and presents them in a readable webpage.
+ Built for Gmail users using the Gmail API

### Function  
+ The script that compiles the user's emails is **emailcompiler.py** which
	+ must be run from a directory of a user's computer that also contains the users *credentials.json* and *token.json* file   
	(see **Set Up**)
	+ contains a string directory which must be changed to indicate the user's desired location for the html files produced and atachments downloaded
		+ this directory can be the same directory as where emailcompiler.py is located or separate
	+ conatins a list of search paramaters that the user can change to curate their daily email brief.   

+ When run, **emailcompiler.py** 
	+ creates an html webpage that displays summaries of all retrieved emails
	+ saves that html file in the specified directory in the user's computer
	+ downloads any email attachments to that same directory (attachments are linked to in the webpage)
	+ prompts the user to decide whether or not to mark all compiled emails as read.
	+ If the user selects 'yes' marks all retrieved emails as read.  

### Set Up
In order to use the ezgmail module as part of this script, you will first have to follow the directions in the Installation section of  
the the [ezgmail GitHub repository](https://github.com/asweigart/ezgmail) (also shown below) in order to enable the Gmail API for your gmail account and save 
the neccesary *credentials.json* and *token.json* files to your directory. 

>### Installation
>To install with pip, run:
>
>    	pip install ezgmail
>
> You will need to download a *credentials-gmail.json* file by going to https://developers.google.com/gmail/api/quickstart/python  
> and clicking the **Enable the Gmail API** button (after logging in to your Gmail account). You will need to rename the downloaded 
>*credentials-gmail.json* file to *credentials.json*.
>
>Once you have the *credentials.json* file, the first time you run ``import ezgmail`` it will bring up a window asking you to log   
>in to your Gmail account and allow "Quickstart" to access it. A *token.json* file will be generated which your script can use to  
>access your account.
>
>Future calls to ``ezgmail.init()`` or any other ``ezgmail`` function won't require this token-generating step. The ``gmail.init()``   
>function is automatically called when any other ``ezgmail`` function is called.
The user's credentials.json and token.json files should be saved in the same directory as the emailcompiler.py file.
	
### Styling
The script contains an optional link to an external css stylesheet 'style.css' if the user desires more flexible display styling.  
The style folder of this repository contains a template style.css file that must be stored in the same directory as the emailcompiler.py file.  

The webpage can be displayed with extneral styling linked:
```python
  with webpage.head:
    link(rel='stylesheet', href='style.css')
```  
Which (with the template style.css in this repository) results in a mail summary that looks like this:  
<img src="images/webpagewithstyling.jpg" alt="WithStyling"
	title="Withstyling" width="650" height="375" />   
	
Or with no external styling linked: 	
```python
  #with webpage.head:
    #link(rel='stylesheet', href='style.css')
``` 
Which results in a mail summary that looks like this:  
<img src="images/webpagenostyling.jpg" width="650" height="375" />   

 

