## Repo Link

https://github.com/delio05/The-Billion-Dollar-Club.git

## Frontend Set Up

The frontend of this project uses HTML, JS, CSS, and custom @webcomponents HTML elements. Read the [frontend guide](Frontend.md) for set-up steps.

## Backend Set Up

The backend of this project uses Django. Read the [backend guide](./Backend.md) to run the backend server.

## Overview

This project was done in partnership with Epic for our CS639: Computer Science Capstone course at UW-Madison. 

This is an AI driven Chrome extension that allows users to highlight text on any webpage that they'd like to simplify into easier to understand language. 
The initial intent was for this to be specefically for complicated medical text and doctor notes left for patients through MyChart, however, we've broadened it such that it can be used for any catagory/page now. 

To use, users can highlight whatever they'd like simplified, and then go to thr Chrome extension. The highlighted text will be displayed there and they can hit the "Summarize" button to simplify. There is also the option to translate to other languages and extract the text to a PDF. Currently with the way the code is set up, users can access the frontend of the extension to see the UI and then run the backend seperatly for access to the full functionality of this extension. 

## What Works & What Doesn't

Currently every feature that we've implemented has full functionality as expected. This includes the summarization of complicated text, language translation, extract to PDF, and provide feedback (which is currently data being collected on our backend). That being said, there is still room for improvement in all these features. For example, what doesn't work yet from what had initially planned is that the extension doesn't persist data. So, if a user wants to see their old simplified text, it will not show up and they will have to re-highlight the text they want.
As an alternative to that, we made the Extract to PDF option, which a user can use to save their old information. However, the features we did add have full functionality. 

## Future Steps

Since we only had the scope of one semester to work on this, here are some features and next steps we would implement with more time:
1. <b>Improve UI</b>: We currently have a straightforward and simple to use UI which aligned with our target audience for this extension. However, we would still like to find creative ways to improve the current design and make it more visually pleasing.
2. <b>Extend Chatbox Functionality</b>: There is currently no way for the user to communicate back and forth with the AI (in other words, we don't have a chatbox functionality). This is something we wanted to do but did not have enough time during the semester to add and can be a future step to extend the functionality of this extension.
3. <b>Privacy Settings</b>: Because the original purpose of this extension was to implemented with MyChart through Epic Systems, it would be important if this were ever being actively used to have some sort of privacy settings enabled.
4. <b>Publish to Chrome Store</b>: The next step after fleshing out all these features would be to publish our extension to the Chrome Store so it can easily be accessed by anyone who'd like!
5. <b>Organize extracted PDF</b>: 
