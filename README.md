# TODO
- checar aggrid streamlit para reemplazar el dataframe de pandas
- checar el siguiente link para mejoras generales [tutorial](https://medium.com/@avra42/streamlit-python-cool-tricks-to-make-your-web-application-look-better-8abfc3763a5b)
- Investigar como hacer unit testing al menos en los modulos de data analysis
- Ir quitando los archivos de la carpeta functionality_tests, debido a que no son partes integradas al proyeto, son solo ejemplos.
- Separar codigo en carpetas
  
# Data Flow Diagram
Data inside DataShip follow the next diagram, if you expierence something not showed here open an issue in the [github repository](https://github.com/AgustinZavalaA/DataShip) 

<style>
    .mermaid svg { height: auto; }
</style>
```mermaid
graph TD
    Start[Start] -->|Click Home .Default.| uf(User upload file)
    Start --> User{User is logged in?}
    Start --> |Click Settings| set(Show user webapp settings)
    Start --> |Click Feedback| feed(Show user feedback form)

    uf --> valid{Is a valid file?}
    valid -->|no| fileerror(Notify the user that the current file has problems)-->Exit

    User --> |no| medn(Show user 'login' and 'signup' in sidebar)
    User --> |yes| medy(Show user 'My files' and 'Modules' in sidebar)

    medn --> |Click Login| login(Show user login form)
    medn --> |Click Signup| signup(Show user signup form)

    medy --> |Click My Files| myfiles(Show current user files)
    medy --> |Click Modules| mod(Show user list of modules)

    mod --> |User click1 module| userhavemodule{User have the module?}
    userhavemodule --> |no| addmodule[Add that module to current user in db]
    addmodule --> Exit
    userhavemodule --> |yes| donothing[Do nothing]
    donothing --> Exit[Return to start]

    set --> |User changes current configuration| applyset[Changes current settings to webapp]
    applyset --> user2{Uset is logged in?}
    user2 --> |no|donothing
    user2 --> |yes| applysetuser[Apply current changes to user and saves it to db] --> Exit

    myfiles --> |User select one file| valid

    login --> |User fill the login form| validuser[Log in or notify the user bad credentials]-->Exit
    signup --> |User fill the login form| validsignup[Save the user in db] --> Exit

    feed --> |User fill the feedback form|savefeed[Save the feedback post in the database] --> Exit

    valid --> |Yes| showdf(Show dataframe to user)
    showdf --> |User selects columns and data_analysis_module| verifydf{columns are valid?}
    verifydf --> |No| baddf[Notify the user currents columns and/or data_analysis_modules are invalid]
    baddf --> showdf
    verifydf --> |Yes| applymodule(Show module answers to user) --> Exit


    style showdf fill:green
    style applymodule fill:purple
    style validuser fill:red
    style validsignup fill:yellow
    style applysetuser fill:blue
    style addmodule fill:cyan
    style savefeed fill:#1AF399
```
The next tables show in more details the flow of the data in the colored boxes.
##  <span style="color:purple">Modules</span>
| Module name        | Module description | Input | Output method |
| ------------------ | ------------------ | ----- | ------------- |
| Mean               | ---                | ---   | ---           |
| Median             | ---                | ---   | ---           |
| Mode               | ---                | ---   | ---           |
| Standard Deviation | ---                | ---   | ---           |
| Variance           | ---                | ---   | ---           |
| Linear Regression  | ---                | ---   | ---           |
| Clusterization     | ---                | ---   | ---           |
| Graphing           | ---                | ---   | ---           |




# Project File Structure
The final project structure should look something like this:
```mermaid
graph LR;
DataShip_ --> demo_data

DataShip_ --> docs

DataShip_ --> src
src --> DataShip
DataShip --> db_management
DataShip --> main.py
DataShip --> data_analysis_modules
DataShip --> views

DataShip_ --> tests
tests --> db_tests
tests --> data_analysis_modules_tests
tests --> views_tests

style main.py fill:green;
```

# Requirements
- [Python](https://www.python.org/ "Python latest version")

# Installation
1. After installing python, download the current version of this repository, you can do it with the following command or download the zip archive and extract it:
``` bash
git clone https://github.com/AgustinZavalaA/DataShip.git
```
2. Open a terminal and navigate to the DataShip folder:
``` bash
cd DataShip
```
3. Run the following command to install all the dependencies:
``` bash
pip install -r requirements.txt
```
3.1. If you don't have a database, you can create one with the following command:
``` bash
python src/DataShip/db_management/db_manager.py -cps
```
where the parameters are:
- `-c`: create the database
- `-p`: populate the database with demo data
- `-s`: show the database
   
1. Run the following command to run the DataShip application:
``` bash
python -m streamlit run src/DataShip/main.py
```
or if you want to run the application in debug mode:
``` bash
python -m streamlit run src/DataShip/main.py --debug
```