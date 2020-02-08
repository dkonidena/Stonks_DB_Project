function addTradeToUI(trade) {
    let s = "<button class=\"btn trade-button d-block text-muted py-0 my-n1\"></button>";
    let b = $(s).text("Trade "+trade.tradeId).data("trade", trade);
    b.on("click", () => {
        loadTradeToForm(trade);
    })
    let li = $("<li class=\"nav-item\"></li>").html(b);
    $("#trades").append(li);
};

function addCurrencyToUI(cur) {
    let o = "<option></option>";
    let c = $(o).text(cur.code).attr({
        "data-symbol": cur.symbol,
        "data-placeholder": cur.allowDecimal ? "0.00" : "0"
    });
    $("#notionalCurrencyInput, #underlyingCurrencyInput").append(c);
};

function addProductToUI(p) {
    let o = "<option></option>";
    let c = $(o).text(p.name);
    $("#productInput").append(c);
}

function addCompanyToUI(c) {
    let o = "<option></option>";
    let d = $(o).text(c.name);
    $("#buyingPartyInput, #sellingPartyInput").append(d);
}

function showRequestError(error, debugData) {
    showError(error.message, "Request:\n" + JSON.stringify(debugData, null, 2));
}

function showError(error = '', detail = '') {
    $('#errorShort').text(error);
    $('#errorDetailContent').text(detail);
    $('#apiErrorModal').modal('show');
}

function loadTradeToForm(trade) {
    $("#tradeIdInput").val(trade.tradeId);

    $("#productInput").val(trade.product).trigger("change");
    $("#buyingPartyInput").val(trade.buyingParty).trigger("change");
    $("#sellingPartyInput").val(trade.sellingParty).trigger("change");

    $("#tradeDateDayInput").val(trade.tradeDate.getDate());
    $("#tradeDateMonthInput").val(trade.tradeDate.getMonth()+1);
    $("#tradeDateYearInput").val(trade.tradeDate.getFullYear());

    $("#maturityDateDayInput").val(trade.maturityDate.getDate());
    $("#maturityDateMonthInput").val(trade.maturityDate.getMonth()+1);
    $("#maturityDateYearInput").val(trade.maturityDate.getFullYear());

    $("#notionalCurrencyInput").val(trade.notionalCurrency).trigger("change");
    $("#notionalPriceInput").val(trade.notionalPrice);
    $("#underlyingCurrencyInput").val(trade.underlyingCurrency).trigger("change");
    $("#underlyingPriceInput").val(trade.underlyingPrice);


    $("#quantityInput").val(trade.quantity);
    $("#strikePriceInput").val(trade.strikePrice);
}

function tradeObjectFromForm() {
    // TODO whole function needs error handling
    let trade = new Trade();

    // TODO these 3 members need to be populated with IDs not names
    trade.product = $("#productInput").val();
    trade.buyingParty = $("#buyingPartyInput").val();
    trade.sellingParty = $("#sellingPartyInput").val();

    trade.tradeDate.setDate($("#tradeDateDayInput").val());
    trade.tradeDate.setMonth($("#tradeDateMonthInput").val()-1);
    trade.tradeDate.setFullYear($("#tradeDateYearInput").val());

    trade.maturityDate.setDate($("#maturityDateDayInput").val());
    trade.maturityDate.setMonth($("#maturityDateMonthInput").val()-1);
    trade.maturityDate.setFullYear($("#maturityDateYearInput").val());

    trade.notionalCurrency = $("#notionalCurrencyInput").val();
    trade.notionalPrice = $("#notionalPriceInput").val();
    trade.underlyingCurrency = $("#underlyingCurrencyInput").val();
    trade.underlyingPrice = $("#underlyingPriceInput").val();

    trade.quantity = $("#quantityInput").val();
    trade.strikePrice = $("#strikePriceInput").val();

    return trade;
}

