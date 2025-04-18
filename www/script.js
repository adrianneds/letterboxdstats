const observer = new MutationObserver(() => {
    if (valid == true) {
        document.getElementById("content-div").style.display = "block";
        document.getElementById("content-div").style.visibility = "visible";
    }
});

let valid = true;

const observer2 = new MutationObserver(() => {
    // document.getElementById("content-div").style.display = "none";
    // document.getElementById("content-div").style.visibility = "hidden";
    valid = false;
});

var config = { attributes: true, childList: true, subtree: true };

function observeDiv() {
    observer2.observe(document.querySelector("#errorMsg"), config);
    observer.observe(document.querySelector(".review-subsection"), config);
}