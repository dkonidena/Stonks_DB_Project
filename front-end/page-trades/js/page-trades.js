function addTradeToUI(trade) {
    let s = "<button class=\"btn trade-button d-block text-muted py-0 my-n1\"></button>";
    let b = $(s).text("Trade "+trade.tradeId).data("trade", trade);
    b.on("click", () => {
        loadTradeToForm(trade);
    })
    let li = $("<li class=\"nav-item\"></li>").html(b);
    $("#trades").append(li);

    let o = "<option></option>";
    let t = $(o).text(trade.tradeId);
    $("#filter-tradeIdInput").append(t);
};

function addCurrencyToUI(cur) {
    let o = "<option></option>";
    let c = $(o).text(cur.code).attr({
        "data-symbol": cur.symbol,
        "data-placeholder": cur.allowDecimal ? "0.00" : "0"
    });
    $("#notionalCurrencyInput, #underlyingCurrencyInput, #filter-notionalCurrencyInput, #filter-underlyingCurrencyInput").append(c);
};

function addProductToUI(p) {
    let o = "<option></option>";
    let c = $(o).text(p.name);
    $("#productInput, #filter-productInput").append(c);
}

function addCompanyToUI(c) {
    let o = "<option></option>";
    let d = $(o).text(c.name);
    $("#buyingPartyInput, #sellingPartyInput, #filter-buyerInput, #filter-sellerInput").append(d);
}

function loadTradeToForm(trade) {
    $("#tradeIdInput").val(trade.tradeId);

    let elem = $("#productInput");
    elem.val(trade.product.name).trigger("change");
    if (!elem.select2("data").length) {
        showError("Could not find product for trade", trade);
    }
    $("#buyingPartyInput").val(trade.buyingParty.name).trigger("change");
    $("#sellingPartyInput").val(trade.sellingParty.name).trigger("change");

    $("#tradeDateDayInput").val(trade.tradeDate.getDate());
    $("#tradeDateMonthInput").val(trade.tradeDate.getMonth()+1);
    $("#tradeDateYearInput").val(trade.tradeDate.getFullYear());

    $("#maturityDateDayInput").val(trade.maturityDate.getDate());
    $("#maturityDateMonthInput").val(trade.maturityDate.getMonth()+1);
    $("#maturityDateYearInput").val(trade.maturityDate.getFullYear());

    $("#notionalCurrencyInput").val(trade.notionalCurrency.code).trigger("change");
    $("#notionalPriceInput").val(trade.notionalPrice);
    $("#underlyingCurrencyInput").val(trade.underlyingCurrency.code).trigger("change");
    $("#underlyingPriceInput").val(trade.underlyingPrice);


    $("#quantityInput").val(trade.quantity);
    $("#strikePriceInput").val(trade.strikePrice);
}

function tradeObjectFromForm() {
    // TODO whole function needs error handling
    let trade = new Trade();

    trade.product = Object.values(products).filter(x => x.name === $("#productInput").val())[0];
    trade.buyingParty = Object.values(companies).filter(x => x.name === $("#buyingPartyInput").val())[0];;
    trade.sellingParty = Object.values(companies).filter(x => x.name === $("#sellingPartyInput").val())[0];;

    trade.tradeDate.setDate($("#tradeDateDayInput").val());
    trade.tradeDate.setMonth($("#tradeDateMonthInput").val()-1);
    trade.tradeDate.setFullYear($("#tradeDateYearInput").val());

    trade.maturityDate.setDate($("#maturityDateDayInput").val());
    trade.maturityDate.setMonth($("#maturityDateMonthInput").val()-1);
    trade.maturityDate.setFullYear($("#maturityDateYearInput").val());

    trade.notionalCurrency = currencies[$("#notionalCurrencyInput").val()];
    trade.notionalPrice = $("#notionalPriceInput").val();
    trade.underlyingCurrency = currencies[$("#underlyingCurrencyInput").val()];
    trade.underlyingPrice = $("#underlyingPriceInput").val();

    trade.quantity = $("#quantityInput").val();
    trade.strikePrice = $("#strikePriceInput").val();

    return trade;
}

