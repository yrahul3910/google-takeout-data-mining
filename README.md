# Obtaining the data
Go to [Google Takeout](https://takeout.google.com) and request a copy of your data. Select the following:
* Chrome
* Fit
* Hangouts
* Location History
* Mail
* Maps
* Maps (your places)
* My Activity
* Search contributions
* YouTube and YouTube Music

Download the files. In the YouTube and YouTube Music folder, delete the videos and uploads folders. This saves disk space. Put the `Takeout` folder in a directory called `data/<name>`, so that the directory structure is `data/<user>/Takeout`.

# Setting up the code

1. **Obtain an API key.**
    1. Go to the [Google Cloud APIs dashboard](https://console.cloud.google.com/apis/credentials), select Create Credentials, followed by API Key. Copy the key.
    2. Restrict your API key. Click on your newly generated key, and under API Restrictions, select Restrict Key. In the search box, type in "Distance Matrix API", "Places API", and "Geocoding API". Restrict the key to these APIs.
    3. Use the sidebar to go to the dashboard, click Enable APIs and Services, and enable those two APIs.
2. **Set up Google Cloud billing.** You may need to set up your Google Cloud account with billing information. You can do so in the Billing section of the sidebar.
3. **Create a .env file.** This will hide your API key. **DO NOT COMMIT THIS FILE.** If you do, anyone will be able to access the APIs and you will be billed for it. If you're feeling altruistic, donate instead. In this file, add in one line, `KEY=<your API key>`.
4. **Install the requirements.** Run `python3 -m pip install -r requirements.txt` to do this.
5. **Run the code.** Run `python3 main.py`

You should now be able to run the code.

# Running tests

To run tests, in the project root directory, run

```{sh}
./tests/test.sh --coverage
```

The `--coverage` option shows a coverage report. You may omit it if desired.

# Chrome

## Data description
The `Autofill.json` file contains auto-fill data saved in Google Chrome. This contains address information that can be mined. The `BrowserHistory.json` file contains browser history. We mine this file for page titles.

## What can we find out
* Where the user lives, and therefore, nearby places
* Pages the user visited, and therefore, potential interests

# Fit

## Data description
The `Activities` folder has XML files (.tcx) for each activity. The filename ends with the activity performed. This in turn can help determine what products the user may buy. The XML structure has <TotalTimeSeconds>, <Calories>, <StartTime>, and <DistanceMeters> keys. The `Daily activity metrics` may not be particularly helpful.

## What can we find out
* Activities
  * Use <StartTime> to see what part of the day user is active
  * Use <Calories> + an estimate of the idle calories burned to estimate user health
  * Use <DistanceMeters> to see if user is involved in, say, 5k, and needs equipment for that


# Maps

## Data description
* Photos contribution has JSON files that store EXIF data for each photo. This may be useful.
* My labeled placed has a JSON file with locations and labels. This could be used to determine the distance between Home and Work, or other pairs of places, find the distance using an API, and compute an estimate of the fuel requirements.
* Commute settings has a JSON that can be used in addition to the above to decide if the user has a car.

## What can we find out
* Does the user have a car?
* How much does the user travel monthly?
* What is the fuel estimate of the user per month?
* Who are the user's friends?


# YouTube and YouTube Music

## Data description
* playlists has a JSON for each playlist, aside from Watch later and Liked videos.
* subscriptions has a JSON of subscriptions. We can mine the description for interests.

## What can we find out
* Topics of interest to the user


# Future Scope
Use the Contacts from Google Takeout, mine each of them. See if they have had any influence. What topics do they like? Recommend the same to the user.
