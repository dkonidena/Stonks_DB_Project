const filters = [
];

function init() {
    let elemCompanyListEmptyMessage = $("#companyListEmptyMessage");
    elemCompanyListEmptyMessage.hide();
    elemCompanyListEmptyMessage.removeClass("d-none");

    $("#companyList").on("show.bs.collapse", () => {
        $("#companyListCollapseSymbol").text("expand_less");
        if (isCompanyListEmpty()) {
            elemCompanyListEmptyMessage.show();
        }
    });

    $("#companyList").on("hide.bs.collapse", () => {
        $("#companyListCollapseSymbol").text("expand_more");
        elemCompanyListEmptyMessage.hide();
    });

    filters.forEach((x) => {
        setInputFilter($(x[0]), (v) => { return x[1].test(v) });
    });

    $("#companyInput").on("change", checkCompanyValidity);

    $("#addCompanyButton").click( () => {
        clearForm();
        showCompanyForm();
    });

    $("#saveCompanyButton").click( () => {
        let company = companyObjectFromForm();
        if (company.id != "") {
            api.patch.companies(company.id, company.getAPIObject(), () => {
                showSuccess('Company updated.');
                clearForm();
            }, showError);
        }
        else {
            api.post.companies(company.getAPIObject(), () => {
                showSuccess('Company saved.');
                clearForm();
            }, showError);
        }
    });

    $("#discardChangesButton").click(clearForm);

    $("#deleteObjectConfirmed").click(() => {
        let id = $("#companyIdInput").val();
        if (id !== "") {
            api.delete.companies(id, () => {
                showSuccess('Trade deleted');
                clearForm();
            },showError)
        }
    });

    $("#doAdvancedSearch").click( () => {
        clearCompanyList();
        getCompanyList(filterObjectFromForm(), 'mostBoughtFrom', (companies) => {
            companies.forEach(addCompanyToUI);
        })
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
}

$(document).ready(init);
