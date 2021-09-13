async function fetchWithTimeout(resource, options = {}) {
    const {timeout = 1000} = options;

    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), timeout);

    const response = await fetch(resource, {
        ...options,
        headers: {'Content-Type': 'application/json'},
        mode: 'cors',
        signal: controller.signal
    });
    clearTimeout(id);

    return response;
}


async function checkGet(
    url,
    params = {method: "GET"},
    expectedCode = 200,
    expectedPayload = null
) {
    const req = `${params.method} ${url}`;

    const resp = await fetchWithTimeout(url, params);
    if (resp.status !== expectedCode) {
        return {
            ok: false,
            description: `Сервис ДОЛЖЕН вернуть ${expectedCode} на запрос "${req}", а вернул: ${resp.status} ${resp.statusText}`,
        };
    }

    const body = await resp.text();
    let payload = null;
    try {
        payload = JSON.parse(body);
    } catch (e) {
    }

    if (payload !== expectedPayload) {
        return {
            ok: false,
            description: `Сервис ДОЛЖЕН вернуть ${JSON.stringify(expectedPayload)} на запрос "${req}", а вернул: ${payload}`,
        };
    }

    return null;
}


const CHECKS = [
    {func: checkGet, params: {method: "GET"}, expectedStatus: 200, expectedPayload: null},
]


async function check(service) {
    let path = "/task/4/";
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

    let req = "";

    try {
        for (const checkSuite of CHECKS) {
            req = `${checkSuite.params.method} ${url}`;
            const resp = await checkSuite.func(
                url,
                checkSuite.params,
                checkSuite.expectedStatus,
                checkSuite.expectedPayload,
            );
            if (resp) {
                result = {...result, ...resp};
                break;
            }
        }
    } catch (e) {
        result = {
            ...result,
            ok: false,
            description: `невозможно сделать запрос ${req}. Пояснение от браузера: "${e.name === "AbortError" ? "таймаут" : e.message}"`,
        }
    }

    result.ms = performance.now() - result.ms;
    return result;
}


async function saveCheckResult(name, service, result) {
    const path = '/task4/check/';
    const payload = {
        description: result.description || null,
        ms: result.ms,
        name: name,
        ok: result.ok,
        service: service,
    }

    const resp = await fetchWithTimeout(
        path, {
            method: "POST",
            body: JSON.stringify(payload),
        });
    const resp2 = resp.clone();

    try {
        const checkObj = await resp.json();
        console.debug(`${resp.status} ${resp.statusText}\n${JSON.stringify(checkObj)}`);
    } catch (e) {
        const body = await resp2.text();
        console.debug(`${resp2.status} ${resp2.statusText}\n${body}\n`);
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

        const result = await check(service);
        await saveCheckResult(name, service, result);

        spanOk.textContent = result.ok ? "всё работает" : "есть проблемы";
        spanOk.style.color = result.ok ? "green" : "red";
        spanDescription.textContent = result.description;
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
