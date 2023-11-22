const inputBtn = document.querySelector(".generate-btn")
const emailEl = document.querySelector("#email")
const messagesEl = document.querySelector("#messages")

inputBtn.addEventListener("click", function (e) {
  messagesEl.innerHTML = ""
  if (!emailEl.value) {
    e.preventDefault()
    const messageEl = document.createElement("h4")
    messageEl.textContent = "Please input an email address"
    messageEl.classList.add("message")
    messagesEl.appendChild(messageEl)
    return false
  }
})
