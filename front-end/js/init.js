const filters = [
    ["#tradeIdInput", /^\d{0,9}$/],
    ["#quantityInput", /^\d*$/],
    ["#notionalPriceInput", /^\d*\.?\d*$/],
    ["#underlyingPriceInput", /^\d*\.?\d*$/],
    ["#strikePriceInput", /^\d*\.?\d*$/],
    ["#tradeDateDayInput", /^\d{0,2}$/],
    ["#tradeDateMonthInput", /^\d{0,2}$/],
    ["#tradeDateYearInput", /^\d{0,4}$/],
    ["#maturityDateDayInput", /^\d{0,2}$/],
    ["#maturityDateMonthInput", /^\d{0,2}$/],
    ["#maturityDateYearInput", /^\d{0,4}$/],
];

function init() {

    $("#notionalCurrencyInput").on("change", () => {
        var selected = $("#notionalCurrencyInput option:selected");
        $("#notionalCurrencySymbol").text(selected.data("symbol"));
        $("#notionalValueInput").prop("placeholder", selected.data("placeholder"));
    });

    $("#underlyingCurrencyInput").on("change", () => {
        var selected = $("#underlyingCurrencyInput option:selected");
        $("#underlyingCurrencySymbol").text(selected.data("symbol"));
        $("#strikePriceCurrencyCymbol").text(selected.data("symbol"));
        $("#underlyingValueInput").prop("placeholder", selected.data("placeholder"));
        $("#strikePriceInput").prop("placeholder", selected.data("placeholder"));
    });

    $("#tradeList").on("show.bs.collapse", () => {
        $("#tradeListCollapseSymbol").text("expand_less");
    });

    $("#tradeList").on("hide.bs.collapse", () => {
        $("#tradeListCollapseSymbol").text("expand_more");
    });

    $("#addTradeButton").on("click", () => {
        addTrade(tradeGenerator().next().value);
    });

    filters.forEach((x) => {
        var t = x[0];
        setInputFilter(t, (v) => { return x[1].test(v) });
    });

    getCurrencyList().forEach((c) => {
        addCurrency(c);
    });

    $('.select2-cur').select2({
        maximumInputLength: 3,
        theme: "bootstrap4",
        width: "auto",
        dropdownCss: {"font-size": "0.8rem"}
    });

    $("span[aria-labelledby='select2-notionalCurrencyInput-container']").css("background-color", "#e9ecef");
    $("span[aria-labelledby='select2-underlyingCurrencyInput-container']").css("background-color", "#e9ecef");
}

$(document).ready(function() {
    init();
});
