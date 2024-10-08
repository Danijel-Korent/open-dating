# Flask Dating App

## Running the app

- If desired, create a virtual environment and activate it.
- Install the requirements with `pip install -r requirements.txt`.
- Compile CSS by running `./tailwindcss -i static/styles/main.css -o static/styles/output.css --minify` (or if developing, run the Tailwind CLI in watch mode: `./tailwindcss -i static/styles/main.css -o static/styles/output.css --watch`).
- Run `python __init__.py`.
- Access the web app at `localhost:8080`

## Code structure
The below is a tree of the most important files and folders in the project:
```
dating-app/  
├─ static/                 contains static assets
│  ├─ images/  
│  ├─ styles/
│  ├─ js/
├─ templates/              contains Flask templates to be rendered
├─ db.py                   used to access mock_database.json
├─ mock_database.json      contains mock user data
├─ requirements.txt        lists all requirements of the project
├─ tailwindcss             TailwindCSS CLI, used for compiling CSS
├─ __init__.py             main Python file containing the main function
```
