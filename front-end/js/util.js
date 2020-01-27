function randInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1) ) + min;
}

function randDate() {
    return new Date(randInt(1990,2020), randInt(0,11), randInt(1,30) ,0 ,0 ,0 ,0);
}

function randCurrency() {
    let l = getCurrencyList();
    return l[randInt(0,l.length-1)];
}

function randCurrencyString(c) {
    let x = randInt(0, 1000);
    if (c.allowDecimal) {
        x += Math.random();
        x = x.toFixed(2);
    }
    else {
        x = x.toFixed(0);
    }
    return x;
}

function randProduct() {
    return "";
}

function randCompany() {
    return "";
}
