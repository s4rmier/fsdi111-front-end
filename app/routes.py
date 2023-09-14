from flask import (
    Flask,
    request,
    render_template
)

import requests  # not to be confused with "request" above
from requests.exceptions import ConnectionError
app = Flask(__name__)
BACKEND_URL = "http://127.0.0.1:5000/tasks"

# quick test/example:


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/about")
def about_me():
    me = {
        "first_name": "Romnick",
        "last_name": "Sarmiento",
        "hobbies": "Gaming",
        "bio": "Romnick is a student at SDGKU"
    }
    return render_template("about.html", user=me)


@app.get("/tasks")
def task_list():
    try:
        response = requests.get(BACKEND_URL)
        if response.status_code == 200:
            task_list = response.json().get("tasks")
            return render_template("list.html", tasks=task_list)
        return (
            render_template("error.html", err=response.status_code),
            response.status_code
        )
    except ConnectionError as conn_err:
        return (
            render_template("error.html", err=500),
            500
        )


@app.get("/tasks/edit/<int:pk>")
def edit_task(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.get(url)
    if response.status_code == 200:
        task_data = response.json().get("task")
        return render_template("edit.html", task=task_data)
    return (
        render_template("error.html", err=response.status_code),
        response.status_code
    )


@app.post("/tasks/edit/<int:pk>")
def edit_task_req(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    task_data = request.form
    response = requests.put(url, json=task_data)
    if response.status_code == 204:
        return render_template("success.html")
    return (
        render_template("error.html", response.status_code),
        response.status_code
    )
