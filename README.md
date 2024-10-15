Python version required: 3.10.13

To install dependancy you can use `pip install -r test_requirements.txt`, but it can be run through dockers.

---

To run the test with dockers: `make exec-tests`
To deploy the web server: `make build` then `make depoy`
To drop the database: `make cleanup`

---

The local server can be accessed through: `http://localhost:5000/`
Automatic generated doc can be accessed through: `http://localhost:5000/docs`
