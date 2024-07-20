# Rika Bot

## Dependencies

Docker and Docker Compose are required to run the bot.

## Installation

Copy .env.example to .env and fill in the required values.

Export the environment variables in the .env file.
```bash
source env-export.sh
```

Run the following command to build and run the bot.

```bash
docker-compose -f compose.yaml up -d --build
```


