let newTradeCount = 0;
//search for elements needed only once to improve performance
const elements = {
    trades: $("#trades"),
    tradeList: $("#tradeList"),
    tradeListCollapseSymbol: $("#tradeListCollapseSymbol"),
    tradeIdInput: $("#tradeIdInput"),
    productInput: $("#productInput"),
    buyingPartyInput: $("#buyingPartyInput"),
    sellingPartyInput: $("#sellingPartyInput"),
    tradeDateDayInput: $("#tradeDateDayInput"),
    tradeDateMonthInput: $("#tradeDateMonthInput"),
    tradeDateYearInput: $("#tradeDateYearInput"),
    maturityDateDayInput: $("#maturityDateDayInput"),
    maturityDateMonthInput: $("#maturityDateMonthInput"),
    maturityDateYearInput: $("#maturityDateYearInput"),
    notionalCurrencyInput: $("#notionalCurrencyInput"),
    notionalPriceInput: $("#notionalPriceInput"),
    underlyingCurrencyInput: $("#underlyingCurrencyInput"),
    underlyingPriceInput: $("#underlyingPriceInput"),
    quantityInput: $("#quantityInput"),
    strikePriceInput: $("#strikePriceInput"),
    filterTradeIdInput: $("#filter-tradeIdInput"),
    filterModificationDateLowerYearInput: $("#filter-modificationDateLowerYearInput"),
    filterModificationDateUpperYearInput: $("#filter-modificationDateUpperYearInput"),
    filterModificationDateLowerMonthInput: $("#filter-modificationDateLowerMonthInput"),
    filterModificationDateUpperMonthInput: $("#filter-modificationDateUpperMonthInput"),
    filterModificationDateLowerDayInput: $("#filter-modificationDateLowerDayInput"),
    filterModificationDateUpperDayInput: $("#filter-modificationDateUpperDayInput"),
    filterCreationDateLowerYearInput: $("#filter-CreationDateLowerYearInput"),
    filterCreationDateUpperYearInput: $("#filter-CreationDateUpperYearInput"),
    filterCreationDateLowerMOnthInput: $("#filter-CreationDateLowerMOnthInput"),
    filterCreationDateUpperMOnthInput: $("#filter-CreationDateUpperMOnthInput"),
    filterCreationDateLowerDayInput: $("#filter-CreationDateLowerDayInput"),
    filterCreationDateUpperDayInput: $("#filter-CreationDateUpperDayInput"),
    tradeListEmptyMessage: $("#tradeListEmptyMessage"),
}

function addTradeToUI(trade) {
    let s = "<button class=\"btn trade-button d-block text-muted py-0 my-n1\"></button>";
    let b = $(s).text("Trade "+trade.tradeId).data("trade", trade);
    b.on("click", () => {
        loadTradeToForm(trade);
        showTradeForm();
    })
    let li = $("<li class=\"nav-item\"></li>").html(b);
    elements.trades.append(li);

    let o = "<option></option>";
    let t = $(o).text(trade.tradeId);
    elements.filterTradeIdInput.append(t);
};

function clearTradeList() {
    elements.trades.html("");
    elements.filterTradeIdInput.html("");
}

