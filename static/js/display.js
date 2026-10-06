function createWaitingContent() {
    const waiting = document.createElement("div");
    waiting.className = "waiting";

    const title = document.createElement("strong");
    title.textContent = "Klar";

    const text = document.createElement("span");
    text.textContent = "Scan NFC-tag for at starte";

    waiting.appendChild(title);
    waiting.appendChild(text);

    return waiting;
}


function createActiveContent(state) {
    const fragment = document.createDocumentFragment();

    const status = document.createElement("div");
    status.className = "status-badge";
    status.textContent = "Aktiv ekspedition";

    fragment.appendChild(status);


    const balanceInfo = document.createElement("div");
    balanceInfo.className = "balance-info";

    const balanceText = document.createTextNode(
        "Registreret saldo: "
    );

    const balanceValue = document.createElement("strong");
    balanceValue.textContent = state.starting_balance;

    balanceInfo.appendChild(balanceText);
    balanceInfo.appendChild(balanceValue);

    fragment.appendChild(balanceInfo);


    const prizeList = document.createElement("div");
    prizeList.className = "prize-list";


    const header = document.createElement("div");
    header.className = "prize-row prize-row--header";

    const headerName = document.createElement("span");
    headerName.textContent = "Gevinst";

    const headerPrice = document.createElement("span");
    headerPrice.textContent = "Pris";

    header.appendChild(headerName);
    header.appendChild(headerPrice);

    prizeList.appendChild(header);


    if (state.prizes.length > 0) {

        for (const prize of state.prizes) {

            const row = document.createElement("div");
            row.className = "prize-row";

            const name = document.createElement("span");
            name.textContent = prize.name;

            const price = document.createElement("span");
            price.textContent = `-${prize.price}`;

            row.appendChild(name);
            row.appendChild(price);

            prizeList.appendChild(row);
        }

    } else {

        const empty = document.createElement("div");
        empty.className = "empty-message";
        empty.textContent = "Ingen gevinster scannet endnu.";

        prizeList.appendChild(empty);
    }


    fragment.appendChild(prizeList);


    const total = document.createElement("div");
    total.className = "display-total";

    const totalLabel = document.createElement("span");
    totalLabel.textContent = "TOTAL";

    const totalValue = document.createElement("strong");
    totalValue.textContent = state.remaining_balance;

    total.appendChild(totalLabel);
    total.appendChild(totalValue);

    fragment.appendChild(total);


    return fragment;
}


function renderSide(side, state) {
    const container = document.getElementById(
        `${side}-content`
    );

    container.replaceChildren();

    if (
        state.active &&
        state.side === side
    ) {
        container.appendChild(
            createActiveContent(state)
        );

        return;
    }

    container.appendChild(
        createWaitingContent()
    );
}


async function updateDisplay() {
    try {
        const response = await fetch(
            "/api/state",
            {
                cache: "no-store"
            }
        );

        if (!response.ok) {
            throw new Error(
                `HTTP ${response.status}`
            );
        }

        const state = await response.json();

        renderSide(
            "left",
            state
        );

        renderSide(
            "right",
            state
        );

    } catch (error) {
        console.error(
            "Kunne ikke opdatere PrizePoint:",
            error
        );
    }
}


updateDisplay();

setInterval(
    updateDisplay,
    500
);