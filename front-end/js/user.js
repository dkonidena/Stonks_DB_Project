const userElements = {
    label: $("#userLabel"),
    button: $("#userButton"),
    dropdown: $("#userDropdown"),
    icon: $("#userIcon"),
};

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

function tryLogIn() {
    let u = getCurrentUserID();
    if (u === undefined) {
        userLogOut();
        return false;
    }
    else {
        userLogIn(u);
        return true;
    }
}

function userLogIn(id) {
    const colours = ["#007bff", "#6610f2", "#6f42c1", "#e83e8c", "#dc3545", "#fd7e14", "#ffc107", "#28a745", "#20c997", "#17a2b8", "#fff", "#343a40"];
    const userLoggedInHTML = "<a class=\"dropdown-item\" id=\"userActivityLogButton\">Activity Log</a> <a class=\"dropdown-item\" id=\"userLogoutButton\">Logout</a>";

    //TODO: check id against database
    userElements.label.text(id);
    setCurrentUserID(id);
    userElements.dropdown.html(userLoggedInHTML);
    $("#userActivityLogButton").on("click", () => {
        showError("NotImplementedError");
    });
    $("#userLogoutButton").on("click", showLogoutModal);
    userElements.icon.css("color", colours[id.hashCode()%colours.length]);
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

function init() {
    const filters = [
        [$("#loginModalUserID"), /^[0-9a-zA-Z]*$/],
    ]

    filters.forEach((x) => {
        setInputFilter(x[0], (v) => { return x[1].test(v) });
    });

    tryLogIn();
    $("#loginModalLoginButton").on("click", () => {
        //TODO: check id with server
        if ($("#loginModalUserID").val() === "") { return }
        userLogIn($("#loginModalUserID").val());
        slide();
    });
    $("#logoutModalLogoutButton").on("click", () => {
        userLogOut();
        $("#logoutModal").modal("hide");
    });
};

$(document).ready(init);
