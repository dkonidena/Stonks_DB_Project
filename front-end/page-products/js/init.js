const filters = [
    ["#valueInUSDInput", /^\d*\.?\d*$/],
    ["#filter-creationDateLowerDayInput", /^\d{0,2}$/],
    ["#filter-creationDateLowerMonthInput", /^\d{0,2}$/],
    ["#filter-creationDateLowerYearInput", /^\d{0,4}$/],
    ["#filter-creationDateUpperDayInput", /^\d{0,2}$/],
    ["#filter-creationDateUpperMonthInput", /^\d{0,2}$/],
    ["#filter-creationDateUpperYearInput", /^\d{0,4}$/],
];

function init() {

    filters.forEach((x) => {
        setInputFilter($(x[0]), (v) => { return x[1].test(v) });
    });

    let elemProductListEmptyMessage = $("#productListEmptyMessage");
    elemProductListEmptyMessage.hide();
    elemProductListEmptyMessage.removeClass("d-none");

    $("#productIdInput,#productInpu,#valueInUSDInput,#companyInput").on("change", checkProductValidity);

    $("#productList").on("show.bs.collapse", () => {
        $("#productListCollapseSymbol").text("expand_less");
        if (isProductListEmpty()) {
            elemProductListEmptyMessage.show();
        }
    });

    $("#productList").on("hide.bs.collapse", () => {
        $("#productListCollapseSymbol").text("expand_more");
        elemProductListEmptyMessage.hide();
    });

    $("#addProductButton").click( () => {
        clearForm();
        showProductForm();
    });

    $("#saveProductButton").click( () => {
        let product = productObjectFromForm();
        if (product.id != "") {
            api.patch.products(product.id, product.getAPIObject(), () => {
                showSuccess('Product updated.');
                clearForm();
            }, showError);
        }
        else {
            api.post.products(product.getAPIObject(), () => {
                showSuccess('Product saved.');
                clearForm();
            }, showError);
        }
        //TODO add visual feedback of the save to user
    });

    $("#discardChangesButton").click(clearForm);

    $("#doAdvancedSearch").click( () => {
        clearProductList();
        getCompanyList(filterObjectFromForm(), 'mostBoughtFrom', (companies) => {
            companies.forEach(addCompanyToUI);

            getProductList(filterObjectFromForm(), (products) => {
                products.forEach(addProductToUI);
            })
        });
    });

    getCompanyList(new Date(), 'mostBoughtFrom', (companies) => {
        companies.forEach(addCompanyToUI);
    });

    $('.select2-comp').select2({
        theme: "bootstrap4"
    });
}

$(document).ready(init);
