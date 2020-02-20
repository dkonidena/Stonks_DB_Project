let newTradeCount = 0;

function addTradeToUI(trade) {
    let s = "<button class=\"btn trade-button d-block text-muted py-0 my-n1\"></button>";
    let b = $(s).text("Trade "+trade.tradeId).data("trade", trade);
    b.on("click", () => {
        loadTradeToForm(trade);
        showTradeForm();
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

function showTradeForm() {
    if(!$("#tradeEditorForm:visible").length) {
        $("#tradeEditorMessage").hide();
        $("#tradeEditorForm").show();
    }
}

function loadTradeToForm(trade) {
    if (trade === null) {
        showError("Tried to load null trade to form");
        return;
    }
    const fields = [
        ["#tradeIdInput", trade.tradeId],
        ["#productInput", nullMemberAccess(trade.product, "name")],
        ["#buyingPartyInput", nullMemberAccess(trade.buyingParty, "name")],
        ["#sellingPartyInput", nullMemberAccess(trade.sellingParty, "name")],
        ["#tradeDateDayInput", trade.tradeDate.getDate()],
        ["#tradeDateMonthInput", trade.tradeDate.getMonth()+1],
        ["#tradeDateYearInput", trade.tradeDate.getFullYear()],
        ["#maturityDateDayInput", trade.maturityDate.getDate()],
        ["#maturityDateMonthInput", trade.maturityDate.getMonth()+1],
        ["#maturityDateYearInput", trade.maturityDate.getFullYear()],
        ["#notionalCurrency", nullMemberAccess(trade.notionalCurrency, "code")],
        ["#notionalPriceInput", trade.notionalPrice],
        ["#underlyingCurrencyInput", nullMemberAccess(trade.underlyingCurrency, "code")],
        ["#underlyingPriceInput", trade.underlyingPrice],
        ["#quantityInput", trade.quantity],
        ["#strikePriceInput", trade.strikePrice],
    ]

    fields.forEach((x) => {
        try {
            $(x[0]).val(x[1]).trigger("change");
        }
        catch {
            $(x[0]).val(null).trigger("change");
        }

    });
}

function companyNameToObject(name) {
    return Object.values(companies).filter(x => x.name === name)[0];
}

function productNameToObject(name) {
    return Object.values(products).filter(x => x.name === name)[0];
}

function tradeObjectFromForm() {
    // TODO whole function needs error handling
    let trade = new Trade();

    trade.tradeId = $("#tradeIdInput").val();

    trade.product = productNameToObject($("#productInput").val());
    trade.buyingParty = companyNameToObject($("#buyingPartyInput").val());
    trade.sellingParty = companyNameToObject($("#sellingPartyInput").val());

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

    // this gets the labels from a select2 input box's return object
    const labelExtractor = x => x.text

    let tradeID = $("#filter-tradeIDInput").val();
    if (tradeID !== "") { filter.tradeID = [tradeID]; }

    let buyingParty = $("#filter-buyerInput").select2('data');
    if (buyingParty.length > 0) {
        filter.buyingParty = buyingParty.map((entry) => { return companyNameToObject(entry.text).id });
    }

    let sellingParty = $("#filter-sellerInput").select2('data');
    if (sellingParty.length > 0) {
        filter.sellingParty = sellingParty.map((entry) => { return companyNameToObject(entry.text).id });
    }

    let product = $("#filter-productInput").select2('data');
    if (product.length > 0) {
        filter.product = product.map((entry) => { return productNameToObject(entry.text).id });
    }

    // these inputs should already contain currency codes so this bit should work
    let notionalCurrency = $("#filter-notionalCurrencyInput").select2('data');
    if (notionalCurrency.length > 0) { filter.notionalCurrency = notionalCurrency.map(labelExtractor); }

    let underlyingCurrency = $("#filter-underlyingCurrencyInput").select2('data');
    if (underlyingCurrency.length > 0) { filter.underlyingCurrency = underlyingCurrency.map(labelExtractor); }

    let userIDCreatedBy = $("#filter-userIDInput").val();
    if (userIDCreatedBy !== "") { filter.userIDCreatedBy = [userIDCreatedBy]; }

    return filter;
}

function checkTradeButton_OnPressed() {
    api.post.check_trade(tradeObjectFromForm().getAPIObject(), console.log, showError);
    //TODO add visual feedback of the checks
}

function addTradeButton_OnPressed() {
    let t = new Trade();
    t.tradeId = `NEW${newTradeCount++}`;
    addTradeToUI(t);
    loadTradeToForm(t);
    showTradeForm();
}

function saveTradeButton_OnPressed() {
    let t = tradeObjectFromForm();
    if (t.tradeId != undefined) {
        api.patch.trades(t.tradeId, t.getAPIObject(), console.log, showError);
    }
    else {
        api.post.trades(t.getAPIObject(), () => {}, showError);
    }
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
