# expense-tracker-REST-API

REST API for managing a list of expenses.\
Uses JWT for authenticating users.\
Passwords and tokens are hashed before being stored in the database.

## Table of Contents

- [Local Setup](#local-setup)
- [Enviroment Files](#enviroment-files)
- [How to Use](#how-to-use)
- [License](#license)
- [Credits](#credits)

## Local Setup

1. Have Python 3.13+ installed.
2. Clone the repository.
3. Create local enviroment, for example by running `py -m venv venv` on Windows.
4. Install requirements from [requirements.txt](requirements.txt).
5. Create files from [Enviroment Files](#enviroment-files).

## Enviroment Files

You need `.env` file, that can be created based on [.env.example](.env.example) file.\
Also you need `hash.py` file, that contains tables to hash strings and place it in `expenseAPI/Views/` directory.

## How to Use

1. Add new user by sending HTTP POST request on /users/ endpoint (you can see a list of all users by sending GET request on this endpoint).
2. In response you get a token, that is necessary to make any data-changing operations.
3. Make a proper request to one of the provided endpoints.

For a full list of endpoints see [endpoints.md](docs/endpoints.md).

## License

See [License](License)

## Credits

Project idea: [roadmap.sh](https://roadmap.sh/projects/expense-tracker-api)
