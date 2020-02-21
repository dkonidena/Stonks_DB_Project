const filters = [
    ["#valueInUSDInput", /^\d*\.?\d*$/],
    ["#filter-creationDateLowerDayInput", /^\d{0,2}$/],
    ["#filter-creationDateLowerMonthInput", /^\d{0,2}$/],
    ["#filter-creationDateLowerYearInput", /^\d{0,4}$/],
    ["#filter-creationDateUpperDayInput", /^\d{0,2}$/],
    ["#filter-creationDateUpperMonthInput", /^\d{0,2}$/],
    ["#filter-creationDateUpperYearInput", /^\d{0,4}$/],
];

$(document).ready(() => {
    filters.forEach((x) => {
        var t = x[0];
        setInputFilter(t, (v) => { return x[1].test(v) });
    });

    getCompanyList(null, 'mostBoughtFrom', (companies) => {
        companies.forEach(addCompanyToUI);
    });

    $("#addProductButton").click( () => {
        let product = new Product();
        product.if = `NEW${newProdCount++}`;
        addProductToUI(product);
        loadProductToForm(product);
    });

    $("#saveProductButton").click( () => {
        let product = productObjectFromForm();
        if (product.id != "") {
            api.patch.products(product.id, product.getAPIObject(), console.log, showError);
        }
        else {
            api.post.products(product.getAPIObject(), console.log, showError);
        }
        //TODO add visual feedback of the save to user
    });

    $("#discardChangesButton").click( () => {
        var product = Object.values(products).filter(t => t.id == $("#productIdInput").val())[0];
        loadProductToForm(product);
    });

    $("#doAdvancedSearch").click( () => {
        getProductList(filterObjectFromForm(), (products) => {
            products.forEach(addProductToUI);
        })
    });

    $('.select2-comp').select2({
        theme: "bootstrap4"
    });
});
