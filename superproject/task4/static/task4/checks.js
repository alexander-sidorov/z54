async function fetchWithTimeout(resource, options = {}, name = "") {
    const {timeout = 4000} = options;

    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), timeout);

    let headers = new Headers();
    headers.set("Content-Type", "application/json");

    if (name && name.length) {
        headers.set("X-User", name);
    }

    let request = `${options.method} ${resource} HTTP/1.1\n`;
    headers.forEach((value, header) => {
        request += `${header}: ${value}\n`
    })

    if (options.body) {
        request += `\n${options.body}`;
    }

    request += '\n\n\n\n----------------\n\n';

    const response = await fetch(resource, {
        ...options,
        headers: headers,
        mode: 'cors',
        credentials: 'include',
        signal: controller.signal
    });
    clearTimeout(id);

    return {response: response, request: request};
}


async function checkEdgeCases(url, name) {
    // 1. check method
    let rr = await fetchWithTimeout(url, {method: "GET"}, name);
    let resp = rr.response;

    if (resp.status !== 405) {
        throw Error(
            rr.request +
            `Сервер должен был вернуть статус 405,` +
            ` а вернул ${resp.status} ${resp.statusText}.` +
            `\nТолько метод POST должен быть разрешён для этой задачи.`
        );
    }

    // 1. check anonymous
    rr = await fetchWithTimeout(url, {method: "POST", body: "0"});
    resp = rr.response;

    if (resp.status !== 403) {
        throw Error(
            rr.request +
            `Сервер должен был вернуть статус 403,` +
            ` а вернул ${resp.status} ${resp.statusText}.` +
            `\nАнонимным пользователям должно быть запрещено делать запросы.`
        );
    }

    // 2. check positive range
    let n = 101;
    let body = JSON.stringify(n);
    rr = await fetchWithTimeout(url, {method: "POST", body: body}, name);
    resp = rr.response;

    if (resp.status !== 422) {
        throw Error(
            rr.request +
            `Сервер должен был вернуть статус 422,` +
            ` а вернул ${resp.status} ${resp.statusText}.` +
            `\nЧисло ${n} должно быть за границей допустимого.`
        );
    }

    // 3. check negative range
    n = -101;
    body = JSON.stringify(n);
    rr = await fetchWithTimeout(url, {method: "POST", body: body}, name);
    resp = rr.response;

    if (resp.status !== 422) {
        throw Error(
            rr.request +
            `Сервер должен был вернуть статус 422,` +
            ` а вернул ${resp.status} ${resp.statusText}.` +
            `\nЧисло ${n} должно быть за границей допустимого.`
        );
    }

    // 3. check unknown input
    n = Math.floor(Math.random() * 10).toString();
    body = JSON.stringify(n);
    rr = await fetchWithTimeout(url, {method: "POST", body: body}, name);
    resp = rr.response;

    if (resp.status !== 422) {
        throw Error(
            rr.request +
            `Сервер должен был вернуть статус 422,` +
            ` а вернул ${resp.status} ${resp.statusText}.` +
            `\nВвод ${body} должен восприниматься сервером как неизвестный и неподдерживаемый.`
        );
    }
}


async function checkHappyPath(url, name) {
    // 1. send 'stop'
    let body = JSON.stringify("stop");
    let rr = await fetchWithTimeout(url, {method: "POST", body: body}, name);
    let resp = rr.response;

    if (resp.status !== 200) {
        throw Error(
            rr.request +
            `Сервер должен был вернуть статус 200,` +
            ` а вернул ${resp.status} ${resp.statusText}.`
        );
    }

    body = await resp.text();
    let payload = null;
    try {
        payload = JSON.parse(body);
    } catch (e) {
    }

    if ((typeof payload) !== "number") {
        throw Error(
            rr.request +
            `Сервер должен был вернуть число,` +
            ` а вернул ${body}.`
        );
    }

    // 2. send number
    const n = Math.floor(Math.random() * 100);
    body = JSON.stringify(n);
    rr = await fetchWithTimeout(url, {method: "POST", body: body}, name);
    resp = rr.response;

    if (resp.status !== 200) {
        throw Error(
            rr.request +
            `Сервер должен был вернуть статус 200,` +
            ` а вернул ${resp.status} ${resp.statusText}.`
        );
    }

    body = await resp.text();
    let payload2 = null;
    try {
        payload2 = JSON.parse(body);
    } catch (e) {
    }

    if ((typeof payload2) !== "number") {
        throw Error(
            rr.request +
            `Сервер должен был вернуть число,` +
            ` а вернул ${body}.`
        );
    }
    if (payload2 !== (payload + n)) {
        throw Error(
            rr.request +
            `Сервер должен был вернуть ${payload + n} = ${payload} + ${n},` +
            ` а вернул ${payload2}.`
        );
    }

    // 3. send -number
    body = JSON.stringify(-n);
    rr = await fetchWithTimeout(url, {method: "POST", body: body}, name);
    resp = rr.response;

    if (resp.status !== 200) {
        throw Error(
            rr.request +
            `Сервер должен был вернуть статус 200,` +
            ` а вернул ${resp.status} ${resp.statusText}.`
        );
    }

    body = await resp.text();
    let payload3 = null;
    try {
        payload3 = JSON.parse(body);
    } catch (e) {
    }

    if ((typeof payload3) !== "number") {
        throw Error(
            rr.request +
            `Сервер должен был вернуть число,` +
            ` а вернул ${body}.`
        );
    }
    if (payload3 !== payload) {
        throw Error(
            rr.request +
            `Сервер должен был вернуть ${payload} = ${payload} + ${-n} + ${n},` +
            ` а вернул ${payload3}.`
        );
    }
}


