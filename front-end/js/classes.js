var currencies = {};
var companies = {};
var products = {};
var trades = {};
var users = {};

class Trade {
    constructor(id) {
        this.tradeId = id;
        this.tradeDate = new Date();
        this.userIdCreatedBy = 0;
        this.lastModifiedDate = null; //new Date();
        this.product = null; //new Product();
        this.buyingParty = null; //new Company();
        this.sellingParty = null; //new Company();
        this.quantity = "";
        this.notionalPrice = "";
        this.notionalCurrency = null; //new Currency();
        this.underlyingPrice = ""
        this.underlyingCurrency = null; //new Currency();;
        this.maturityDate = new Date();
        this.strikePrice = "";
    }

    getAPIObject() {
        let a = new APITrade();
        a.product = this.product.id;
        a.buyingParty = this.buyingParty.id;
        a.sellingParty = this.sellingParty.id;
        a.quantity = this.quantity;
        a.notionalPrice = this.notionalPrice;
        a.notionalCurrency = this.notionalCurrency.code;
        a.underlyingPrice = this.underlyingPrice;
        a.underlyingCurrency = this.underlyingCurrency.code;
        a.maturityDate = this.maturityDate.toISOString();
        a.strikePrice = this.strikePrice;
        return a;
    }

    populateFromServerJSON(o) {
        //TODO: make less ugly
        try {
            this.tradeId = o.tradeID;
            this.tradeDate = new Date(o.tradeDate);
            this.userIdCreatedBy = o.userIDcreatedBy;
            this.lastModifiedDate = new Date(o.lastModifiedDate);
            this.product = products[o.product];
            this.buyingParty = companies[o.buyingParty];
            this.sellingParty = companies[o.sellingParty];
            this.quantity = o.quantity;
            this.notionalPrice = o.notionalPrice;
            this.notionalCurrency = currencies[o.notionalCurrency];
            this.underlyingPrice = o.underlyingPrice;
            this.underlyingCurrency = currencies[o.underlyingCurrency];
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
    api.get.trades(filter.getAPIObject(), false, (response) => {
        if (response['matches'] === undefined) {
            showError("Malformed server reponse", "trade matches field not present", false);
            return;
        }

        for (let json of response.matches) {
            let trade = new Trade();
            trade.populateFromServerJSON(json);  // TODO error handling
            trades[trade.tradeId] = trade;
        }

        res(Object.values(trades));
    }, showError);
}

class Product {
    constructor() {
        this.id = "";
        this.name = "";
        this.company = null; //new Company();
        this.valueInUSD = "";
        this.dateEnteredIntoSystem = new Date();
        this.userIDcreatedBy = "";
    }

	getAPIObject() {
		let a = new APIProduct();
		a.name = this.name;
		a.valueInUSD = this.valueInUSD;
		a.companyID = this.company.id;
		return a;
	}

    populateFromServerJSON(o) {
        try {
            //TODO make less ugly
            this.id = o.id;
            this.name = o.name;
            this.company = companies[o.companyID];
            this.valueInUSD = o.valueInUSD;
            this.dateEnteredIntoSystem = new Date(o.dateEnteredIntoSystem);
            this.userIDcreatedBy = o.userIDcreatedBy;
            return this;
        }
        catch {
            return null;
        }
    }
};

class APIProduct {
	constructor() {
		this.name = "";
		this.valueInUSD = "";
		this.companyID = "";
	}
}

function getProductList(date, res) {
    api.get.products(date, false, (response) => {
        if (response.matches === undefined) {
            showError("Malformed server reponse", "product matches field not present");
            return;
        }

        for (let json of response.matches) {
            let product = new Product();
            product.populateFromServerJSON(json);
            products[product.id] = product;
        }

        res(Object.values(products));
    }, showError);
}

class Currency {
    constructor() {
        this.code = "";
        this.symbol = "";
        this.allowDecimal = true;
        this.valueInUSD = "";
    }

    getPlaceholder() {
        return this.allowDecimal ? "0.00" : "0";
    }

    populateFromServerJSON(o) {
        try {
            this.code = o.code;
            this.symbol = o.symbol;
            this.allowDecimal = o.allowDecimal;
            this.valueInUSD = o.valueInUSD;
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
            showError("Malformed server reponse", "currency matches field not present");
            return;
        }

        for (let json of response.matches) {
            let currency = new Currency();
            currency.populateFromServerJSON(json);
            currencies[currency.code] = currency;
        }

        res(Object.values(currencies));
    }, showError);
}

class Company {
    constructor() {
        this.id = "";
        this.name = "";
        this.dateEnteredIntoSystem = new Date();
        this.userIDcreatedBy = "";
    }

	getAPIObject() {
		let c = new APICompany();
		c.name = this.name;
		return c;
	}

    populateFromServerJSON(o) {
        try {
            this.id = o.id;
            this.name = o.name;
            this.dateEnteredIntoSystem = new Date(o.dateEnteredIntoSystem);
            this.userIDcreatedBy = o.userIDcreatedBy;
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
            showError("Malformed server reponse", "company matches field not present");
            return;
        }

        for (let json of response.matches) {
            let company = new Company();
            company.populateFromServerJSON(json);
            companies[company.id] = company;
        }

        res(Object.values(companies));
    }, showError);
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
    }, showError);
}

class User {
    constructor() {
        this.id = "";
        this.name = "";
    }

    populateFromServerJSON(o) {
        try {
            this.id = o.id;
            this.name = o.name;
            return this;
        }
        catch {
            return null;
        }
    }
}

function getUserList(res, err) {
    api.get.users(false, (response) => {
        if (response.matches === undefined) {
            showError("Malformed server reponse for users", "matches field not present");
            return;
        }

        for (let json of response.matches) {
            let user = new User();
            user.populateFromServerJSON(json);
            users[user.id] = user;
        }

        res(Object.values(users));
    }, showError);
}
