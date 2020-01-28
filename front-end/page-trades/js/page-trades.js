function addCurrency(cur) {
    let o = "<option></option>";
    let c = $(o).text(cur.code).attr({
        "data-symbol": cur.symbol,
        "data-placeholder": cur.allowDecimal ? "0.00" : "0"
    });
    $("#notionalCurrencyInput, #underlyingCurrencyInput").append(c);
};

function addProduct(p) {
    let o = "<option></option>";
    let c = $(o).text(p.name);
    $("#productInput").append(c);
}

function addCompany(c) {
    let o = "<option></option>";
    let d = $(o).text(c.name);
    $("#buyingPartyInput, #sellingPartyInput").append(d);
}

function addTrade(trade) {
    let s = "<button class=\"btn trade-button d-block text-muted py-0 my-n1\"></button>";
    let b = $(s).text("Trade "+trade.tradeId).data("trade", trade);
    b.on("click", () => {
        loadTrade(trade);
    })
    let li = $("<li class=\"nav-item\"></li>").html(b);
    $("#trades").append(li);
};


function loadTrade(trade) {
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
