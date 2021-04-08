# OnlineStoreApp

This is a readme file for the OnlineStoreApp for the Systems Development 2 coursework.

## Implementation Notes

Since this is a prototype application, there are obviously going to be a few things different between this and the final product.

### What is implemented

#### Core Features
1. Loading data from online store APIs
2. Storing data from online store APIs in a sqlite3 database
3. Displaying a list of unprocessed orders in a kivy user interface
4. Selecting an order from the list of unprocessed orders and displaying it's address label for copy/pasting
5. Error popup box that appears when there is an error, allowing you to copy paste the error instead of the app just burning to the ground :)
6. Displaying a list of items for a selected order
7. Button for changing an order from `unprocessed` to `shipped`

#### Extras
I added an extra feature to help compensate for the state of the unfinished prototype.
The use of a `configOverrides.json` file to allow the user to customise the applications behaviour. 
You can change
1. The location of the `.db` file.
2. The list of items to be loaded into the database
3. A section that makes it easy to configure new APIs and give them their own options
4. A section to customise the (non-functional) automated email system

#### Design Decisions

Given the limited time for this assignment, I made a couple design decisions which I will explain here.

##### The lack of classes to represent data

I didn't create an Order, Customer, Address, Listing or Item class.
I thought this would be unnecessary because the sqlite3 module gives you sqlite3.Row objects which
are guaranteed to have keys that are from the table columns in the database. 
You could say that turning these into classes would prevent a function from trying to access nonexistant keys (say, if you're given a row object from the wrong table)
I don't think that would be an issue, it's not difficult to make sure you pass a function the result of getOrder instead of getCustomer.

##### Email and address labels

Because I ran out of time, I thought it would be acceptable to put the automated emails and address labels in text boxes for the user to copy paste.
Rather than omitting this feature completely because I couldn't get automated email sending and automated printing going, instead I just put it in
a text box so that you could at least copy it over to a word document to print or email body to send.

## TODO List

If I had the time, I would have implemented these things. 
1. Get the proportions on the UI correct!!!
2. Automated email sending
3. Automated address label printing
4. Properly testing all StoreAPI child classes
5. A custom email screen

## Technical Details

### Initial setup

First you will need a python 3 installation that has the `venv` module installed.
Then, go to the root directory of this project and execute the following:
```
python -m venv .venv
cd .venv/Scripts
activate
cd ../../
pip install -r requirements.txt
```
or use this nice one-liner
```
python -m venv .venv & cd .venv/Scripts & activate & cd ../../ & pip install -r requirements.txt
```

Before you attempt to run any of the code, you should activate the virtual environment with
```
cd .venv/Scripts & activate & cd ../../
```

### Running tests

All the tests are written in separate files from the code they're testing, all test files are prefixed with `Test_`.
To run all the tests you can simply execute the following from the top-level directory
```
python -m unittest discover
```

### Running the application

Before you run the application you need to run the `webay.py` file, you can do this like any other python file
```
python webay.py
```

To run the application, you can run any of the following
```
python OnlineStoreApp
-- or --
python OnlineStoreApp/__main__.py
-- or --
python OnlineStoreApp/ui/App.py
```