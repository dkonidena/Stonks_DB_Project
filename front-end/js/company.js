class Company {
    constructor() {
        this.id = 0;
        this.name = "";
        this.foundedDate = new Date();
        this.creationDate = new Date();
        this.userIdCreatedBy = 0;
    }
};

var companies = [];

function * companyGenerator() {
    while (true) {
        let c = new Company();
        c.id = randInt(0, 999);
        c.name = "Company " + c.id;
        c.foundedDate = randDate();
        c.creationDate = randDate();
        c.userIdCreatedBy = randInt(0, 999999);
        yield c;
    }
}

function addCompany(c) {
    let o = "<option></option>";
    let d = $(o).text(c.name);
    $("#buyingPartyInput, #sellingPartyInput").append(d);
}

function getCompanyList() {
    if (companies.length == 0) {
        for (let i = 0; i < 10; i++) {
            companies.push(companyGenerator().next().value);
        }
    }
    return companies;
}
