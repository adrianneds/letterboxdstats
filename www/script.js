const observer = new MutationObserver(() => {
    document.getElementById("content-div").style.display = "block";
    document.getElementById("content-div").style.visibility = "visible";
});

var config = { attributes: true, childList: true, subtree: true };

function observeDiv() {
    observer.observe(document.querySelector("#content-div"), config);
}