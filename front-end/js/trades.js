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
};

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


    $("#quantityInput").val(trade.quantity);
    $("#strikePriceInput").val(trade.strikePrice);
}
