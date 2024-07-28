// The form button from the website
const formButton = document.getElementById('form-button');

// The form from the website
const form = document.getElementById('form');


formButton.addEventListener("click", ButtonClicked);

/**
 * runs when the formButton is clicked and turns on and off the form
 */
function ButtonClicked()
{
    if (form.style.display != "flex")
    {
        form.style.display = "flex";
    }
    else{
        form.style.display = "none";
    }
}