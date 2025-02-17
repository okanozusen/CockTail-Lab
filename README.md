# CockTail-Lab
this is my first capstone project 
Okan Ozusen

# Gaming Lab 🎮
A social platform for gamers to connect, share, and chat.

## Features
- User Authentication (Signup/Login)
- Game Discussion Posts
- Friend System with Messaging
- Profile Customization (Profile Pics & Banners)

## Tech Stack
- **Frontend**: React, Context API
- **Backend**: Node.js, Express.js
- **Database**: PostgreSQL

## Setup Instructions
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/gaming-lab.git


Capstone proposal

	For this project Cocktail lab and for the tech at this moment I would like to use Flask since I really like python and am more interested in it. The project will be full stack using a backend such  as SQL for the databases of the alcohols and mixers and the front end for when you mix the alcohol and it shows the final product color. The frontend will allow people to choose and pick what alcohol and how much do they want to put. I will also implement different cup sizes such  as a big jug for jungle juice or a regular cocktail cup. This will be a website that aims for people that love to drink, bartenders that are curious on making a drink but not having the drinks and worrying if it’s gonna taste good. The website will provide a selection of different types of alcohols and mixers that they make their own cocktails and show the colors. This will be good for people wanting to make a new drink, for example a Halloween themed drink that is green and tastes good and strong. The API I will use is either Cocktail DB or Open Mixology API because they offer a wide selection of spirits. Another implementation I will put is users so users can always look back into what they made and also a little social media input where users can post on the website their new alcoholic cocktail and share their thoughts on it with other people commenting on it. The SQL database that I will make is the cocktail people favorite because on the website I will have popular cocktails that people can use as inspiration, and the ones they make so it saves on server.
# Remote version of README.md
This is the remote repository’s version.

## Database Schema 📊

Below is the database schema for Cocktail Lab:

ic.cocktails"
      Column      |       Type        | Collation | Nullable |                Default                | Storage  | Compression | Stats target | Description
------------------+-------------------+-----------+----------+---------------------------------------+----------+-------------+--------------+-------------
 id               | integer           |           | not null | nextval('cocktails_id_seq'::regclass) | plain    |             |              |
 name             | character varying |           | not null |                                       | extended |             |              |
 cup              | character varying |           | not null |                                       | extended |             |              |
 capacity         | integer           |           | not null |                                       | plain    |             |              |
 ingredients      | json              |           | not null |                                       | extended |             |              |
color            | character varying |           | not null |                                       | extended |             |              |
 sweetness        | double precision  |           |          |                                       | plain    |             |              |
 bitterness       | double precision  |           |          |                                       | plain    |             |              |
 smoothness       | double precision  |           |          |                                       | plain    |             |              |
 strength         | double precision  |           |          |                                       | plain    |             |              |
 freshness        | double precision  |           |          |                                       | plain    |             |              |
 enjoyment_rating | double precision  |           |          |                                       | plain    |             |              |
 final_strength   | double precision  |           |          |                                       | plain    |             |              |
 user_id          | integer           |           | not null |                                       | plain    |             |              |
                         | plain    |             |              |
https://cocktail-lab.onrender.com