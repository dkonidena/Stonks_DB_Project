var currentTradesNum = 0;
var date;

//search for elements needed only once to improve performance
const elements = {
    trades: $("#trades"),
    tradeId: $("#tradeId"),
    tradeDate: $("#tradeDate"),
    productInput: $("#productInput"),
    buyingPartyInput: $("#buyingPartyInput"),
    sellingPartyInput: $("#sellingPartyInput"),
    maturityDateInput: $("#maturityDateInput"),
    notionalCurrencyInput: $("#notionalCurrencyInput"),
    notionalPriceInput: $("#notionalPriceInput"),
    underlyingCurrencyInput: $("#underlyingCurrencyInput"),
    underlyingPriceInput: $("#underlyingPriceInput"),
    quantityInput: $("#quantityInput"),
    strikePriceInput: $("#strikePriceInput"),
    filterTradeIdInput: $("#filter-tradeIDInput"),
    filterModificationDateLowerInput: $("#filter-modificationDateLowerInput"),
    filterModificationDateUpperInput: $("#filter-modificationDateUpperInput"),
    filterCreationDateLowerInput: $("#filter-creationDateLowerInput"),
    filterCreationDateUpperInput: $("#filter-creationDateUpperInput"),
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

    date = trade.tradeDate;

    let md = elements.maturityDateInput;
    md.datepicker("setDate", trade.maturityDate);
    md.datepicker("setStartDate", trade.tradeDate);
    md.trigger("change");
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

    if (elements.maturityDateInput.datepicker("getDate") === null) {
        throw new SyntaxError;
    }

    trade.maturityDate = elements.maturityDateInput.datepicker("getDate");

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
            if (dateDifference(date, new Date()) > editWindow) {
                $("#tooOldModal").modal("show");
                return;
            }
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

function resetFilter() {
    elements.filterTradeIdInput.val("");
    $("#filter-buyerInput").val("").trigger("change");
    $("#filter-sellerInput").val("").trigger("change");
    $("#filter-productInput").val("").trigger("change");
    $("#filter-notionalCurrencyInput").val("").trigger("change");
    $("#filter-underlyingCurrencyInput").val("").trigger("change");
    $("#filter-userIDInput").val("").trigger("change");

    elements.filterCreationDateLowerInput.val("").datepicker('clearDates');
    elements.filterCreationDateUpperInput.val("").datepicker('clearDates');
    elements.filterModificationDateLowerInput.val("").datepicker('clearDates');
    elements.filterModificationDateUpperInput.val("").datepicker('clearDates');
}

function filterObjectFromForm() {
    // TODO whole function needs error handling
    let filter = new TradeFilter();
    let d;

    d = elements.filterCreationDateLowerInput.datepicker("getDate");
    if (d !== null) {
        if (!filter.dateCreated) { filter.dateCreated = {}; }
        console.log(d);
        filter.dateCreated['after'] = d.toISOString();
    }

    d = elements.filterCreationDateUpperInput.datepicker("getDate");
    if (d !== null) {
        if (!filter.dateCreated) { filter.dateCreated = {}; }
        filter.dateCreated['before'] = d.toISOString();
    }

    d = elements.filterModificationDateLowerInput.datepicker("getDate");
    if (d !== null) {
        if (!filter.dateModified) { filter.dateModified = {}; }
        filter.dateModified['after'] = d.toISOString();
    }

    d = elements.filterModificationDateUpperInput.datepicker("getDate");
    if (d !== null) {
        if (!filter.dateModified) { filter.dateModified = {}; }
        filter.dateModified['before'] = d.toISOString();
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
    let t = new Trade("");
    t.notionalCurrency = currencies.USD;
    t.underlyingCurrency = currencies.USD;
    loadTradeToForm(t);
    elements.tradeDate.text("").trigger("change");
    elements.maturityDateInput.datepicker("clearDates").trigger("change");
    $("#tradeEditorForm").hide();
    $("#saveTradeButton").hide();
    $("#suggestionsTable").hide();
    $("#startButtons").show();
}

//gets the next 1000 trades
function getNextTradeBlock(first) {
    getTradeList(currentFilter, (trades) => {
        if (!trades.length) renderTable("");
        if (first) {
            renderTable(tradesToCSV(trades, true));
        } else {
            let csv = tradesToCSV(trades, false);
            CsvToHtmlTable.add_existing("#table-container", csv, {"separator": ",", "delimiter": "\""});
        }
        currentTradesNum += trades.length;
    }, currentTradesNum);
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
            ],
            "drawCallback": () => {
                //whenever the next button or the button for the last page is pressed, check if the last page button is the active one
                //if so, need to load the next block of trades
                $(".pagination").children().slice(-2).children().on("click", () => {
                    setTimeout(() => {
                        if ($(".pagination").children().slice(-2,-1).hasClass("active")) {
                            getNextTradeBlock(false);
                        }
                    }, 50);
                });
            }
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

function tradesToCSV(trades, header) {
    let csv;
    if (header)
        csv = "Trade ID,Date Of Trade,Product,Buying Party,Selling Party,Notional Value,Notional Currency,Quantity,Maturity Date,Underlying Value,Underlying Currency,Strike Price\n"
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
