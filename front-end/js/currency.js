class Currency {
    constructor(code, sym, decimal, val) {
        this.code = code;
        this.symbol = sym;
        this.allowDecimal = decimal;
        this.value = val;
    }
};

function addCurrency(cur) {
    let o = "<option></option>";
    let c = $(o).text(cur.code).attr({
        "data-symbol": cur.symbol,
        "data-placeholder": cur.allowDecimal ? "0.00" : "0"
    });
    $("#notionalCurrencyInput, #underlyingCurrencyInput").append(c);
};

function getCurrencyList() {
    let currencyList = [];
    currencyData.forEach((c) => {
        currencyList.push(new Currency(c[0], c[1], c[2], c[3]));
    });
    return currencyList;
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
