var currencies = [];
var companies = [];
var products = [];
var trades = [];

class Trade {
    constructor(id) {
        this.tradeId = id;
        this.tradeDate = new Date();
        this.userIdCreatedBy = 0;
        this.lastModifiedDate = new Date();
        this.product = ""; // a Product ID
        this.buyingParty = ""; // a Company ID
        this.sellingParty = ""; // a Company ID
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

    getAPIObject() {
        let a = new APITrade();
        a.product = this.product;
        a.buyingParty = this.buyingParty;
        a.sellingParty = this.sellingParty;
        a.quantity = this.quantity;
        a.notionalPrice = this.notionalPrice;
        a.notionalCurrency = this.notionalCurrency;
        a.underlyingPrice = this.underlyingPrice;
        a.underlyingCurrency = this.underlyingCurrency;
        a.maturityDate = this.maturityDate.toISOString();
        a.strikePrice = this.strikePrice;
        return a;
    }

    populateFromServerJSON(o) {
        try {
            this.tradeId = o.tradeId;
            this.tradeDate = new Date(o.tradeDate);
            this.userIdCreatedBy = o.userIdCreatedBy;
            this.lastModifiedDate = new Date(o.lastModifiedDate);
            this.product = o.product;
            this.buyingParty = o.buyingParty;
            this.sellingParty = o.sellingParty;
            this.quantity = o.quantity;
            this.notionalPrice = o.notionalPrice;
            this.notionalCurrency = o.notionalCurrency;
            this.underlyingPrice = o.underlyingPrice;
            this.underlyingCurrency = o.underlyingCurrency;
            this.maturityDate = new Date(o.maturityDate);
            this.strikePrice = o.strikePrice;
            return this;
        }
        catch {
            return null;
        }
    }
};

class APITrade {
    constructor() {
        this.product = "";
        this.buyingParty = "";
        this.sellingParty = "";
        this.quantity = 0;
        this.notionalPrice = "";
        this.notionalCurrency = "";
        this.underlyingPrice = "";
        this.underlyingCurrency = "";
        this.maturityDate = "";
        this.strikePrice = "";
    }
}

function getTradeList(filter, res) {
    // default to between 2000 and now
    filter.dateCreated = [new Date("2000-01-01T00:00:00.000Z"), new Date()];

    api.get.trades(filter.getAPIObject(), false, (response) => {
        if (response.matches === undefined) {
            showError("Malformed server reponse", "matches field not present");
            return;
        }

        for (let json of response.matches) {
            let trade = new Trade();
            trade.populateFromServerJSON(json);  // TODO error handling
            if (trade != null)
                trades.push(trade);
        }

        if (res !== undefined) { res(trades); }
    }, showRequestError);
}

class Product {
    constructor() {
        this.id = "";
        this.name = "";
        this.companyId = "";
        this.value = 0;
        this.creationDate = new Date();
        this.userIdCreatedBy = 0;
    }

	getAPIObject() {
		let a = new APIProduct();
		a.id = this.id;
		a.value = this.value;
		a.company = this.companyId;
		return a;
	}

    populateFromServerJSON(o) {
        try {
            this.id = o.id;
            this.name = o.name;
            this.companyId = o.companyId;
            this.value = o.value;
            this.creationDate = new Date(o.value);
            this.userIdCreatedBy = o.userIdCreatedBy;
            return this;
        }
        catch {
            return null;
        }
    }
};

class APIProduct {
	constructor() {
		this.id = "";
		this.value = "";
		this.company = "";
	}
}

function getProductList(date, res) {
    api.get.products(date, false, (response) => {
        if (response.matches === undefined) {
            showError("Malformed server reponse", "matches field not present");
            return;
        }

        for (let json of response.matches) {
            let product = new Product();
            product.populateFromServerJSON(json);
            if (product != null)
                products.push(product);
        }

        if (res !== undefined) { res(products); }
    }, showRequestError);
}

class Currency {
    constructor(code, sym, decimal, val) {
        this.code = code;
        this.symbol = sym;
        this.allowDecimal = decimal;
        this.value = val;
    }

    populateFromServerJSON(o) {
        try {
            this.code = o.code;
            this.symbol = o.sym;
            this.allowDecimal = o.decimal;
            this.value = o.val;
            return this;
        }
        catch {
            return null;
        }

    }
};

function getCurrencyList(date, res) {
    api.get.currencies(date, false, (response) => {
        if (response.matches === undefined) {
            showError("Malformed server reponse", "matches field not present");
            return;
        }

        for (let json of response.matches) {
            let currency = new Currency();
            currency.populateFromServerJSON(json);
            if (currency != null)
                currencies.push(currency);
        }

        if (res !== undefined) { res(currencies); }
    }, showRequestError);
}

class Company {
    constructor() {
        this.id = "";
        this.name = "";
        this.creationDate = new Date();
        this.userIdCreatedBy = 0;
    }

	getAPIObject() {
		let c = new APICompany();
		c.id = this.id;
		return c;
	}

    populateFromServerJSON(o) {
        try {
            this.id = o.id;
            this.name = o.name;
            this.creationDate = new Date(o.creationDate);
            this.userIdCreatedBy = o.userIdCreatedBy;
            return this;
        }
        catch {
            return null;
        }
    }
};

class APICompany {
	constructor() {
		this.name = "";
	}
}

function getCompanyList(date, order, res) {
    api.get.companies(date, order, false, (response) => {
        if (response.matches === undefined) {
            showError("Malformed server reponse", "matches field not present");
            return;
        }

        for (let json of response.matches) {
            let company = new Company();
            company.populateFromServerJSON(json);
            if (company != null)
                companies.push(company);
        }

        if (res !== undefined) { res(companies); }
    }, showRequestError);
}

class Filter {
    constructor() {
        this.dateCreated = null;
    }

    getAPIObject() {
        // the API spec says that we should only send members that we actually
        // want to filter by. eg. if we only want to filter by date we only send
        // the dateCreated key

        let object = {};
        for (let key of Object.keys(this)) {
            if (this[key] !== null) {
                object[key] = this[key];
            }
        }

        return object;
    }
}

class TradeFilter extends Filter {
    constructor() {
        super();
        this.dateModified = null;
        this.tradeID = null;
        this.buyingParty = null;
        this.sellingParty = null;
        this.product = null;
        this.notionalCurrency = null;
        this.underlyingCurrency = null;
        this.userIDCreatedBy = null;
    }
}

class Report {
    constructor() {
        this.date = new Date();
        this.content = "";
    }

    populateFromServerJSON(o) {
        try {
            this.date = new Date(o.date);
            this.content = o.content;
            return this;
        }
        catch {
            return null;
        }
    }
}

function getReportList(filter, res, err) {
    api.get.reports(filter.getAPIObject(), false, (response) => {
        if (response.matches === undefined) {
            showError("Malformed server reponse for reports", "matches field not present");
            return;
        }

        let reports = [];
        for (let json of response.matches) {
            let report = new Report();
            reports.push(report.populateFromServerJSON(json));
        }

        if (res !== undefined) { res(reports); }
    }, showRequestError);
}
