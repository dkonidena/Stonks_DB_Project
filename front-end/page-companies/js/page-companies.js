var companies = {};

var newCompCount = 0;

function addCompanyToUI(company) {
    let s = "<button class=\"btn company-button d-block text-muted py-0 my-n1\"></button>";
    let b = $(s).text(company.name).data("company", company);
    b.on("click", () => {
        loadCompanyToForm(company);
        showCompanyForm();
    })
    let li = $("<li class=\"nav-item\"></li>").html(b);
    $("#companies").append(li);
}

function clearCompanyList() {
    $("#companies").html("");
    $("#filter-companyIdInput").html("");
}

function isCompanyListEmpty() {
    return $("#companies").html() === "";
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

function showCompanyForm() {
    if(!$("#companyEditorForm:visible").length) {
        $("#companyEditorMessage").hide();
        $("#companyEditorForm").show();
    }
}

function companyObjectFromForm() {
    let company = new Company();

    company.id = $("#companyIdInput").val();
    company.name = $("#companyInput").val();

    return company;
}

function checkCompanyValidity() {
    $("#saveCompanyButton").prop('disabled', !isValidCompany());
}

function isValidCompany() {
    return $("#companyInput").val() !== "";
}

function loadCompanyToForm(company) {
    if (company === null) {
        showError("Tried to load null company to form");
        return;
    }

    const fields = [
        ["#companyIdInput", company.id],
        ["#companyInput", company.name],
        ["#companyDateDayInput", company.dateEnteredIntoSystem.getDate()],
        ["#companyDateMonthInput", company.dateEnteredIntoSystem.getMonth()+1],
        ["#companyDateYearInput", company.dateEnteredIntoSystem.getFullYear()],
    ]

    fields.forEach((x) => {
            $(x[0]).val(x[1]).trigger("change");
    });
}

function clearForm() {
    let company = new Company();
    loadCompanyToForm(company);
}
