# The Python Glasgow Meetup Archive 🐍

Data can be pulled from:

[https://raw.githubusercontent.com/python-glasgow/meetups/refs/heads/main/archive.json](https://raw.githubusercontent.com/python-glasgow/meetups/refs/heads/main/archive.json)

## Run the archive app

* install uv ([Instructions](https://docs.astral.sh/uv/getting-started/installation/))
* clone repo
* `uv sync`
* `uv run flask run`
* visit http://127.0.0.1:5000

## Adding or Updating a Talk or Workshop

* fork this repo
* create a new branch for your changes
* install uv (if you haven't already)
* run the archive app `uv run flask run` on the new branch
* visit http://127.0.0.1:5000
* use the web app to make your changes
* go back to the home page and click 'Write to Archive'
* commit both `archive.json` and `main.db`
* create a PR
* after the PR has been accepted delete your branch

## I don't want to use uv

1. Create a virtual environment in the project folder and activate it:

```text
# Linux
cd /path/to/project-folder

# Windows
cd C:\path\to\project-folder
```

**Linux / MacOS**

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

**Windows**

```bash
python -m venv venv
```

```bash
.\venv\Scripts\activate
```

2. Install from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

3. Run the archive app:

```bash
flask run
```