function isTradeListEmpty() {
    return elements.trades.html() === "";
}

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
        [elements.tradeIdInput, trade.tradeId],
        [elements.productInput, nullMemberAccess(trade.product, "name")],
        [elements.buyingPartyInput, nullMemberAccess(trade.buyingParty, "name")],
        [elements.sellingPartyInput, nullMemberAccess(trade.sellingParty, "name")],
        [elements.tradeDateDayInput, trade.tradeDate.getDate()],
        [elements.tradeDateMonthInput, trade.tradeDate.getMonth()+1],
        [elements.tradeDateYearInput, trade.tradeDate.getFullYear()],
        [elements.maturityDateDayInput, trade.maturityDate.getDate()],
        [elements.maturityDateMonthInput, trade.maturityDate.getMonth()+1],
        [elements.maturityDateYearInput, trade.maturityDate.getFullYear()],
        [elements.notionalCurrencyInput, nullMemberAccess(trade.notionalCurrency, "code")],
        [elements.notionalPriceInput, trade.notionalPrice],
        [elements.underlyingCurrencyInput, nullMemberAccess(trade.underlyingCurrency, "code")],
        [elements.underlyingPriceInput, trade.underlyingPrice],
        [elements.quantityInput, trade.quantity],
        [elements.strikePriceInput, trade.strikePrice],
    ]

    fields.forEach((x) => {
        $(x[0]).val(x[1]).trigger("change");
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

    trade.tradeId = elements.tradeIdInput.val();

    trade.product = productNameToObject(elements.productInput.val());
    trade.buyingParty = companyNameToObject(elements.buyingPartyInput.val());
    trade.sellingParty = companyNameToObject(elements.sellingPartyInput.val());

    trade.tradeDate.setDate(elements.tradeDateDayInput.val());
    trade.tradeDate.setMonth(elements.tradeDateMonthInput.val()-1);
    trade.tradeDate.setFullYear(elements.tradeDateYearInput.val());

    trade.maturityDate.setDate(elements.maturityDateDayInput.val());
    trade.maturityDate.setMonth(elements.maturityDateMonthInput.val()-1);
    trade.maturityDate.setFullYear(elements.maturityDateYearInput.val());

    trade.notionalCurrency = currencies[elements.notionalCurrencyInput.val()];
    trade.notionalPrice = elements.notionalPriceInput.val();
    trade.underlyingCurrency = currencies[elements.underlyingCurrencyInput.val()];
    trade.underlyingPrice = elements.underlyingPriceInput.val();

    trade.quantity = elements.quantityInput.val();
    trade.strikePrice = elements.strikePriceInput.val();

    return trade;
}

function filterObjectFromForm() {
    // TODO whole function needs error handling
    let filter = new TradeFilter();

    if (elements.filterCreationDateLowerYearInput.val() !== "") {
        if (!filter.dateCreated) { filter.dateCreated = {}; }
        filter.dateCreated['after'] =  new Date();
        filter.dateCreated.after.setHours(0,0,0,0);
        filter.dateCreated.after.setDate(elements.filterCreationDateLowerDayInput.val());
        filter.dateCreated.after.setMonth(elements.filterCreationDateLowerMonthInput.val()-1);
        filter.dateCreated.after.setFullYear(elements.filterCreationDateLowerYearInput.val());
        filter.dateCreated.after = filter.dateCreated.after.toISOString();
    }

    if (elements.filterCreationDateUpperYearInput.val() !== "") {
        if (!filter.dateCreated) { filter.dateCreated = {}; }
        filter.dateCreated['before'] =  new Date();
        filter.dateCreated.before.setHours(0,0,0,0);
        filter.dateCreated.before.setDate(elements.filterCreationDateUpperDayInput.val());
        filter.dateCreated.before.setMonth(elements.filterCreationDateUpperMonthInput.val()-1);
        filter.dateCreated.before.setFullYear(elements.filterCreationDateUpperYearInput.val());
        filter.dateCreated.before = filter.dateCreated.before.toISOString();
    }

    if (elements.filterModificationDateLowerYearInput.val() !== "") {
        if (!filter.dateModified) { filter.dateModified = {}; }
        filter.dateModified['after'] =  new Date();
        filter.dateModified.after.setHours(0,0,0,0);
        filter.dateModified.after.setDate(elements.filterModificationDateLowerDayInput.val());
        filter.dateModified.after.setMonth(elements.filterModificationDateLowerMonthInput.val()-1);
        filter.dateModified.after.setFullYear(elements.filterModificationDateLowerYearInput.val());
        filter.dateModified.after = filter.dateModified.after.toISOString();
    }

    if (elements.filterModificationDateUpperYearInput.val() !== "") {
        if (!filter.dateModified) { filter.dateModified = {}; }
        filter.dateModified['before'] =  new Date();
        filter.dateModified.before.setHours(0,0,0,0);
        filter.dateModified.before.setDate(elements.filterModificationDateUpperDayInput.val());
        filter.dateModified.before.setMonth(elements.filterModificationDateUpperMonthInput.val()-1);
        filter.dateModified.before.setFullYear(elements.filterModificationDateUpperYearInput.val());
        filter.dateModified.before = filter.dateModified.before.toISOString();
    }

    // this gets the labels from a select2 input box's return object
    const labelExtractor = x => x.text

    let tradeID = elements.filterTradeIdInput.val();
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
