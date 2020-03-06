var companies = {};
var products = {};

var newProdCount = 0;

function addProductToUI(product) {
    let s = "<button class=\"btn product-button d-block text-muted py-0 my-n1\"></button>";
    let b = $(s).text(product.name).data("product", product);
    b.on("click", () => {
        loadProductToForm(product);
        showProductForm();
    })
    let li = $("<li class=\"nav-item\"></li>").html(b);
    $("#products").append(li);
}

function addCompanyToUI(c) {
    let o = "<option></option>";
    let d = $(o).text(c.name);
    $("#companyInput").append(d);
}

function showProductForm() {
    if(!$("#productEditorForm:visible").length) {
        $("#productEditorMessage").hide();
        $("#productEditorForm").show();
    }
}

function clearProductList() {
    $("#products").html("");
    $("#filter-productIdInput").html("");
}

function isProductListEmpty() {
    return $("#products").html() === "";
}

function filterObjectFromForm() {
    if ($("#filter-creationDateLowerDayInput").val() !== "") {
        let date = new Date();
        date.setHours(0,0,0,0);
        date.setDate($("#filter-creationDateLowerDayInput").val());
        date.setMonth($("#filter-creationDateLowerMonthInput").val()-1);
        date.setFullYear($("#filter-creationDateLowerYearInput").val());
        return date;
    } else {
        return null;
    }
}

function productObjectFromForm() {
    let product = new Product();

    product.id = $("#productIdInput").val();
    product.name = $("#productInput").val();
    product.valueInUSD = $("#valueInUSDInput").val();
    product.company = companyNameToObject($("#companyInput").val());

    return product;
}

function checkProductValidity() {
    $("#saveProductButton").prop('disabled', !isValidProduct());

    if ($("#productIdInput").val() === "") {
        $("#deleteObject").hide();
    } else {
        $("#deleteObject").show();
    }
}

function isValidProduct() {
    let obj;
    try {
        obj = productObjectFromForm().getAPIObject()
    } catch (e) {
        return false;
    }

    for (const value of Object.values(obj)) {
        if (value === "") {
            return false;
        }
    }

    return true;
}

function loadProductToForm(product) {
    if (product === null) {
        showError("Tried to load null product to form");
        return;
    }

    const fields = [
        ["#productIdInput", product.id],
        ["#productInput", nullMemberAccess(product, "name")],
        ["#companyInput", nullMemberAccess(product.company, "name")],
        ["#productDateDayInput", product.dateEnteredIntoSystem.getDate()],
        ["#productDateMonthInput", product.dateEnteredIntoSystem.getMonth()+1],
        ["#productDateYearInput", product.dateEnteredIntoSystem.getFullYear()],
        ["#valueInUSDInput", product.valueInUSD]
    ]

    fields.forEach((x) => {
        try {
            $(x[0]).val(x[1]).trigger("change");
        }
        catch {
            $(x[0]).val(null).trigger("change");
        }

    });

    checkProductValidity();
}

function companyNameToObject(name) {
    return Object.values(companies).filter(x => x.name === name)[0];
}

function clearForm() {
    let product = new Product();
    loadProductToForm(product);
}
