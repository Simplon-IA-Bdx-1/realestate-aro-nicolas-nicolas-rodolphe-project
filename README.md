# CUSTOM REAL ESTATE PREDICTION

## Project definition

We had to build an end-to-end machine learning project.  
The goal of this project is to predict real estate houses prices.

For now, we only focusing to the Gironde area.

## Steps to make it work

### Prerequisites

Clone this repo and access it from the command line: `git clone https://github.com/Simplon-IA-Bdx-1/realestate-aro-nicolas-nicolas-rodolphe-project.git`.

#### Anaconda

If you want, you can install [conda](https://docs.conda.io/en/latest/miniconda.html) to manage environments on your machine.  
Create a conda env with this command: `conda env create -f ./env/environment.yml` at the root of the repo.

#### Virtual env

For Linux :
  - Create an [environment](https://virtualenv.pypa.io/en/stable/) at the root of the repo: `python3 venv venv/`
  - Acivate it `source venv/bin/activate`
  - You can now install the dependencies with the `pip install -r ./env/requirements.txt` command.

For Windows :
  - Create an environement at the root of the repo : `python -m venv envImmo`
  - Activate it move to `envImmo\Scripts` then `activate`
  - Back to the root of repo.
  - You can now install the dependencies with the `pip install -r ./env/requirements.txt` command.

### The app

You're now ready to launch the application via the following command line `python app.py` and fire your first prediction.

### Expiriments

See Branch develop/Labo for see details of model's and Pipeline
