# Stalkator

## Table of contents
* [General info](#general-info)
* [Requirements](#requirements)
* [Setup](#setup)
* [Patch notes](#patch-notes)

## General info
This is a program to scrape data on social media, such as instagram, linkedin, facebook...

You can connect multiples account with one server in order to have a more accurate scrapping (when it comes to followers and following since you can't view them all at once)

**The targeted account must be accessible from the one you're connected to !**

For now it only:
* Scrape instagram followers and following
* Save photos of an instagram account

## Requirements
Libraries:
* Selenium
* Pandas
* Requests

Other:
* Windows
* Google chrome up to date

## Setup
* Step I - Launch the server
* Step II - Launch the clients (it will connect to the server automatically)
* Step III - Connect all your accounts
* Step IV - Set a target then scrape the data

## Patch notes

* **V0.2:**
    * Support for server/clients
    * Configuration files
* **V0.2b:**
    * Code rearranged
    * Get photos of an account
* **V0.3:**
    * Graphical interface (GUI)
* **V0.3b: (soon)**
   * Bugfixes, exceptions handling, etc..
* **V0.4:**
    * Database sqlite3
* **V0.5:**
    * Facial recognition, spotting (openCV + facenet)
    * Improving scrapping of photos (only thoses with faces, only target...)
* **V0.6:**
    * Automated standby (Likes/Comments/Followers change)
* **V0.7:**
    * Android application and notifications about changes from a specific target
* **V0.8:**
    * Support for Facebook (same actions)
