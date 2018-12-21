$(document).ready(function() {

   var score = 0;
   var answer ="";
   var choices=[];

   //when user click a continent to start to play
   document.querySelectorAll(".playGame").forEach(function(link){
     link.onclick = function (e){

        e.preventDefault();
        let continent = link.innerHTML;
        localStorage.setItem("continent", continent);

        //call startGame function that start the game
        startGame(continent);
      };

      return false;
   });

   //when user want to replay
   document.querySelector("#playAgain-link").onclick = function(e){
     e.preventDefault();
     let continent = localStorage.getItem("continent");

     //call startGame function that start the game
     startGame(continent);

   };

   //start the game
   function startGame(continent)
   {
     document.querySelector("#result").style.display = "none";
     document.querySelector("#home-display").style.display="none";
     document.querySelector("#play-display").style.display="block";

      //open a get request to get the data(countries name, capitals) from the server
     let request = new XMLHttpRequest();
     request.open("GET", "/play/"+continent);

     request.onload = function ()
     {

       //get the messages of the channel from the server response
        let response = JSON.parse(request.responseText);
        let countries = response.countries;
        let capitals = response.capitals;

        playGame(countries, capitals);
     };
     request.send();
     return false;
   }

   //generate a random number between 0 and maxi
   function randomNum(min, max)
   {
     return Math.floor(Math.random() * max) + min;

   }

   //pick three item from the list randomly
   function generateChoice(list, answer)
   {
      let max = list.length;
      let result = [];
      let counter = 0;
      let pick
      while(counter < 3)
      {
        pick = list[randomNum(0, max)];
        if(!result.includes(pick) && answer != pick)
        {
          result.push(pick);
          counter++;
        }
      }

      console.log("result before: ", result);

      //switch the correct answer in the list with another element
      let num = randomNum(0, 4);
      if(num != 3)
      {
        let temp = result[num];
        result[3] = temp;
        result[num] = answer;
      }
      else
      {
        result.push(answer);
      }

      console.log("result afer: ", result);
      console.log();

      return result;
   }

   //disable the answer options when user already clicked an answer, enable the "next" button
   function disable()
   {
     document.querySelectorAll(".answer-choice").forEach(function(choice){
            choice.classList.add("disable");
            document.querySelector("#next-button").classList.remove("disable");
     });

   }

   //enable the answer choice link to be clickable when user goes to the nexr question
   //disable the "next" button
   function enable()
   {
     document.querySelectorAll(".answer-choice").forEach(function(choice){
            choice.classList.remove("disable");
            document.querySelector("#next-button").classList.add("disable");
     });
   }


   // play the game
   function playGame(countries, capitals)
   {
        let counter = 0;
        let questionNumber = 1;
        let country = countries[counter][0];
        let answer = countries[counter][1];
        let choices = generateChoice(capitals, answer);
        let score = 0;

        //display the question section
        var source = document.querySelector("#question-choices").innerHTML;
        var template = Handlebars.compile(source);
        var context = {country: country, choices: choices, number:questionNumber};
        document.querySelector("#question").innerHTML = template(context);

        //whem the user select a answer by clicking on it
         document.querySelectorAll(".answer-choice").forEach(function(choice)
         {
            choice.onclick = function()
            {
              //show the right answer, and wrong if the user clicked the wrong one
              if(choice.innerHTML != answer)
              {
                choice.classList.add("wrongAnswer");
                let answersChoices = document.querySelectorAll(".answer-choice");
                for(var i = 0; i < 4; i++)
                {
                  if(answersChoices[i].innerHTML == answer)
                      answersChoices[i].classList.add("rightAnswer");
                }
              }
              //increase user score if the answer was right
              else
              {
                score++;
                choice.classList.add("rightAnswer");
              }

              //make the answer choice links inclickable
              disable();

            };
         });

        //when the user click  next to go to the next question
       document.querySelector("#next-button").onclick = function ()
       {

         // if it was the last question, show the user score
         if(questionNumber == 10)
         {
            document.querySelector("#question").innerHTML = "";
            document.querySelector("#result").style.display = "block";
            document.querySelector("#score").innerHTML = score +"/"+10

         }

         //go to the next question and generating new choices
         else
         {
           counter ++;
           questionNumber++;
           country = countries[counter][0];
           answer = countries[counter][1];
           choices = generateChoice(capitals, answer);

          //remove the right answer mark or wrong mark on the link
          //change text with the new answer choice
          let previousChoices = document.querySelectorAll(".answer-choice");
          for(var i =0; i <4; i++)
           {
             previousChoices[i].classList.remove("rightAnswer");
             previousChoices[i].classList.remove("wrongAnswer");
             previousChoices[i].innerHTML = choices[i];
           }

           document.querySelector("#question-number").innerHTML = questionNumber;
           document.querySelector('#country').innerHTML = country;
           enable();
         }
       };
   }
 });
