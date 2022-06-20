var inp_email = document.getElementById("email-inp");
var inp_pin = document.getElementById("pin-inp");
var validEmail = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;

function first_page() {
    if (inp_email.value.match(validEmail)) {
        document.querySelector(".second-page").style.display = "flex";
        document.querySelector(".first-page").style.display = "none";

        // document.querySelector(".num1").style.backgroundColor = "white";
        // document.querySelector(".num1").style.color = "black";

        document.querySelector(".num2").style.backgroundColor = "#513CD2";
        document.querySelector(".num2").style.color = "white";
        document.querySelector(".line").style.borderBottom = "3px solid #513CD2";

    }
    else {
        inp_email.style.borderColor = "red";
        inp_email.value = "";
        inp_email.placeholder = "Please enter valid email";
        return false;
    }
}

function second_page() {
    if (inp_pin.value == "") {
        inp_pin.style.borderColor = "red";
        inp_pin.placeholder = "Please fill out this field";
        return false;
    }
    else {
        document.querySelector(".third-page").style.display = "flex";
        document.querySelector(".second-page").style.display = "none";

        document.querySelector(".num3").style.backgroundColor = "#513CD2";
        document.querySelector(".num3").style.color = "white";
        document.querySelector(".line1").style.borderBottom = "3px solid #513CD2";
    }
}

