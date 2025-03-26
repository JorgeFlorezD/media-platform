
# How to execute

There is a docker-compose file that contains the definition to launch the containers. In this way it is easier to run the tech test without the need of install packages in a local environment
- mongo: the database containing collections for channels and contents
- platform, which is the container that contains the logic for the media application
- mongo_seed: used to load initial data to the mongo container (the data is in the mongo_seed folder)
to run the containers, just
```
docker-compose up
```
# How to run the unit tests
```
docker exec --env-file .env -it media.platform sh -c "pytest"
```

# How to run the script to generate the ratings for the Channels
```
docker exec --env-file .env -it media.platform sh -c "python scripts/calculate_ratings.py"
```
The script is generated in the folder ./scripts/rating_reports/ inside the container. The format of the name of the files is `ratings_<timestamp>.csv` . There is an example of the result of the script in the local folder with the same name.

# Structure of the project
I project have the following structure:
```
--app
  |-- adapters
      |-- api
      |-- repositories
  |-- aplication
  |-- domain
```

## API
Contains the definition of the API (media_api.py). It includes the following endpoints:

- **GET /media/channel/{channel_id}**
Return the information of a channel by its ID
<br/>
- **GET /media/first_level_channels**
Return the first level channels, that is, the channels that are not underneath  another channels
<br/>
- **GET /channel/{channel_id}/channels**
Return the subchannels of a given channel_id. This endpoints will return the direct child channels. However, in case it is needed, it is possible to return as many sublevels as needed. This is defined by means of the constant MAX_SUBCHANNEL_LEVEL in the API file. Currently, it is set to 1, but it can be change in order to obtaine more sublevel channels of the given channel_id. 
<br/>
- **GET /media/content/{content_id}**
Return the information of a content by its ID

## Repositories

#### DB Models
DB models (MongoDB documents) of the channels and contents (`channel_db.py and content_db.py`)

### Mappers
Maps from the DB Models to the domain models (`channel_mapper.py and content_mapper.py`)

### Repositories
Contains the logic to get the information from MongoDB into the DB Models, and use the mapper to return domain models.

The `channel repository` uses the graphlookup pipeline (`pipelines.py`) which allows to efficiently return all the children of a node, or limit the number of sublevels. The script that generates the ratings for all the channels uses this specific feature of the channel repository.

### Domain
Contains the domain models for channel and contents (`channel.py and content.py`).

### Application
Contain the services that contain the domain logic (channel_service.py and content_service.py). The services are used in the endpoints to get the results to return to the client.

## Development of the tech test

### Database Model
- There are collection for channels and contents
- Apart from the required fields, a channel contains a field called "parents" with the list of the IDs of its parents (a channel can have many channel parents).
- A channel can contain a field called contents with the list of the IDs of the contents (IDs from the content collection)
- A channel without parent is called "fist level channels"

### How to expect that FE works
- First obtain the first level channels, and then request subchannels and contents using the endpoints.

### Calculation of the Ratings of all the channels
The entry of the script is in the file `scripts/calculate_rating.py`. This file makes a call to a method in the channel service which contains the login to generate a dict with the information about titles and ratings, ordered by rating. Once the information is generated, the file is created.
The script loads the first level channels, and for each one, obtains all his childrens, and calculates the rating in a deep search. In this manner we avoid loading all the channels for all the first level ones.
Moreover, the csv dict is being created, so if a rating for a channel is already calculated, it avoids processing the children of such nodes and just gets its current rating.