async function check(service, name) {
    let path = "/task4/";
    let scheme = "http://";

    if (service.endsWith("/")) {
        path = path.substr(1);
    }
    if (service.startsWith("http://") || service.startsWith("https://")) {
        scheme = "";
    }

    let url = `${scheme}${service}${path}`;

    let result = {
        ok: true,
        description: null,
        ms: performance.now(),
    }

    try {
        await checkEdgeCases(url, name);
        await checkHappyPath(url, name);
    } catch (e) {
        result = {
            ...result,
            ok: false,
            description: e.message,
        }
    }

    result.ms = Math.floor(performance.now() - result.ms);
    return result;
}


async function saveCheckResult(service, name, result) {
    const path = '/task4/check/';
    const payload = {
        description: result.description || null,
        ms: result.ms,
        name: name,
        ok: result.ok,
        service: service,
    }

    const rr = await fetchWithTimeout(
        path, {
            method: "POST",
            body: JSON.stringify(payload),
        });
    const resp = rr.response;

    try {
        const body = await resp.text();
        try {
            const checkObj = JSON.parse(body);
            console.debug(`${resp.status} ${resp.statusText}\n${JSON.stringify(checkObj)}`);
        } catch (e) {
            console.debug(`json error:\n${resp2.status} ${resp2.statusText}\n${body}\n`);
        }
    } catch (e) {
        console.debug(`fetch error:\n${resp2.status} ${resp2.statusText}\n`);
    }

}


async function loadUserData() {
    return {
        name: localStorage.getItem("task4/name") || "",
        service: localStorage.getItem("task4/service") || "",
    }
}


async function storeUserData(service, name) {
    localStorage.setItem("task4/name", name);
    localStorage.setItem("task4/service", service);
}


async function setUp() {
    let inputName = document.getElementById("id_name");
    let inputService = document.getElementById("id_service");
    let btnCheck = document.getElementById("id_check");
    let sectionResults = document.getElementById("id_results");
    let spanOk = document.getElementById("id_ok");
    let spanDescription = document.getElementById("id_description");
    let spanTiming = document.getElementById("id_timing");

    const userData = await loadUserData();
    inputName.value = userData.name;
    inputService.value = userData.service;

    const checkEventHandler = async function (event) {
        sectionResults.hidden = true;

        const name = inputName.value;
        const service = inputService.value;

        if (!name.length) {
            alert("Необходимо представиться!");
            inputName.focus();
            return;
        }
        if (!service.length) {
            alert("Необходимо указать УРЛ или хост сервиса!");
            inputService.focus();
            return;
        }

        await storeUserData(service, name);

        const result = await check(service, name);
        await saveCheckResult(service, name, result);

        if (result.ok) {
            spanOk.textContent = "всё работает";
            spanOk.style.color = "green";
            spanDescription.parentElement.hidden = true;
        } else {
            spanOk.textContent = "есть проблемы";
            spanOk.style.color = "red";
            spanDescription.textContent = result.description;
            spanDescription.parentElement.hidden = false;
        }

        spanTiming.textContent = result.ms.toFixed(0).toString();

        sectionResults.hidden = false;
    };

    const checkEventHandlerOnEnter = async function (event) {
        if (event.code === "Enter") {
            event.preventDefault();
            return await checkEventHandler(event);
        }
    };

    btnCheck.addEventListener("click", checkEventHandler);
    inputName.addEventListener("keyup", checkEventHandlerOnEnter);
    inputService.addEventListener("keyup", checkEventHandlerOnEnter);
}


document.addEventListener("DOMContentLoaded", setUp);
