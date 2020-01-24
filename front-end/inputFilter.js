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

setInputFilter(document.getElementById("quantityInput"), (value) => {
	return /^\d*\.?\d*$/.test(value);
});

setInputFilter(document.getElementById("strikePriceInput"), (value) => {
	return /^\d*\.?\d*$/.test(value);
});

setInputFilter(document.getElementById("idInput"), (value) => {
	return /^\d*$/.test(value);
});

setInputFilter(document.getElementById("notionalValueInput"), (value) => {
	return /^\d*\.?\d*$/.test(value);
});

setInputFilter(document.getElementById("underlyingValueInput"), (value) => {
	return /^\d*\.?\d*$/.test(value);
});

//setInputFilter(document.getElementById("dateInput"), (value) => {
//	return /^\d{1,2}(-|\/|\.)\d{1,2}\1\d{2}(\d{2})?$/.test(value);
//});

//setInputFilter(document.getElementById("expiryInput"), (value) => {
//	return /^\d{1,2}(-|\/|\.)\d{1,2}\1\d{2}(\d{2})?$/.test(value);
//});
