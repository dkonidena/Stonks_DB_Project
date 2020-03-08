//search for elements needed only once to improve performance
const elements = {
    trades: $("#trades"),
    tradeId: $("#tradeId"),
    tradeDate: $("#tradeDate"),
    productInput: $("#productInput"),
    buyingPartyInput: $("#buyingPartyInput"),
    sellingPartyInput: $("#sellingPartyInput"),
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
    filterCreationDateUpperDayInput: $("#filter-creationDateUpperDayInput")
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
    $("#buyingPartyInput, #filter-buyerInput, #filter-sellerInput").append(d);
}

function populateSellerSelection() {
    let product = productNameToObject(elements.productInput.val());
    if (product) {
        $("#sellingPartyInput").empty();
        let o = "<option></option>";
        let d = $(o).text(product.company.name);
        $("#sellingPartyInput").append(d);
    }
}

function showTradeForm() {
    $("#startButtons").hide();
    $("#tradeEditorForm").show();
}

function loadTradeToForm(trade) {
    showTradeForm();

    if (trade === null) {
        showError("Tried to load null trade to form");
        return;
    }
    const fields = [
        [elements.productInput, nullMemberAccess(trade.product, "name")],
        [elements.buyingPartyInput, nullMemberAccess(trade.buyingParty, "name")],
        [elements.sellingPartyInput, nullMemberAccess(trade.sellingParty, "name")],
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

    elements.tradeId.text(trade.tradeId);
    elements.tradeDate.text(trade.tradeDate.toISOString().substring(0,10));
    checkTradeValidity();
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

    trade.tradeId = elements.tradeId.text();

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
    $("#checkTradeButton").prop('disabled', !isValidTrade());
    $("#saveTradeButton").prop('disabled', !isValidTrade());

    if ($("#tradeId").text() === "") {
        $("#deleteObject").hide();
    } else {
        $("#deleteObject").show();
    }
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
            api.patch.trades(t.tradeId, t.getAPIObject(), () => {
                showSuccess('Trade updated.');
                resetState();
            }, showError);
        }
        else {
            api.post.trades(t.getAPIObject(), () => {
                showSuccess('Trade saved.');
                resetState();
            }, showError);
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

    let userIDcreatedBy = $("#filter-userIDInput").select2('data');
    if (userIDcreatedBy.length > 0) {
        filter.userIDcreatedBy = userIDcreatedBy.map((entry) => { return userNameToObject(entry.text).id });
    }

    return filter;
}

function resetState() {
    $("#tradeEditorForm").hide();
    $("#saveTradeButton").hide();
    $("#suggestionsTable").hide();
    $("#startButtons").show();
}

function renderTable(csv) {
    const blob = new Blob([csv], { type: "text/plain" });
    CsvToHtmlTable.init({
        csv_path: URL.createObjectURL(blob),
        element: "table-container",
        allow_download: false,
        csv_options: {"separator": ",", "delimiter": "\""},
        datatables_options: {
            "scrollY": "60vh",
            "paging": true,
            "scrollX": true,
            "columnDefs": [
                {
                    "targets": 0,
                    "render": ( data, type, row, meta ) =>  {
                        return `<a id="trade-${data}" href="#" data-dismiss="modal">${data}</a>`
                    }
                }
            ]
        },
        onComplete: () => {
            $("#table-container tbody").on("click", "a", function () {
                let id = this.id.substring(6);
                loadTradeToForm(trades[id]);
                showTradeForm();
            });
            $("#resultsStatus").hide();
        }
    });
}

function tradesToCSV(trades) {
    let csv = "Trade ID,Date Of Trade,Product,Buying Party,Selling Party,Notional Value,Notional Currency,Quantity,Maturity Date,Underlying Value,Underlying Currency,Strike Price\n"
    for (const trade of trades) {
        let fields = [
            trade.tradeId,
            trade.tradeDate.toISOString().substring(0,10),
            trade.product.name,
            trade.buyingParty.name,
            trade.sellingParty.name,
            trade.notionalPrice,
            trade.notionalCurrency.code,
            trade.quantity,
            trade.maturityDate.toISOString().substring(0,10),
            trade.underlyingPrice,
            trade.underlyingCurrency.code,
            trade.strikePrice
        ];


        for (let i = 0; i < fields.length; i++) {
            let field = fields[i];
            if (i === fields.length - 1) {
                csv += `${field}\n`;
            } else {
                csv += `${field},`;
            }
        }
    }

    return csv;
}
