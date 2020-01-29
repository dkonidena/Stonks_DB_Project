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

function showError(error, detail) {
    $('#errorShort').text(error.message);
    $('#errorDetailContent').text(JSON.stringify(detail, null, 2));
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


var tg = tradeGenerator(true);
function addTradeButton_OnPressed() {
    var t = tg.next().value;
    addTradeToUI(t);
    trades.push(t);
}

function saveTradeButton_OnPressed() {
    var trade = trades.filter(t => t.tradeId == $("#tradeIdInput").val())[0];
    trade.lastModifiedDate = new Date();

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

    api.post.trades(trade.getAPIObject(), console.log, showError)

    //TODO add visual feedback of the save to user
}

function cancelTradeButton_OnPressed() {
    var trade = trades.filter(t => t.tradeId == $("#tradeIdInput").val())[0];
    loadTradeToForm(trade);
}
