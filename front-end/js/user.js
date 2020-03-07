const userElements = {
    label: $("#userLabel"),
    button: $("#userButton"),
    dropdown: $("#userDropdown"),
    icon: $("#userIcon"),
};

const configModal = `
<div class="modal fade" id="configModal" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">System Configuration</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body">
                <div class="container-fluid">
                    <form>
                        <div class="row">
                            <div class="col"><label for="config-numberOfDays">Editing time window (days)</label></div>
                            <div class="col"><input class="form-control" min="1" id="config-numberOfDays" type="number"></input>
                            </div>
                        </div><div class="row">
                            <div class="col"><label for="config-neigboursFromRules">KNN Neigbour Count</label></div>
                            <div class="col"><input class="form-control" min="1" id="config-neigboursFromRules" type="number"></input></div>
                        </div>
                        <div class="row">
                            <div class="col"><label for="config-noOfIterations">KNN Iterations</label></div>
                            <div class="col"><input class="form-control" min="1" id="config-noOfIterations" type="number"></input></div>
                        </div>
                    </form>
                <div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-primary" id="saveConfigButton" data-dismiss="modal">Save Changes</button>
            </div>
        </div>
    </div>
</div>`

const eventsModal = `
<div class="modal fade" id="activityLogModal" tabindex="-1" role="dialog">
    <div class="modal-dialog modal-xl" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">User Event Log</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body">
                <div id="events-table"></div>
            </div>
        </div>
    </div>
</div>`

//returns undefined if cookie not present
function getCurrentUserID() {
    return Cookies.get("userID");
};

function setCurrentUserID(id) {
    if (id === null || id === undefined) {
        Cookies.remove("userID");
    }
    else {
        //TODO: check id is valid when we have decided what userids should look like
        Cookies.set("userID", id);
    }
};

function tryLogIn(u) {
    if (u === undefined) {
        userLogOut();
        return false;
    }
    else {
        if (u in users) {
            userLogIn(u);
            setCurrentUserID(u);
            return true;
        } else {
            return false;
        }
    }
}

function userLogIn(id) {
    if (id === undefined) { return; }
    const colours = ["#007bff", "#6610f2", "#6f42c1", "#e83e8c", "#dc3545", "#fd7e14", "#ffc107", "#28a745", "#20c997", "#17a2b8", "#fff", "#343a40"];
    const userLoggedInHTML = `
    <a class="dropdown-item" id="userActivityLogButton" data-toggle="modal" data-target="#activityLogModal">Activity Log</a>
    <a class="dropdown-item" id="userLogoutButton" data-toggle="modal" data-target="#logoutModal">Logout</a>`;

    const configPage = `<a class="dropdown-item" id="userConfigPageButton" data-toggle="modal" data-target="#configModal">Config Page</a>`;

    userElements.label.text(id);
    if (id === "1870") {
        userElements.dropdown.html(configPage);
    }
    userElements.dropdown.append(userLoggedInHTML);
    userElements.icon.css("color", colours[id.hashCode()%colours.length]);

    const filters = [
        ["#config-numberOfDays", /^\d*$/],
        ["#config-neigboursFromRules", /^\d*$/],
        ["#config-noOfIterations", /^\d*$/]
    ];

    filters.forEach((x) => {
        setInputFilter($(x[0]), (v) => { return x[1].test(v) });
    });
}

function userLogOut() {
    const userLoggedOutHTML = "<a class=\"dropdown-item\" id=\"userLoginButton\">Login</a>";

    userElements.label.text("Not logged in");
    setCurrentUserID(null);
    userElements.dropdown.html(userLoggedOutHTML);
    $("#userLoginButton").on("click", showLoginModal);
    userElements.icon.css("color", "rgb(255,255,255,0.7)");

    let w = window.location.href;
    if (!w.endsWith("/page-home/page-home.html")) {
        window.location.href = "../page-home/page-home.html";
    }
}

function showLoginModal() {
    $("#loginModal").modal("show");
}

function showLogoutModal() {
    $("#logoutModal").modal("show");
}

function renderEventsTable(csv) {
    const blob = new Blob([csv], { type: "text/plain" });
    CsvToHtmlTable.init({
        csv_path: URL.createObjectURL(blob),
        element: "events-table",
        allow_download: false,
        csv_options: {"separator": ",", "delimiter": "\""},
        datatables_options: {
            "scrollY": "60vh",
            "paging": true
        },
        onComplete: () => {}
    });
}

function eventsToCSV(events) {
    let csv = "Date, UserID, Event Description, EventID, ReferenceID, Table Name, Type\n";
    for (const obj of events) {
        let fields = [
            obj["dateOfEvent"],
            obj["employeeID"],
            obj["eventDescription"],
            obj["eventID"],
            obj["referenceID"],
            obj["table"],
            obj["typeOfAction"]
        ];

        for (let i = 0; i < fields.length; i++) {
            let field = fields[i];
            if (i === fields.length - 1) {
                csv += `${field}\n`;
            } else {
                csv += `${field},`;
            }
        }
    }

    return csv;
}

function init() {
    const filters = [
        [$("#loginModalUserID"), /^\d*$/],
    ]

    filters.forEach((x) => {
        setInputFilter(x[0], (v) => { return x[1].test(v) });
    });

    $("body").append(configModal);
    $("body").append(eventsModal);

    $('#activityLogModal').on('shown.bs.modal', () => {
        api.get.events((events) => {
            renderEventsTable(eventsToCSV(events));
        }, showError);
    });

    $("#saveConfigButton").click(() => {
        let config = {
            days: $("#config-numberOfDays").val(),
            neighboursFromRules: $("#config-neigboursFromRules").val(),
            noOfIterations: $("#config-noOfIterations").val()
        };

        api.patch.config(config, console.log, showError);
    });

    // tryLogIn();
    $("#loginModalLoginButton").on("click", () => {
        //TODO: check id with server
        if (tryLogIn($("#loginModalUserID").val())) {
            $("#loginModalUserID").removeClass("is-invalid");
            slide();
        } else {
            $("#loginModalUserID").toggleClass("is-invalid");
        }
    });

    $("#logoutModalLogoutButton").on("click", () => {
        userLogOut();
        $("#logoutModal").modal("hide");
    });

    userLogIn(getCurrentUserID());

    api.get.config((res) => {
        $("#config-numberOfDays").val(res.days);
        $("#config-neigboursFromRules").val(res.neighboursFromRules);
        $("#config-noOfIterations").val(res.noOfIterations);
    }, showError);
};

$(document).ready(init);
