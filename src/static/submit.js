// Good practive would have been to write those little script in a TypeScript format, which I did not do as it was very limited.
submitCalc = async () => {
    const operation = document.getElementById("NPIInput").value
    const request = new Request(`${window.location.origin}/calc`, {
        method: "POST",
        body: JSON.stringify({
            operation: operation
        }),
        headers: new Headers({ "Content-Type": "application/json" }),
    });

    const response = await fetch(request).then((res) => {
        return res.json();
    });

    const result = document.getElementById("result");
    if (!response.result) {
        result.innerHTML = `An error occured for the operation <strong>"${operation}"</strong>: ${response.detail}`;
        return
    }

    result.innerHTML = `The result of the operation <strong>"${operation}"</strong> is ${response.result}`;

    await getHistory();
}

getHistory = async () => {
    const request = new Request(`${window.location.origin}/calc`, {
        method: "GET",
        headers: new Headers({ "Content-Type": "application/json" }),
    });

    const response = await fetch(request).then((res) => {
        return res.json();
    });

    const history = document.getElementById("history");
    history.innerHTML = response.history;
    history.style.height = 'auto';
    history.style.height = history.scrollHeight+'px';
}

getHistory();
