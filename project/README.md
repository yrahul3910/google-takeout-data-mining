# Obtaining the data
====================
Go to [Google Takeout](https://takeout.google.com) and request a copy of your data. Select the following:
* Contacts
* Fit
* Google Account
* Hangouts
* Location History
* Maps
* Maps (your places)
* My Activity
* Search contributions
* Shopping Lists
* YouTube and YouTube Music

Download the files. In the YouTube and YouTube Music folder, delete the videos folder. This saves disk space.


# Fit:
======

Data description:
=================
The `Activities` folder has XML files (.tcx) for each activity. The filename ends with the activity performed. This in turn can help determine what products the user may buy. The XML structure has <TotalTimeSeconds>, <Calories>, <StartTime>, and <DistanceMeters> keys. The `Daily activity metrics` may not be particularly helpful.

What can we find out:
=====================
* Activities
  * Use <StartTime> to see what part of the day user is active
  * Use <Calories> + an estimate of the idle calories burned to estimate user health
  * Use <DistanceMeters> to see if user is involved in, say, 5k, and needs equipment for that


# Location History:
===================

Data description:
=================
??

What can we find out:
=====================
??


# Maps:
=======

Data description:
=================
* Photos contribution has JSON files that store EXIF data for each photo. This may be useful.
* My labeled placed has a JSON file with locations and labels. This could be used to determine the distance between Home and Work, or other pairs of places, find the distance using an API, and compute an estimate of the fuel requirements.
* Commute settings has a JSON that can be used in addition to the above to decide if the user has a car.

What can we find out:
=====================
* Does the user have a car?
* How much does the user travel monthly?
* What is the fuel estimate of the user per month?
* Who are the user's friends?


# YouTube and YouTube Music:
============================

Data description:
=================
* playlists has a JSON for each playlist, aside from Watch later and Liked videos.
* subscriptions has a JSON of subscriptions. We can mine the description for interests.

What can we find out:
=====================
* Topics of interest to the user


# Future Scope
==============
Use the Contacts from Google Takeout, mine each of them. See if they have had any influence. What topics do they like? Recommend the same to the user.