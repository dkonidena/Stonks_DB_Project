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
    filterTradeIdInput: $("#filter-tradeIDInput"),
    filterModificationDateLowerYearInput: $("#filter-modificationDateLowerYearInput"),
    filterModificationDateUpperYearInput: $("#filter-modificationDateUpperYearInput"),
    filterModificationDateLowerMonthInput: $("#filter-modificationDateLowerMonthInput"),
    filterModificationDateUpperMonthInput: $("#filter-modificationDateUpperMonthInput"),
    filterModificationDateLowerDayInput: $("#filter-modificationDateLowerDayInput"),
    filterModificationDateUpperDayInput: $("#filter-modificationDateUpperDayInput"),
    filterCreationDateLowerYearInput: $("#filter-creationDateLowerYearInput"),
    filterCreationDateUpperYearInput: $("#filter-creationDateUpperYearInput"),
    filterCreationDateLowerMonthInput: $("#filter-creationDateLowerMonthInput"),
    filterCreationDateUpperMonthInput: $("#filter-creationDateUpperMonthInput"),
    filterCreationDateLowerDayInput: $("#filter-creationDateLowerDayInput"),
    filterCreationDateUpperDayInput: $("#filter-creationDateUpperDayInput"),
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
    return elements.trades.html().isBlank();
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

function addUserToUI(p) {
    let o = "<option></option>";
    let c = $(o).text(p.name);
    $("#filter-userIDInput").append(c);
}

function addCompanyToUI(c) {
    let o = "<option></option>";
    let d = $(o).text(c.name);
    $("#buyingPartyInput, #sellingPartyInput, #filter-buyerInput, #filter-sellerInput").append(d);
}

function showTradeForm() {
    $("#startButtons").hide();
    $("#tradeEditorForm").show();
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

function companyIDToName(id) {
    return Object.values(companies).filter(x => x.id === id)[0].name;
}

function productIDToName(id) {
    return Object.values(products).filter(x => x.id === id)[0].name;
}

function productNameToObject(name) {
    return Object.values(products).filter(x => x.name === name)[0];
}

function userNameToObject(name) {
    return Object.values(users).filter(x => x.name === name)[0];
}

function tradeObjectFromForm() {
    // TODO whole function needs error handling
    let trade = new Trade();

    trade.tradeId = elements.tradeIdInput.val();

    trade.product = productNameToObject(elements.productInput.val());
    trade.buyingParty = companyNameToObject(elements.buyingPartyInput.val());
    trade.sellingParty = companyNameToObject(elements.sellingPartyInput.val());

    if (elements.maturityDateDayInput.val() === "" || elements.maturityDateMonthInput.val() === "" | elements.maturityDateYearInput.val() === "") {
        throw new SyntaxError;
    }

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

function checkTradeValidity() {
    $("#saveTradeButton").prop('disabled', !isValidTrade());
}

function isValidTrade() {
    let obj;
    try {
        obj = tradeObjectFromForm().getAPIObject()
    } catch (e) {
        return false;
    }

    for (const value of Object.values(obj)) {
        if (value === "") {
            return false;
        }
    }

    return true;
}

function saveTrade() {
    if (isValidTrade()) {
        let t = tradeObjectFromForm();
        if (t.tradeId !== "") {
            api.patch.trades(t.tradeId, t.getAPIObject(), () => showSuccess('Trade updated.'), showError);
        }
        else {
            api.post.trades(t.getAPIObject(), () => showSuccess('Trade saved.'), showError);
        }
    }
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

    let userIDCreatedBy = $("#filter-userIDInput").select2('data');
    if (userIDCreatedBy.length > 0) {
        filter.userIDCreatedBy = userIDCreatedBy.map((entry) => { return userNameToObject(entry.text).id });
    }

    return filter;
}

function showResults() {
    $("#resultsModal").modal("show");
    renderTable(`Date Of Trade,Trade ID,Product,Buying Party,Selling Party,Notional Value,Notional Currency,Quantity,Maturity Date,Underlying Value,Underlying Currency,Strike Price
2019-12-01,PRAHGHUD44334854,74,DDIB11,UFAY59,287749.0,USD,700,2024-07-13,411.07,USD,408.02
2019-12-01,UWRDSKTF42789997,43,RJUD59,YWMD69,6300.0,USD,100,2023-05-24,63.0,USD,72.02
2019-12-01,CGKFXLKD21336618,84,IZLM67,SXHU74,48735.0,USD,500,2021-09-10,97.47,USD,85.74
2019-12-01,VYZDXMDK00087572,69,WIZJ73,QLCE04,837900.0,USD,6000,2021-01-31,139.65,USD,134.81
2019-12-01,TFOLQEZN94334607,59,SXTM39,TFLS35,243430.0,USD,1000,2023-07-02,243.43,USD,221.49
2019-12-01,LLCVFARQ49216174,79,GGLV00,GBEZ65,142120.0,USD,2000,2023-09-18,71.06,USD,77.63
2019-12-01,JMQFWWIA92526877,89,RJUD59,HPTP65,803000.0,USD,20000,2021-04-12,40.15,USD,41.92
2019-12-01,TBDAUGJG58817614,5,NGBA40,DVVB31,418260.0,USD,2000,2023-09-12,209.13,USD,249.73
2019-12-01,GZALOIUG74439111,38,FORM54,HWHS51,7166.0,USD,100,2023-03-07,71.66,USD,66.69
2019-12-01,UUAFJXRX98147604,14,JVHD93,EIWJ22,178116.0,USD,600,2023-10-10,296.86,USD,236.75
2019-12-01,FANTXEWA98082344,85,QWOA67,DOGG07,80991900.0,USD,90000,2023-08-04,899.91,USD,802.44
2019-12-01,WUYJVCNE52292075,87,LIIS96,DOGG07,7441.0,USD,100,2020-12-20,74.41,USD,67.21
2019-12-01,TJDJETLI33632148,80,CAVR54,GBEZ65,1418400.0,USD,40000,2024-04-03,35.46,USD,29.58`)
}

function renderTable(csv) {
    $("#resultsStatus").show();
    const blob = new Blob([csv], { type: "text/plain" });

    CsvToHtmlTable.init({
        csv_path: URL.createObjectURL(blob),
        element: "table-container",
        allow_download: false,
        csv_options: {separator: ",", delimiter: "\""},
        datatables_options: {
            "paging": true,
            "scrollX": true
        },
        onComplete: () => { $("#resultsStatus").hide() }
    });
}
