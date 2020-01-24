
$("#notionalCurrencySelect").on("change", function () {
    var selected = $("#notionalCurrencySelect option:selected");
    $("#notionalCurrencySymbol").text(selected.data("symbol"))
    $("#notionalValueInput").prop("placeholder", selected.data("placeholder"))
})


$("#underlyingCurrencySelect").on("change", function () {
    var selected = $("#underlyingCurrencySelect option:selected");
    $("#underlyingCurrencySymbol").text(selected.data("symbol"))
    $("#strikePriceCurrencyCymbol").text(selected.data("symbol"))
    $("#underlyingValueInput").prop("placeholder", selected.data("placeholder"))
    $("#strikePriceInput").prop("placeholder", selected.data("placeholder"))
})
