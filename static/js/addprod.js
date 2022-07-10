//------------------ rightside------------------------
document.getElementById("inp_right").readOnly = true;
document.getElementById("cardnum").readOnly = true;
document.getElementById("cvv").readOnly = true;
document.getElementById("edate").readOnly = true;
document.getElementById("checkout").disabled = true;

var inp_left = document.getElementById('inp_left');
var task = document.getElementById("task");
var require = document.getElementById("require");
var guide = document.getElementById("guide");

//----------------- right side-----------------------
var inp_right = document.getElementById("inp_right");
var cardnum = document.getElementById("cardnum");
var cvv = document.getElementById("cvv");
var edate = document.getElementById("edate");

function leftside() {

    if (inp_left.value == "") {
        inp_left.style.borderColor = "red";
        inp_left.placeholder = "Please fill out this field";
        return false;
    }

    else if (task.value == "") {
        task.style.borderColor = "red";
        task.placeholder = "Please fill out this field";
        return false;
    }

    else if (require.value == "") {
        require.style.borderColor = "red";
        require.placeholder = "Please fill out this field";
        return false;
    }

    else if (guide.value == "") {
        guide.style.borderColor = "red";
        guide.placeholder = "Please fill out this field";
        return false;
    }

    else {

        // if (inp_left.value == "") {
        //     inp_left.style.borderColor = "red";
        //     inp_left.placeholder = "Please fill out this field";
        //     return false;
        // }

        // else if (task.value == "") {
        //     task.style.borderColor = "red";
        //     task.placeholder = "Please fill out this field";
        //     return false;
        // }

        // else if (require.value == "") {
        //     require.style.borderColor = "red";
        //     require.placeholder = "Please fill out this field";
        //     return false;
        // }

        // else if (guide.value == "") {
        //     guide.style.borderColor = "red";
        //     guide.placeholder = "Please fill out this field";
        //     return false;
        // }

        //----------------- left side------------------------
        inp_left.readOnly = true;
        task.readOnly = true;
        require.readOnly = true;
        guide.readOnly = true;

        //----------------- right side-----------------------
        inp_right.readOnly = false;
        cardnum.readOnly = false;
        cvv.readOnly = false;
        edate.readOnly = false;

        //------------------ buttons-------------------------
        document.getElementById("next_step").disabled = true;

        document.getElementById("checkout").style.backgroundColor = "#513CD2";
        document.getElementById("checkout").disabled = false;

        //-----------------= step number---------------------
        document.querySelector(".num1").style.backgroundColor = "white";
        document.querySelector(".num1").style.color = "black";

        document.querySelector(".num2").style.backgroundColor = "#513CD2";
        document.querySelector(".num2").style.color = "white";

    }

}


//-------------- makes form right side invisible when width is 500px-----------
const mediaQuery = window.matchMedia('screen and (max-width: 500px)')
if (mediaQuery.matches) {
    document.querySelector(".right").style.opacity = "0";
    document.querySelector(".two").style.opacity = "0";
}

const next = document.querySelector(".next");
const right = document.querySelector(".right");
const left = document.querySelector(".left");
const one = document.querySelector(".one");
const two = document.querySelector(".two");

next.addEventListener("click", () => {

    if (inp_left.value == "") {
        inp_left.style.borderColor = "red";
        inp_left.placeholder = "Please fill out this field";
        return false;
    }

    else if (task.value == "") {
        task.style.borderColor = "red";
        task.placeholder = "Please fill out this field";
        return false;
    }

    else if (require.value == "") {
        require.style.borderColor = "red";
        require.placeholder = "Please fill out this field";
        return false;
    }

    else if (guide.value == "") {
        guide.style.borderColor = "red";
        guide.placeholder = "Please fill out this field";
        return false;
    }

    else {
        //------------- activates form right side---------------------
        right.classList.toggle("active");
        two.classList.toggle("active");

        //--------------makes form left side inactive-----------------
        left.classList.toggle("inactive");
        one.classList.toggle("inactive");

        document.getElementById("checkout").style.backgroundColor = "#513CD2";
        document.getElementById("checkout").disabled = false;

        //-------------- makes form right side visible---------------------
        document.querySelector(".two").style.opacity = "100";
        document.querySelector(".right").style.opacity = "100";

        //------------- makes form right side input editable----------------
        document.getElementById("inp_right").readOnly = false;
        document.getElementById("cardnum").readOnly = false;
        document.getElementById("cvv").readOnly = false;
        document.getElementById("edate").readOnly = false;
    }


})

function leftsubmit() {
    var regName = /^[a-zA-Z]+ [a-zA-Z]+$/;
    if (inp_right.value == "") {
        inp_right.style.borderColor = "red";
        inp_right.placeholder = "Please enter your name";
        return false;
    }

    else if (inp_right.value != inp_right.value.match(regName)) {
        inp_right.value = ""
        inp_right.style.borderColor = "red";
        inp_right.placeholder = "Please enter valid name";
        return false;
    }

    else if (cardnum.value == "") {
        cardnum.style.borderColor = "red";
        cardnum.placeholder = "Please enter card number";
        return false;
    }

    else if (cardnum.value > 9999999999999999) {
        cardnum.style.borderColor = "red";
        cardnum.value = "";
        cardnum.placeholder = "Enter between 15-16 digits";
        return false;
    }

    else if (cardnum.value < 100000000000000) {
        cardnum.style.borderColor = "red";
        cardnum.value = "";
        cardnum.placeholder = "Enter between 15-16 digits";
        return false;
    }

    else if (cvv.value == "") {
        cvv.style.borderColor = "red";
        cvv.placeholder = "Please enter cvv";
        return false;
    }

    else if (cvv.value > 9999) {
        cvv.style.borderColor = "red";
        cvv.value = "";
        cvv.placeholder = "Enter between 3-4 digits";
        return false;
    }

    else if (cvv.value < 100) {
        cvv.style.borderColor = "red";
        cvv.value = "";
        cvv.placeholder = "Enter between 3-4 digits";
        return false;
    }

    else if (edate.value == "") {
        edate.style.borderColor = "red";
        edate.placeholder = "Please enter edate";
        return false;
    }

    else {
        document.getElementById("checkout").addEventListener("click", (event) => {
            event.preventDefault();
            document.getElementById('form_left').submit();
            alert('you have submitted');
        })
    }
}





