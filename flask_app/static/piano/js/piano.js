
// The keys on the keyboard taken from the HTML and css
const keys = document.getElementById('keys');

// The notes on the piano that can be played
const sound = {65:"http://carolinegabriel.com/demo/js-keyboard/sounds/040.wav",
                87:"http://carolinegabriel.com/demo/js-keyboard/sounds/041.wav",
                83:"http://carolinegabriel.com/demo/js-keyboard/sounds/042.wav",
                69:"http://carolinegabriel.com/demo/js-keyboard/sounds/043.wav",
                68:"http://carolinegabriel.com/demo/js-keyboard/sounds/044.wav",
                70:"http://carolinegabriel.com/demo/js-keyboard/sounds/045.wav",
                84:"http://carolinegabriel.com/demo/js-keyboard/sounds/046.wav",
                71:"http://carolinegabriel.com/demo/js-keyboard/sounds/047.wav",
                89:"http://carolinegabriel.com/demo/js-keyboard/sounds/048.wav",
                72:"http://carolinegabriel.com/demo/js-keyboard/sounds/049.wav",
                85:"http://carolinegabriel.com/demo/js-keyboard/sounds/050.wav",
                74:"http://carolinegabriel.com/demo/js-keyboard/sounds/051.wav",
                75:"http://carolinegabriel.com/demo/js-keyboard/sounds/052.wav",
                79:"http://carolinegabriel.com/demo/js-keyboard/sounds/053.wav",
                76:"http://carolinegabriel.com/demo/js-keyboard/sounds/054.wav",
                80:"http://carolinegabriel.com/demo/js-keyboard/sounds/055.wav",
                186:"http://carolinegabriel.com/demo/js-keyboard/sounds/056.wav"};

// The creepy music link
const creepyMusic = "https://orangefreesounds.com/wp-content/uploads/2020/09/Creepy-piano-sound-effect.mp3?_=1";

// A boolean to signify if you can play on the piano
let canPlay = true;

// The notes that have to played in order for an event to happen
const weSeeYou = [87,69,83,69,69,89,79,85];

// The notes that have been pressed
let notesPlayed = []

//Adds an event mouseover event to show the notes on the piano
keys.addEventListener("mouseover", ShowNotes);

//Adds an event mouseout event to unshow the notes on the piano
keys.addEventListener("mouseout", UnShowNotes);

//Adds an event keydown event to play notes on the piano
window.addEventListener("keydown", PlaySound);


/**
 * Adds a key notes visualizer on the piano
 */
function ShowNotes()
{
    let specificKey = keys.children;

    for (key of specificKey)
    {
        let text = key.children;
        for (item of text)
        {
            if(canPlay)
            {
                item.style.display = "block";
            }
            
        }
        
    }
}

/**
 * Removes the key notes visualizer on the piano
 */
function UnShowNotes()
{
    let specificKey = keys.children;

    for (key of specificKey)
    {
        let text = key.children;
        for (item of text)
        {
            item.style.display = "none";
        }
    }
}

/**
 * Plays a sound based off the notes played on the piano
 * If the note is not on the piano it is not played
 * Calls function to make the key visual change
 */
function PlaySound()
{
    //Checks to see if it can be played
    if(event.keyCode in sound && canPlay)
    {
        let audio = new Audio(sound[event.keyCode]);
        audio.play();
        
        //Gets the key in the html and css
        const keyPressed = document.getElementById(event.keyCode);
        DoKey(keyPressed);
        setTimeout(function(){ UnDoKey(keyPressed); },50);
        
        AddToList(event.keyCode);
        

    }

}

/**
 * Shrinks the key to make it look like its been pressed down
 * @param {the key pressed on the piano} keyPressed 
 */
function DoKey(keyPressed)
{
    keyPressed.style.transform = "rotate(0deg) scale(0.75, 0.75) skew(0deg, 0deg)";
}

/**
 * Sets the pressed key back to normal
 * @param {the key pressed on the piano} keyPressed 
 */
function UnDoKey(keyPressed)
{
    keyPressed.style.transform = "rotate(0deg) scale(1, 1) skew(0deg, 0deg)";
}


/**
 * Adds a key to the has played notes and if it matches the weseeyou
 * input than it will call PianoGone function
 * @param {the key event played} eventKey 
 */
function AddToList(eventKey)
{
    if(eventKey === 87)
    {
        //redos the list
        notesPlayed = [];
        notesPlayed.push(eventKey);
    }
    else
    {
        notesPlayed.push(eventKey);

        //checks to see if the lists are the same
        if(JSON.stringify(notesPlayed) === JSON.stringify(weSeeYou))
        {
            //no notes can be played anymore
            canPlay = false;
            setTimeout(PianoGone,1000);
        }
    }
}

/**
 * Is called when the user has types weseeyou and will make the piano disappear
 * bringing the new image up
 */
function PianoGone()
{

    //Gets the header that will disappear 
    let headerGone = document.getElementById('key-title');
    headerGone.style.display = "none";

    //Gets the header that will appear
    let headerOn = document.getElementById('awoken-title');
    headerOn.style.display = "block";

    //makes the keys disappear
    keys.style.opacity = "0";
    let piano = document.getElementById('piano');

    //Sets the new background
    piano.style.backgroundImage = "url(../static/piano/images/texture.jpeg)";
    let audio = new Audio(creepyMusic);

    //Plays the creepy sound
    audio.play();
}