function filterObjectFromForm() {
    // TODO whole function needs error handling
    let filter = new TradeFilter();

    if ($("#advancedSearch #creationDateLowerDayInput").val() !== "") {
        filter.dateCreated = [new Date(), new Date()];
        filter.dateCreated[0].setHours(0,0,0,0);
        filter.dateCreated[0].setDate($("#advancedSearch #creationDateLowerDayInput").val());
        filter.dateCreated[0].setMonth($("#advancedSearch #creationDateLowerMonthInput").val()-1);
        filter.dateCreated[0].setFullYear($("#advancedSearch #creationDateLowerYearInput").val());
        filter.dateCreated[1].setHours(0,0,0,0);
        filter.dateCreated[1].setDate($("#advancedSearch #creationDateUpperDayInput").val());
        filter.dateCreated[1].setMonth($("#advancedSearch #creationDateUpperMonthInput").val()-1);
        filter.dateCreated[1].setFullYear($("#advancedSearch #creationDateUpperYearInput").val());
        filter.dateCreated[0] = filter.dateCreated[0].toISOString();
        filter.dateCreated[1] = filter.dateCreated[1].toISOString();
    }

    if ($("#advancedSearch #modificationDateLowerDayInput").val() !== "") {
        filter.dateModified = [new Date(), new Date()];
        filter.dateModified[0].setHours(0,0,0,0);
        filter.dateModified[0].setDate($("#advancedSearch #modificationLowerDayInput").val());
        filter.dateModified[0].setMonth($("#advancedSearch #modificationDateLowerMonthInput").val()-1);
        filter.dateModified[0].setFullYear($("#advancedSearch #modificationDateLowerYearInput").val());
        filter.dateModified[1].setHours(0,0,0,0);
        filter.dateModified[1].setDate($("#advancedSearch #modificationDateUpperDayInput").val());
        filter.dateModified[1].setMonth($("#advancedSearch #modificationDateUpperMonthInput").val()-1);
        filter.dateModified[1].setFullYear($("#advancedSearch #modificationDateUpperYearInput").val());
        filter.dateModified[0] = filter.dateModified[0].toISOString();
        filter.dateModified[1] = filter.dateModified[1].toISOString();
    }

    // TODO these 4 members need to be populated with IDs not names
    let tradeID = $("#advancedSearch #tradeIDInput").val();
    if (tradeID !== "") { filter.tradeID = tradeID; }

    let buyingParty = $("#advancedSearch #buyerInput").val();
    if (buyingParty !== "") { filter.buyingParty = buyingParty; }

    let sellingParty = $("#advancedSearch #sellerInput").val();
    if (sellingParty !== "") { filter.sellingParty = sellingParty; }

    let product = $("#advancedSearch #productInput").val();
    if (product !== "") { filter.product = product; }

    let notionalCurrency = $("#advancedSearch #notionalCurrencyInput").val();
    if (notionalCurrency !== "") { filter.notionalCurrency = notionalCurrency; }

    let underlyingCurrencyInput = $("#advancedSearch #underlyingCurrencyInput").val();
    if (underlyingCurrencyInput !== "") { filter.underlyingCurrencyInput = underlyingCurrencyInput; }

    let userIDCreatedBy = $("#advancedSearch #userIDInput").val();
    if (userIDCreatedBy !== "") { filter.userIDCreatedBy = userIDCreatedBy; }

    return filter;
}

function checkTradeButton_OnPressed() {
    api.post.check_trade(tradeObjectFromForm().getAPIObject(), console.log, showRequestError);
    //TODO add visual feedback of the checks
}

function addTradeButton_OnPressed() {
    showError('not implemented');
    // TODO
}

function saveTradeButton_OnPressed() {
    api.post.trades(tradeObjectFromForm().getAPIObject(), console.log, showRequestError);
    //TODO add visual feedback of the save to user
}

function cancelTradeButton_OnPressed() {
    var trade = trades.filter(t => t.tradeId == $("#tradeIdInput").val())[0];
    loadTradeToForm(trade);
}

function advancedSearchButton_OnPressed() {
    let filter = filterObjectFromForm();
    getTradeList(filter, (trades) => {
        trades.forEach(addTradeToUI);
    });
}
