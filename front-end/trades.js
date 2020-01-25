class Trade {
	constructor(id) {
		this.tradeId = id;
		this.dateOfTrade = new Date();
		this.userIdCreatedBy = 0;
		this.lastModified = new Date();

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
	let a = trade.tradeId;
	$("#tradeIdInput").val(a);
}


$("#addTradeButton").on("click", () => {
	let id = ($("#trades").children().length + 1).toString().padStart(9, "0");
	let trade = new Trade(id);
	addTrade(trade);
});
