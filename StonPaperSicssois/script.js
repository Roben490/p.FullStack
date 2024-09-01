const pChoice = document.querySelector(".p-choice");
const pImg = pChoice.previousElementSibling;
const cChoice = document.querySelector(".c-choice");
const cImg = cChoice.previousElementSibling;
const weapons = document.querySelectorAll(".img");
const result = document.querySelector(".result");

function randomNumber() {
    return Math.floor(Math.random() * 3);
}

function computer() {
    const choices = ["paper", "rock", "scissors"];
    const ele = choices[randomNumber()];
    cImg.src = `./image/${ele}.jpeg`;
    cImg.id = ele; 
    cChoice.innerHTML = ele;
}

weapons.forEach((weapon) => {
    weapon.addEventListener("click", () => {
        const item = weapon.querySelector("img");
        pImg.src = item.src;
        pImg.id = weapon.id;
        pChoice.innerHTML = weapon.id;
        computer();
        check(pImg.id, cImg.id);
    });
});

function check(player, computer) {
    let msg = "";
    if (player === computer) {
        msg = "DRAW";
    } else if ((player === "rock" && computer === "scissors") ||
               (player === "scissors" && computer === "paper") ||
               (player === "paper" && computer === "rock")) {
        msg = "You WIN!";
    } else {
        msg = "You Lost!";
    }
    result.innerHTML = msg;
}