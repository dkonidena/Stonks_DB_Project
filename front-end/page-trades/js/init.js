var editWindow;

function init() {

    $.fn.dataTable.ext.errMode = 'none';

    const filters = [
        [elements.quantityInput, /^\d*$/],
        [elements.notionalPriceInput, /^\d*\.?\d*$/],
        [elements.underlyingPriceInput, /^\d*\.?\d*$/],
        [elements.strikePriceInput, /^\d*\.?\d*$/],
        [elements.maturityDateInput, /^[\d-]{0,10}$/],
        [elements.filterCreationDateLowerInput, /^[\d-]{0,10}$/],
        [elements.filterCreationDateUpperInput, /^[\d-]{0,10}$/],
        [elements.filterModificationDateLowerInput, /^[\d-]{0,10}$/],
        [elements.filterModificationDateUpperInput, /^[\d-]{0,10}$/],
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
        if (isValidTrade()) {
            if (allSuggestionsResolved()) {
                saveTrade();
            } else {
                $("#mustAcceptWarning").modal("show");
            }
        }
    });

    $("#checkTradeButton").on("click", () => {
        if (isValidTrade()) {
            getFeedback();
        }
    });

    $("#deleteObjectConfirmed").click(() => {
        let id = $("#tradeId").text();
        if (id !== "") {
            api.delete.trades(id, () => {
                showSuccess('Trade deleted');
                resetState();
            },showError)
        }
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
        currentFilter = filterObjectFromForm();
        $("#resultsStatus").show();
        $("#table-container").empty();
        $("#resultsModal").modal("show");
        getNextTradeBlock(true);
    });

    $("#resultsModal").on("hidden.bs.modal", () => {
        $("#table-container").DataTable().destroy();
        currentTradesNum = 0;
    });

    $("#searchTradesButton,#searchAgain").click(() => {
        resetFilter();
        $("#advancedSearch").modal("show");
    });

    $("#productInput").on("change", () => {
        populateSellerSelection();
    });

    $("#acceptAll").click(acceptAll);
    $("#ignoreAll").click(ignoreAll);

    getCompanyList(null, 'mostBoughtFrom', (companies) => {
        companies.forEach(addCompanyToUI);

        getProductList(null, (products) => {
            products.forEach(addProductToUI);
        });
    });

    getCurrencyList(null, (currencies) => {
        currencies.forEach(addCurrencyToUI);
    });

    getUserList((users) => {
        users.forEach(addUserToUI);
    });

    api.get.config((config) => {
        editWindow = config.days;
    }, showError);

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

    $('.date').datepicker({
        clearBtn: true,
        format: "dd-mm-yyyy",
        maxViewMode: 3,
        templates: {
            leftArrow: '<i class="material-icons align-bottom">keyboard_arrow_left</i>',
            rightArrow: '<i class="material-icons align-bottom">keyboard_arrow_right</i>',
        },
    });

    $("span[aria-labelledby='select2-notionalCurrencyInput-container']").css("background-color", "#e9ecef");
    $("span[aria-labelledby='select2-underlyingCurrencyInput-container']").css("background-color", "#e9ecef");
}

$(document).ready(init);
