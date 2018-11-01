# ARUP Concept Project

A Dockerized Mongodb-backed demo project using Graphene and Flask.

## Requirements

Docker Compose must be installed to build from the included 'docker-compose.yml' file.

## Setup

Clone this repo, then run `docker-compose up --build` as root or as a user who can execute docker-compose commands.

Wait until all required components are fetched and the server is running before continuing. This all should happen automagically, with a docker repository containing a mongo database downloaded and populated with dummy data. 

## Testing GraphQL

Open http://localhost:8082 to begin. 

To explore the schema, click the `< Docs` button at the top right to open a utility. 

ID's are incremental and are designated as follows (to explore the dummy data itself, be sure to check out setup.py):
* `11** - Wands`
* `12** - Actors`
* `13** - Movies`
* `14** - Characters`

### Getting a single wand
```
query {
  wand(id: 1100) {
    wood
    core
    length
    description
  }
}
```

### Getting a list of all characters 
```
query {
  allCharacters{
    id
    name
    actor{
      name
    }
    house
    wand{
      wood
      core
    }
  }
}
```

### Getting a list of all characters that appear in a specific movie
```
query {
  characterAppearsIn(appearsIn: 1300){
    id
    name
  }
}
```

### Creating a character
```
mutation createCharacter {
  createCharacter(actor: 1200, appearsIn: [1300, 1301, 1302, 1303, 1304, 1305, 1306, 1307], name: "Hagrid"){
    character{
      id
      name
      appearsIn {
        id
      }
    }
  }
}
```
