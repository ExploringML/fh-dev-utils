# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_serve_dev.ipynb.

# %% auto 0
__all__ = ['serve_dev', 'cache_buster']

# %% ../nbs/00_serve_dev.ipynb 4
from fasthtml.common import *
import subprocess
from time import time

# %% ../nbs/00_serve_dev.ipynb 6
def serve_dev(
    app='app',                 # FastHTML (Starlette) class instance
    host='0.0.0.0',            # Uvicorn host
    port=None,                 # Uvicorn port
    reload=True,               # Uvicorn reload status
    reload_includes=None,      # Files to watch to reload Uvicorn
    reload_excludes=None,      # Files to exclude from watching to reload Uvicorn
    sqlite_port=8035,          # sqlite-web port
    db=False,                  # Enable SQLIte browser
    db_path='data/app.db',     # SQLite database path
    jupyter=False,             # Enable Jupyter Lab
    jupyter_port=8036,         # Jupyter Lab port
    tw=False,                  # Enable TailwindCSS
    tw_src='./app.css',        # TailwindCSS source file
    tw_dist='./public/app.css' # TailwindCSS output file
):
    "Utility function to start FastHTML, TailwindCSS, Jupyter Lab, and SQLite in development mode"
    import inspect
    frame = inspect.currentframe().f_back
    module = inspect.getmodule(frame)
    
    # Check if this is the main module
    if module.__name__ != '__main__':
        return

    appname = module.__name__

    if tw:
        print("Watching for TailwindCSS class changes...")
        tailwind_process = subprocess.Popen(
            ['tailwindcss', '-i', tw_src, '-o', tw_dist, '--watch'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    if db:
        #print("Starting SQLite...")
        sqlite_process = subprocess.Popen(
            ['sqlite_web', db_path, '--port', str(sqlite_port), '--no-browser'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f'SQLite link: http://localhost:{sqlite_port}')

    if jupyter:
        #print("Starting Jupyter...")
        jupyter_process = subprocess.Popen(
            ['jupyter', 'lab', '--port', str(jupyter_port), '--no-browser', '--NotebookApp.token=', '--NotebookApp.password='],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
            text=True
        )

        # Extract and print the Jupyter Lab URL
        for line in jupyter_process.stderr:
            if 'http://' in line:
                match = re.search(r'(http://localhost:\d+/lab)', line)
                if match:
                    print(f'Jupyter Lab link: {match.group(1)}')
                    break

    try:
        #print("Starting FastHTML...")
        serve(appname=appname, app=app, host=host, port=port, reload=reload, reload_includes=reload_includes, reload_excludes=reload_excludes)
    finally:
        if db:
            sqlite_process.terminate()
        if jupyter:
            jupyter_process.terminate()
        if tw:
            tailwind_process.terminate()


# %% ../nbs/00_serve_dev.ipynb 8
def cache_buster():
	"Helps to avoid browser caching of dynamically generated CSS during development"
	return f"?v={int(time())}"
