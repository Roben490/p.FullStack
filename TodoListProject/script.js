const inputTask = document.getElementById("inputTask");
const listContainer = document.getElementById("list-container");
document.getElementById("add-btn").addEventListener("click", addTask);

function addTask() {
    if(inputTask.value == "" ) {
        alert("You must need to add text");
    }
    else {
        let li = document.createElement("li");
        li.innerHTML = inputTask.value;
        let span = document.createElement("span");
        span.innerHTML = "<i class='fa-solid fa-trash'></i>"
        li.appendChild(span);
        listContainer.appendChild(li);
    }
    inputTask.value = "";
    saveDate();
}

addEventListener("keydown", (e) => {
    if(e.key == "Enter") { addTask() }
})

function saveDate() {
    localStorage.setItem("data", listContainer.innerHTML)
}

listContainer.addEventListener("click", (e) => {
    if(e.target.tagName.toUpperCase() === "LI") {
        e.target.classList.toggle("checked")
        saveDate();
    }
    else if(e.target.tagName.toUpperCase() === "SPAN") {
        e.target.parentElement.remove();
        saveDate();
    }
})

function showTasks() {
    listContainer.innerHTML = localStorage.getItem("data")
}

showTasks();