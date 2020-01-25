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
    $("#tradeDateInput").val(trade.tradeDate);
    $("#maturityDateInput").val(trade.maturityDate);
    $("#quantityInput").val(trade.quantity);
    $("#strikePriceInput").val(trade.strikePrice);
}


$("#addTradeButton").on("click", () => {
    let id = ($("#trades").children().length + 1).toString().padStart(9, "0");
    let trade = new Trade(id);
    trade.tradeDate = new Date(1990, 0, 1, 0, 0, 0, 0);
    trade.maturityDate = new Date(1990, 0, 1, 0, 0, 0, 0);
    trade.quantity = 100;
    trade.strikePrice = "320.20";
    addTrade(trade);
});
