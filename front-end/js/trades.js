class Trade {
    constructor(id) {
        this.tradeId = id;
        this.tradeDate = new Date();
        this.userIdCreatedBy = 0;
        this.lastModifiedDate = new Date();

        this.product = "";
        this.buyingParty = "";
        this.sellingParty = "";
        this.quantity = 0;
        this.notionalPrice = "";
        this.notionalCurrency = "";
        this.underlyingPrice = "";
        this.underlyingCurrency = "";
        this.maturityDate = new Date();
        this.strikePrice = "";
    }

    getNotionalCurrencyObject() {
        return getCurrencyList().filter((x) => { x.code == this.notionalCurrency })[0];
    }

    getUnderlyingCurrencyObject() {
        return getCurrencyList().filter((x) => { x.code == this.underlyingCurrency })[0];
    }
};

function * tradeGenerator() {
    while(true) {
        let t = new Trade();
        t.tradeId = randInt(0, 999999999);
        t.tradeDate = randDate();
        t.userIdCreatedBy = randInt(0,9999999);
        t.lastModifiedDate = randDate();
        t.product = "";
        t.buyingParty = "";
        t.sellingParty = "";
        t.quantity = randInt(0, 100);
        let c1 = randCurrency();
        let c2 = randCurrency();
        t.notionalCurrency = c1.code;
        t.notionalPrice = randCurrencyString(c1);
        t.underlyingCurrency = c2.code;
        t.underlyingPrice = randCurrencyString(c2);
        t.maturityDate = randDate();
        t.strikePrice = randCurrencyString(c2);
        yield t;
    }
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
