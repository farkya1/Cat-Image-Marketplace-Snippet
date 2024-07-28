
//used to help keep track of the input so to add to the database
var numExperiences = 1;
var numPositions = 1;

//resets the variables;
function ResetAdding(event){
  numPositions = 1;
  numExperiences = 1;
}

// Adds a new position to the form
function AddExperience(event)
{
  
  var inputContain= document.getElementById("resume-contain");

    // Create a new input element and set its attributes
    var newExperience = document.createElement("input");
    newExperience.type = "text";
    newExperience.name = numPositions+" | "+numExperiences+" | experience";
    newExperience.placeholder = "Your Experience";
    newExperience.classList.add("resume-add-input");
    newExperience.classList.add("resume-add-height");
    newExperience.required = true;

    var newDescription = document.createElement("input");
    newDescription.type = "text";
    newDescription.name = numPositions+" | "+numExperiences+" | experience-description";
    newDescription.placeholder = "Your Experience Description";
    newDescription.classList.add("resume-add-input");
    newDescription.classList.add("resume-add-height");
    newDescription.required = true;

    var newSkills = document.createElement("input");
    newSkills.type = "text";
    newSkills.name = numPositions+" | "+numExperiences+" | skills";
    newSkills.placeholder = "Your Experience's Skills (seperated by;)";
    newSkills.classList.add("resume-add-input");
    newSkills.classList.add("resume-add-height");

    numExperiences += 1;
    
    // Appends each new input
    inputContain.appendChild(newExperience);
    inputContain.appendChild(newDescription);
    inputContain.appendChild(newSkills);
    
}

// Adds a new position to the form
function AddPosition(event)
{
  
  var inputContain= document.getElementById("resume-contain");

    //position information
    var newPosition = document.createElement("input");
    newPosition.type = "text";
    newPosition.name = numPositions+" | title";
    newPosition.placeholder = "Your Position";
    newPosition.classList.add("resume-add-input");
    newPosition.classList.add("resume-add-height");
    newPosition.required = true;

    var newResponsibilities = document.createElement("input");
    newResponsibilities.type = "text";
    newResponsibilities.name = numPositions+" | responsibilities";
    newResponsibilities.placeholder = "Your Position Responsibilities";
    newResponsibilities.classList.add("resume-add-input");
    newResponsibilities.classList.add("resume-add-height");
    newResponsibilities.required = true;

    var newStartDate = document.createElement("input");
    newStartDate.type = "text";
    newStartDate.name = numPositions+" | start_date";
    newStartDate.placeholder = "Your Position Start Date 2021-05-24";
    newStartDate.classList.add("resume-add-input");
    newStartDate.classList.add("resume-add-height");
    newStartDate.required = true;

    var newEndDate = document.createElement("input");
    newEndDate.type = "text";
    newEndDate.name = numPositions+" | end_date";
    newEndDate.placeholder = "Your Position End Date";
    newEndDate.classList.add("resume-add-input");
    newEndDate.classList.add("resume-add-height");

    

    //experience information
    var newExperience = document.createElement("input");
    newExperience.type = "text";
    newExperience.name = numPositions+" | 0 | experience";
    newExperience.placeholder = "Your Experience";
    newExperience.classList.add("resume-add-input");
    newExperience.classList.add("resume-add-height");
    newExperience.required = true;

    var newDescription = document.createElement("input");
    newDescription.type = "text";
    newDescription.name = numPositions+" | 0 | experience-description";
    newDescription.placeholder = "Your Experience Description";
    newDescription.classList.add("resume-add-input");
    newDescription.classList.add("resume-add-height");
    newDescription.required = true;

    var newSkills = document.createElement("input");
    newSkills.type = "text";
    newSkills.name = numPositions+" | 0 | skills";
    newSkills.placeholder = "Your Experience's Skills (seperated by;)";
    newSkills.classList.add("resume-add-input");
    newSkills.classList.add("resume-add-height");

    numExperiences = 1;
    numPositions += 1;
    
    
    // Appends each new input
    inputContain.appendChild(newPosition);
    inputContain.appendChild(newResponsibilities);
    inputContain.appendChild(newStartDate);
    inputContain.appendChild(newEndDate);
    inputContain.appendChild(newExperience);
    inputContain.appendChild(newDescription);
    inputContain.appendChild(newSkills);
    
    
}