function filterObjectFromForm() {
    // TODO whole function needs error handling
    let filter = new TradeFilter();

    if ($("#filter-creationDateLowerYearInput").val() !== "") {
        if (!filter.dateCreated) { filter.dateCreated = {}; }
        filter.dateCreated['after'] =  new Date();
        filter.dateCreated.after.setHours(0,0,0,0);
        filter.dateCreated.after.setDate($("#filter-creationDateLowerDayInput").val());
        filter.dateCreated.after.setMonth($("#filter-creationDateLowerMonthInput").val()-1);
        filter.dateCreated.after.setFullYear($("#filter-creationDateLowerYearInput").val());
        filter.dateCreated.after = filter.dateCreated.after.toISOString();
    }

    if ($("#filter-creationDateUpperYearInput").val() !== "") {
        if (!filter.dateCreated) { filter.dateCreated = {}; }
        filter.dateCreated['before'] =  new Date();
        filter.dateCreated.before.setHours(0,0,0,0);
        filter.dateCreated.before.setDate($("#filter-creationDateUpperDayInput").val());
        filter.dateCreated.before.setMonth($("#filter-creationDateUpperMonthInput").val()-1);
        filter.dateCreated.before.setFullYear($("#filter-creationDateUpperYearInput").val());
        filter.dateCreated.before = filter.dateCreated.before.toISOString();
    }

    if ($("#filter-modificationDateLowerYearInput").val() !== "") {
        if (!filter.dateModified) { filter.dateModified = {}; }
        filter.dateModified['after'] =  new Date();
        filter.dateModified.after.setHours(0,0,0,0);
        filter.dateModified.after.setDate($("#filter-modificationDateLowerDayInput").val());
        filter.dateModified.after.setMonth($("#filter-modificationDateLowerMonthInput").val()-1);
        filter.dateModified.after.setFullYear($("#filter-modificationDateLowerYearInput").val());
        filter.dateModified.after = filter.dateModified.after.toISOString();
    }

    if ($("#filter-modificationDateUpperYearInput").val() !== "") {
        if (!filter.dateModified) { filter.dateModified = {}; }
        filter.dateModified['before'] =  new Date();
        filter.dateModified.before.setHours(0,0,0,0);
        filter.dateModified.before.setDate($("#filter-modificationDateUpperDayInput").val());
        filter.dateModified.before.setMonth($("#filter-modificationDateUpperMonthInput").val()-1);
        filter.dateModified.before.setFullYear($("#filter-modificationDateUpperYearInput").val());
        filter.dateModified.before = filter.dateModified.before.toISOString();
    }

    // TODO these 4 members need to be populated with IDs not names
    let tradeID = $("#filter-tradeIDInput").val();
    if (tradeID !== "") { filter.tradeID = tradeID; }

    // this gets the labels from a select2 input box's return object
    const labelExtractor = x => x.text

    let buyingParty = $("#filter-buyerInput").select2('data');
    if (buyingParty.length > 0) { filter.buyingParty = buyingParty.map(labelExtractor); }

    let sellingParty = $("#filter-sellerInput").select2('data');
    if (sellingParty.length > 0) { filter.sellingParty = sellingParty.map(labelExtractor); }

    let product = $("#filter-productInput").select2('data');
    if (product.length > 0) { filter.product = product.map(labelExtractor); }

    // these inputs should already contain currency codes so this bit should work
    let notionalCurrency = $("#filter-notionalCurrencyInput").select2('data');
    if (notionalCurrency.length > 0) { filter.notionalCurrency = notionalCurrency.map(labelExtractor); }

    let underlyingCurrency = $("#filter-underlyingCurrencyInput").select2('data');
    if (underlyingCurrency.length > 0) { filter.underlyingCurrency = underlyingCurrency.map(labelExtractor); }

    // TODO do we need to get a list of userIDs? currently is is impossible to enter anything into this input
    let userIDCreatedBy = $("#filter-userIDInput").select2('data');
    if (userIDCreatedBy.length > 0) { filter.userIDCreatedBy = userIDCreatedBy; }

    return filter;
}

function checkTradeButton_OnPressed() {
    api.post.check_trade(tradeObjectFromForm().getAPIObject(), console.log, showError);
    //TODO add visual feedback of the checks
}

function addTradeButton_OnPressed() {
    showError('NotImplementedError');
    // TODO
}

function saveTradeButton_OnPressed() {
    api.post.trades(tradeObjectFromForm().getAPIObject(), console.log, showError);
    //TODO add visual feedback of the save to user
}

function cancelTradeButton_OnPressed() {
    var trade = Object.values(trades).filter(t => t.tradeId == $("#tradeIdInput").val())[0];
    loadTradeToForm(trade);
}

function advancedSearchButton_OnPressed() {
    let filter = filterObjectFromForm();
    getTradeList(filter, (trades) => {
        trades.forEach(addTradeToUI);
    });
}
