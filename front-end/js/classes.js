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

    getAPIObject() {
        let a = new APITrade();
        a.buyingParty = this.buyingParty;
        a.sellingParty = this.buyingParty;
        a.quantity = this.quantity;
        a.notionalPrice = this.notionalPrice;
        a.notionalCurrency = this.notionalCurrency;
        a.underlyingPrice = this.underlyingPrice;
        a.underlyingCurrency = this.underlyingCurrency;
        a.maturityDate = this.maturityDate.toISOString();
        a.strikePrice = this.strikePrice;
        return a;
    }
};

class APITrade {
    constructor() {
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

function * tradeGenerator(e) {
    let x = 0;
    while(true) {
        let t = new Trade();
        t.tradeId = e ? "NEW " + x++ : randInt(0, 999999999).toString().padStart(9, "0");
        t.tradeDate = new Date();
        t.userIdCreatedBy = randInt(0,9999999);
        t.lastModifiedDate = randDate();
        t.product = randProductString();
        t.buyingParty = randCompanyString();
        t.sellingParty = randCompanyString();
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
};

function getTradeList() {
    if (trades.length == 0) {
        for (let i = 0; i < 10; i++) {
            trades.push(tradeGenerator(false).next().value);
        }
    }
    return trades;
};

class Product {
    constructor() {
        this.id = 0;
        this.name = "";
        this.companyId = 0;
        this.value = 0;
        this.creatioDate = new Date();
        this.userIdCreatedBy = 0;
    }
};


function * productGenerator() {
    while (true) {
        let p = new Product();
        p.id = randInt(0, 999);
        p.name = "Product " + p.id;
        p.companyId = randInt(0, 999999);
        p.value = (randInt(0,9999) + Math.random()).toFixed(2);
        p.creatioDate = randDate();
        p.userIdCreatedBy = randInt(0, 999999);
        yield p;
    }
};

function getProductList() {
    if (products.length == 0) {
        for (let i = 0; i < 10; i++) {
            products.push(productGenerator().next().value);
        }
    }
    return products;
}

class Currency {
    constructor(code, sym, decimal, val) {
        this.code = code;
        this.symbol = sym;
        this.allowDecimal = decimal;
        this.value = val;
    }
};

function getCurrencyList() {
    if (currencies.length == 0) {
        currencyData.forEach((c) => {
            currencies.push(new Currency(c[0], c[1], c[2], c[3]));
        });
    }
    return currencies;
}

//the ten global most traded currencies
const currencyData = [
    ["USD", "$", true, 1],
    ["EUR", "€", true, 1],
    ["JPY", "¥", false, 1],
    ["GPB", "£", true, 1],
    ["AUD", "$", true, 1],
    ["CAD", "$", true, 1],
    ["CHF", "CHF", true, 1],
    ["CNY", "元", true, 1],
    ["HKD", "$", true, 1],
    ["NZD", "$", true, 1]
];

class Company {
    constructor() {
        this.id = 0;
        this.name = "";
        this.foundedDate = new Date();
        this.creationDate = new Date();
        this.userIdCreatedBy = 0;
    }
};


function * companyGenerator() {
    while (true) {
        let c = new Company();
        c.id = randInt(0, 999);
        c.name = "Company " + c.id;
        c.foundedDate = randDate();
        c.creationDate = randDate();
        c.userIdCreatedBy = randInt(0, 999999);
        yield c;
    }
}

function getCompanyList() {
    if (companies.length == 0) {
        for (let i = 0; i < 10; i++) {
            companies.push(companyGenerator().next().value);
        }
    }
    return companies;
}
