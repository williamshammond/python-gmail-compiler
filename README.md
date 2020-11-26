# Gmail Email Compiler
### Function
<ul>
<li>A personal use script to compile my daily emails into a readable webpage.  </li>
<li>emailcompiler.py requires changes to a list of search paramaters that the user chooses to curate their daily email brief.  </li>
<li>When run, emailcompiler.py creates an html webpage that displays summaries of all retrieved emails, downloads that html file in the specified directory in the user's computer, downloads any email attachments to that same directory (attachments linked in the html file), and prompts the user to decide whether or not to mark all compiled emails as read.</li>
<li>If the user selects 'yes' the emails are marked as read.</li>
</ul>
### Set Up
In order to use the ezgmail module as part of this script, you will first have to follow the directions in the Installation section of  
the the [ezgmail GitHub repository](https://github.com/asweigart/ezgmail), shown below.

>Installation
------------

To install with pip, run:

    pip install ezgmail

You will need to download a *credentials-gmail.json* file by going to https://developers.google.com/gmail/api/quickstart/python and clicking the **Enable the Gmail API** button (after logging in to your Gmail account). You will need to rename the downloaded *credentials-gmail.json* file to *credentials.json*.

Once you have the *credentials.json* file, the first time you run ``import ezgmail`` it will bring up a window asking you to log in to your Gmail account and allow "Quickstart" to access it. A *token.json* file will be generated which your script can use to access your account.

Future calls to ``ezgmail.init()`` or any other ``ezgmail`` function won't require this token-generating step. The ``gmail.init()`` function is automatically called when any other ``ezgmail`` function is called.
### Styling
The script contains an optional link to an external css stylesheet 'style.css' if the user desires more flexible display styling.  
The style folder of this repository contains a template style.css file that must be stored in the same directory as the emailcompiler.py file.
The webpage can be displayed with only in-line styling:  
<img src="images/internalstyling.jpg" width="430" height="55" />  
Which results in a mail summary that looks like this:  
<img src="images/webpagenostyling.jpg" width="650" height="375" />   

Or with the external styling linked:  
<img src="images/externalstyling.jpg" width="430" height="55" />   
Which (with the template style.css) results in this:  
<img src="images/webpagewithstyling.jpg" alt="WithStyling"
	title="Withstyling" width="650" height="375" />  
