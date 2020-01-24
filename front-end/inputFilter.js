function setInputFilter(textbox, inputFilter) {
	["input", "keydown", "keyup", "mousedown", "mouseup", "select", "contextmenu", "drop"].forEach(function (event) {
		textbox.addEventListener(event, function () {
			if (inputFilter(this.value)) {
				this.oldValue = this.value;
				this.oldSelectionStart = this.selectionStart;
				this.oldSelectionEnd = this.selectionEnd;
			} else if (this.hasOwnProperty("oldValue")) {
				this.value = this.oldValue;
				this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
			} else {
				this.value = "";
			}
		});
	});
}

setInputFilter(document.getElementById("quantityInput"), function (value) {
	return /^\d*\.?\d*$/.test(value);
});

setInputFilter(document.getElementById("strikePriceInput"), function (value) {
	return /^\d*\.?\d*$/.test(value);
});

setInputFilter(document.getElementById("idInput"), function (value) {
	return /^\d*$/.test(value);
});

setInputFilter(document.getElementById("notionalValueInput"), function (value) {
	return /^\d*\.?\d*$/.test(value);
});

setInputFilter(document.getElementById("underlyingValueInput"), function (value) {
	return /^\d*\.?\d*$/.test(value);
});

//setInputFilter(document.getElementById("dateInput"), function (value) {
//	return /^\d{1,2}(-|\/|\.)\d{1,2}\1\d{2}(\d{2})?$/.test(value);
//});

//setInputFilter(document.getElementById("expiryInput"), function (value) {
//	return /^\d{1,2}(-|\/|\.)\d{1,2}\1\d{2}(\d{2})?$/.test(value);
//});