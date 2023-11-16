const forgottenBtn = document.getElementById("forgotten")

// forgottenBtn.addEventListener("click", function () {
//   console.log("hello")
//   forgottenBtn.innerHTML = "Pressed"
// })

const modal = document.getElementById("myModal")

// Get the button that opens the modal
// var btn = document.getElementById("myBtn")

// Get the <span> element that closes the modal
const span = document.getElementsByClassName("close")[0]

// When the user clicks on the button, open the modal
forgottenBtn.onclick = function () {
  console.log(1)
  modal.style.display = "block"
}

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
  modal.style.display = "none"
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = "none"
  }
}
