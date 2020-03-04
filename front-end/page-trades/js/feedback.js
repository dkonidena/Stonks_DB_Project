const NAMES = {
    buyingParty: "Buyer",
    maturityDate: "Maturity Date",
    notionalCurrency: "Notional Currency",
    notionalPrice: "Notional Price",
    product: "Product",
    quantity: "Quantity",
    sellingParty: "Selling Party",
    strikePrice: "Strike Price",
    underlyingCurrency: "Underlying Currency",
    underlyingPrice: "Underlying Price"
};

var suggestions = {};

function getFeedback() {
    let trade = tradeObjectFromForm().getAPIObject();
    api.post.check_trade(trade, (res) => handleFeedback(res, trade), showError);
}

function handleFeedback(response, current) {
    $("#suggestions").empty();

    let suggested = new Trade();
    suggested.populateFromServerJSON(response);
    suggested = suggested.getAPIObject();

    for (const field in NAMES) {
        let suggestedValue = suggested[field];
        let currentValue = current[field];

        if (field === "maturityDate") {
            // only compare day & month of date and not the time
            currentValue = currentValue.substring(0,10);
            suggestedValue = suggestedValue.substring(0,10);
        }

        if (currentValue !== suggestedValue)  {
            addSuggestion(field, currentValue, suggestedValue);
        }
    }

    if (allSuggestionsResolved()) {
        $("#saveTradeButton").text("Save Trade");
    }
    $("#suggestionsTable").show();
}

function allSuggestionsResolved() {
    return Object.keys(suggestions).length == 0;
}

function ignoreAll() {
    Object.keys(suggestions).forEach(removeSuggestion);
}

function acceptAll() {
    Object.keys(suggestions).forEach(acceptSuggestion);
}

function acceptSuggestion(field) {
    let value = suggestions[field];
    switch (field) {
        case "buyingParty":
            elements.buyingPartyInput.val(companyIDToName(value)).trigger("change");
            break;
        case "maturityDate":
            value = new Date(value);
            elements.maturityDateDayInput.val(value.getDate());
            elements.maturityDateMonthInput.val(value.getMonth()+1);
            elements.maturityDateYearInput.val(value.getFullYear());
            break;
        case "notionalCurrency":
            elements.underlyingCurrencyInput.val(value).tigger("change");
            break;
        case "notionalPrice":
            elements.notionalPriceInput.val(value).trigger("change");
            break;
        case "product":
            elements.productInput.val(productIDToName(value)).trigger("change");
            break;
        case "quantity":
            elements.quantityInput.val(value).trigger("change");
            break;
        case "sellingParty":
            elements.sellingPartyInput.val(companyIDToName(value)).trigger("change");
            break;
        case "strikePrice":
            elements.strikePriceInput.val(value).trigger("change");
            break;
        case "underlyingCurrency":
            elements.underlyingCurrencyInput.val(value).trigger("change");
            break;
        case "underlyingPrice":
            elements.underlyingPriceInput.val(value).trigger("change");
            break;
    }
    removeSuggestion(field);
}

function addSuggestion(field, currentValue, suggestedValue) {
    suggestions[field] = suggestedValue;
    $(`#suggestions`).append(`
    <tr id="${field}-suggestion">
        <td>${NAMES[field]}</td>
        <td>${currentValue} -> ${suggestedValue}</td>
        <td>
            <button id="${field}-accept" type="button" class="btn btn-sm btn-outline-dark">
                <i style="font-size:26px;" class="material-icons text-success mr-1">done</i>
            </button>
        </td>
        <td>
        <button id="${field}-ignore" type="button" class="btn btn-sm btn-outline-dark">
            <i style="font-size:26px;" class="material-icons text-fail mr-1">close</i>
        </button>
        </td>
    </tr>`);
    $(`#suggestions #${field}-accept`).click(() => acceptSuggestion(field));
    $(`#suggestions #${field}-ignore`).click(() => removeSuggestion(field));
}

function removeSuggestion(field) {
    delete suggestions[field];
    $(`#suggestions #${field}-suggestion`).remove();

    if (allSuggestionsResolved()) {
        $("#saveTradeButton").text("Save Trade");
    }
}
