const events = ["input", "keydown", "keyup", "mousedown", "mouseup", "select", "contextmenu", "drop"];

function setInputFilter(t, filter) {
    events.forEach((e) => {
        $(t).on(e, function () {
            if (filter(this.value)) {
                this.oldValue = this.value;
                this.oldSelectionStart = this.selectionStart;
                this.oldSelectionEnd = this.selectionEnd;
            }
            else if (this.hasOwnProperty("oldValue")) {
                this.value = this.oldValue;
                this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
            }
            else {
                this.value = "";
            }
        });
    });
}

function showError(error, debugData = 'no additional data', stringify = true) {
    if (stringify && debugData !== '') debugData = JSON.stringify(debugData, null, 2);
    showErrorDialogue(error, debugData);
}

function showErrorDialogue(error = '', detail = '') {
    $('#errorShort').text(error);
    $('#errorDetailContent').text(detail);
    $('#apiErrorModal').modal('show');
}

//use for accessing xxx.yyy where xxx can be null
function nullMemberAccess(parent, child) {
    if (parent === null || parent === undefined) {
        return null;
    }
    else return parent[child];
}

function randInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1) ) + min;
}

function randDate() {
    return new Date(randInt(1990,2020), randInt(0,11), randInt(1,30), 0, 0, 0, 0);
}

function randCurrency() {
    let l = getCurrencyList();
    return l[randInt(0,l.length-1)];
}

function randCompany() {
    let c = getCompanyList();
    return c[randInt(0,c.length-1)];
}

function randProduct() {
    let p = getProductList();
    return p[randInt(0,p.length-1)];
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

function randCompanyString() {
    return randCompany().name;
}

function randProductString() {
    return randProduct().name;
}
