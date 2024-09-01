const pChoice = document.querySelector(".p-choise");
const pImg = pChoice.previousElementSibling;


const cChoice = document.querySelector(".c-choise");
const cImg = cChoice.previousElementSibling;


const weapons = document.querySelectorAll(".img");
const resault = document.querySelector(".resault");

function randomNumber(){
    return Math.floor(Math.random() * 3);
}
 
function computer() {
    const choise = ["paper", "ston", "scissors"]
    const ele = choise[randomNumber()]
    cImg.src = `image/${ele}.jpeg`
    cChoice.innerHTML = ele
}


weapons.forEach((wepon) => {
    wepon.addEventListener("click", () => {
        const item = wepon.childNodes[1];
        pImg.src = item.src;
        pImg.id = wepon.id
        pChoice.innerHTML = wepon.id
        computer()
        check(cImg.id, pImg.id)
        console.log(cImg.id);
        
        
    });
});

function check(a,b) {
    let msg = "";
    if (a === b) msg = "DRAW";

    // if (a == "rock" && b == "paper") {
    //     msg =  "You WIN!";
    // }
    // else if (a == "rock" && b == "scissors") {
    //     msg = "You Lost!";
    // }
    // if (a == "paper" && b == "scissors") {
    //     msg =  "You WIN!";
    // }
    // else if (a == "paper" && b == "ston") {
    //     msg = "You Lost!";
    // }
    // if (a == "scissors" && b == "ston") {
    //     msg = "You WIN!";
    // }
    // else if (a == "scissors" && b == "paper") {
    //     msg = "You Lost!";
    // }
    console.log(msg);
    
    return resault.innerHTML = msg
    
    //controling at click on web
    //document.body.style.pointerEvents = "none"
    
}