function init() {

    const filters = [
        [elements.quantityInput, /^\d*$/],
        [elements.notionalPriceInput, /^\d*\.?\d*$/],
        [elements.underlyingPriceInput, /^\d*\.?\d*$/],
        [elements.strikePriceInput, /^\d*\.?\d*$/],
        [elements.maturityDateDayInput, /^\d{0,2}$/],
        [elements.maturityDateMonthInput, /^\d{0,2}$/],
        [elements.maturityDateYearInput, /^\d{0,4}$/],
        [elements.filterCreationDateLowerDayInput, /^\d{0,2}$/],
        [elements.filterCreationDateLowerMonthInput, /^\d{0,2}$/],
        [elements.filterCreationDateLowerYearInput, /^\d{0,4}$/],
        [elements.filterCreationDateUpperDayInput, /^\d{0,2}$/],
        [elements.filterCreationDateUpperMonthInput, /^\d{0,2}$/],
        [elements.filterCreationDateUpperYearInput, /^\d{0,4}$/],
        [elements.filterModificationDateLowerDayInput, /^\d{0,2}$/],
        [elements.filterModificationDateLowerMonthInput, /^\d{0,2}$/],
        [elements.filterModificationDateLowerYearInput, /^\d{0,4}$/],
        [elements.filterModificationDateUpperDayInput, /^\d{0,2}$/],
        [elements.filterModificationDateUpperMonthInput, /^\d{0,2}$/],
        [elements.filterModificationDateUpperYearInput, /^\d{0,4}$/],
    ];

    filters.forEach((x) => {
        setInputFilter(x[0], (v) => { return x[1].test(v) });
    });

    Object.values(elements).forEach((x) => {
        x.on("change", checkTradeValidity);
    });

    elements.notionalCurrencyInput.on("change", () => {
        try {
            let selection = elements.notionalCurrencyInput.select2("data")[0];
            let curr = currencies[selection.text];

            $("#notionalCurrencySymbol").text(curr.symbol);
            elements.notionalPriceInput.prop("placeholder", curr.getPlaceholder());
        } catch (e) {}
    });

    elements.underlyingCurrencyInput.on("change", () => {
        try {
            let selection = elements.underlyingCurrencyInput.select2("data")[0];
            let curr = currencies[selection.text];

            $("#underlyingCurrencySymbol").text(curr.symbol);
            $("#strikePriceCurrencySymbol").text(curr.symbol);
            elements.underlyingPriceInput.prop("placeholder", curr.getPlaceholder());
            elements.strikePriceInput.prop("placeholder", curr.getPlaceholder);
        } catch (e) {}
    });

    $("#addTradeButton").on("click", () => {
        let t = new Trade();
        t.notionalCurrency = currencies['USD'];
        t.underlyingCurrency = currencies['USD'];
        trades[t.tradeId] = t;
        loadTradeToForm(t);
        showTradeForm();
    });

    $("#saveTradeButton").on("click", () => {
        if(!$("#suggestionsTable:visible").length) {
            getFeedback();
        } else {
            if (allSuggestionsResolved()) {
                saveTrade();
                $("#suggestionsTable").hide();
                $("#saveTradeButton").text("Check Trade");
            } else {
                getFeedback();
            }
        }
    });

    $("#checkTradeButton").on("click", () => {
        api.post.check_trade(tradeObjectFromForm().getAPIObject(), console.log, showError);
        //TODO add visual feedback of the checks
    });

    $("#discardChangesButton").on("click", () => {
        let t = new Trade();
        t.notionalCurrency = currencies['USD'];
        t.underlyingCurrency = currencies['USD'];
        trades[t.tradeId] = t;
        loadTradeToForm(t);
        resetState();
    });

    $("#doAdvancedSearch").on("click", () => {
        let filter = filterObjectFromForm();
        getTradeList(filter, (trades) => {
            showResults(trades);
        });
    });

    $("#searchTradesButton,#searchAgain").click(() => {
        $("#advancedSearch").modal("show");
    });

    $("#acceptAll").click(acceptAll);
    $("#ignoreAll").click(ignoreAll);

    getCompanyList(null, 'mostBoughtFrom', (companies) => {
        companies.forEach(addCompanyToUI);

        getProductList(null, (products) => {
            products.forEach(addProductToUI);
        });
    });

    getCurrencyList(new Date(), (currencies) => {
        currencies.forEach(addCurrencyToUI);
    });

    getUserList((users) => {
        users.forEach(addUserToUI);
    });

    $('.select2-cur').select2({
        maximumInputLength: 3,
        theme: "bootstrap4",
        width: "auto",
        dropdownCss: {"font-size": "0.8rem"}
    });

    $('.select2-comp, .select2-prod').select2({
        theme: "bootstrap4"
    });

    $('.select2-filter').select2({
        theme: "bootstrap4",
        multiple: true,
    });

    $("span[aria-labelledby='select2-notionalCurrencyInput-container']").css("background-color", "#e9ecef");
    $("span[aria-labelledby='select2-underlyingCurrencyInput-container']").css("background-color", "#e9ecef");
}

$(document).ready(init);
